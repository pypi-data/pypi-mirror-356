import os
import pexpect
import subprocess
import uuid
import logging
import time
import threading

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("ShellSession")

global_shell_session = None

def bash(cmd_string, suppress_exception=False):
    """
    Run a shell command in a one-off subprocess, streaming its output in real time.
    Merges stdout and stderr. Raises CalledProcessError on non-zero exit unless
    suppress_exception=True.
    """
    process = subprocess.Popen(
        cmd_string,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        stdin=subprocess.DEVNULL,
        bufsize=1,
        text=True
    )

    for line in iter(process.stdout.readline, ''):
        print(line, end='', flush=True)

    process.stdout.close()
    returncode = process.wait()

    if returncode != 0 and not suppress_exception:
        raise subprocess.CalledProcessError(returncode, cmd_string)

    return returncode


def experimental_bash(cmd_string, suppress_exception=False):
    """
    Run a shell command in a persistent bash session, streaming its output in real time.
    This is an experimental feature and may not work as expected.
    Args:
        cmd_string (str): The shell command to execute.
        suppress_exception (bool): If True, suppress exceptions on non-zero exit code.
        
    Returns:
        int: The exit code of the command.
    """
    global global_shell_session
    if global_shell_session is None:
        global_shell_session = ShellSession()
    return global_shell_session.run_command(cmd_string, suppress_exception)

class ShellSession:
    """
    A class that manages a persistent interactive bash session using pexpect.
    Provides methods to run commands and process their output through callbacks.
    """
    
    def __init__(self, output_callback=None, timeout=60):
        """
        Initialize a new ShellSession with a persistent bash shell.
        
        Args:
            output_callback (callable, optional): A function that will be called with each 
                                                 line of output. If it returns True, the session will exit.
            timeout (int): Timeout in seconds for expect operations.
        """
        self._output_callback = output_callback
        self._timeout = timeout
        # Use UUID-based prompt marker to avoid conflicts with command output
        self._prompt = f'PEXPECT_PROMPT_{uuid.uuid4().hex}>'
        
        # Create a custom output handler
        class CustomPexpectOutputHandler:
            def __init__(self, callback):
                self.callback = callback
                
            def write(self, data):
                return self.callback(data)
                
            def flush(self):
                pass
        
        # Set up custom output handling
        def custom_output_handler(data):
            # Print the data to stdout (except our custom prompt)
            if self._prompt not in data:
                print(data, end='', flush=True)
            
            # Process the data if callback is provided
            if self._output_callback and data:
                if self._output_callback(data):
                    logger.info("Callback triggered exit condition.")
                    print("\nCallback triggered exit condition.")
                    return True
            return False
        
        # Start a persistent bash session
        logger.info(f"Starting persistent bash session with timeout {timeout} seconds")
        self._child = pexpect.spawn(
            '/bin/bash',
            ['--norc', '--noprofile'], 
            encoding='utf-8',
            echo=False,
            timeout=self._timeout
        )
        
        # Set up a custom prompt to reliably detect command completion
        self._child.sendline(f'export PS1="{self._prompt}"')
        self._child.expect(self._prompt)
        
        # Set up output handling
        self._child.logfile_read = CustomPexpectOutputHandler(custom_output_handler)
        
    def run_command(self, cmd_string: str, raise_on_error: bool = False) -> int:
        """
        Runs a command in the persistent bash session, processing real-time output.
        
        Args:
            cmd_string (str): The shell command to execute.
            raise_on_error (bool): If True, raise an exception on non-zero exit code.
            
        Returns:
            int: The actual exit code of the command.
        """
        logger.info(f"Running command: {cmd_string}")
        
        try:
            # Send the command
            self._child.sendline(cmd_string)
            
            # Process output until we see our prompt again (command completed)
            while True:
                try:
                    # Wait for prompt, EOF, or timeout
                    index = self._child.expect([self._prompt, pexpect.EOF, pexpect.TIMEOUT])
                    
                    # Get the output since the last expect
                    output = self._child.before
                    
                    # Process the output if callback is provided
                    if self._output_callback and output:
                        if self._output_callback(output):
                            logger.info("Callback triggered exit condition.")
                            print("\nCallback triggered exit condition.")
                            return 0
                    
                    # Check if we've reached the prompt (command completed)
                    if index == 0:  # prompt
                        logger.info("Command completed. Getting exit code.")
                        
                        # Get the exit code
                        exit_code_marker = f"EXITCODE_{uuid.uuid4().hex}"
                        self._child.sendline(f"echo $?; echo {exit_code_marker}")
                        self._child.expect(exit_code_marker)
                        
                        # Extract the exit code from the output
                        exit_code_output = self._child.before.strip()
                        exit_code_lines = exit_code_output.splitlines()
                        try:
                            exit_code = int(exit_code_lines[-1]) if exit_code_lines else 0
                        except ValueError:
                            exit_code = 1
                        
                        # Wait for the prompt again
                        self._child.expect(self._prompt)
                        
                        # Raise exception if requested and exit code is non-zero
                        if exit_code != 0 and raise_on_error:
                            raise subprocess.CalledProcessError(
                                exit_code, cmd_string, f"Command failed with exit code {exit_code}: {cmd_string}"
                            )
                        
                        logger.info(f"Command completed with exit code {exit_code}.")
                        return exit_code
                        
                    # Check if we've reached EOF
                    if index == 1:  # pexpect.EOF
                        logger.info("Session ended unexpectedly (EOF).")
                        return 1
                        
                    # Check if we've timed out
                    if index == 2:  # pexpect.TIMEOUT
                        logger.debug("Timeout waiting for output, continuing...")
                        continue
                        
                except pexpect.TIMEOUT:
                    logger.debug("Timeout waiting for output, continuing...")
                    continue
                except pexpect.EOF:
                    logger.info("Session ended unexpectedly (EOF).")
                    return 1
            
        except KeyboardInterrupt:
            logger.info("Process interrupted by user.")
            return 1
        
    def close(self):
        """Close the persistent bash session."""
        logger.info("PexpectSession closed")
        if self._child and self._child.isalive():
            self._child.sendline("exit")
            self._child.terminate(force=True)

class FilePoller:
    """
    Polls for the existence of a specific file and executes a callback when found.
    """
    
    def __init__(self, file_path, on_file_found_callback, check_interval=1):
        """
        Initialize a new FilePoller.
        
        Args:
            file_path (str): Path to the file to poll for.
            on_file_found_callback (callable): Function to call when the file is found.
            check_interval (int): How often to check for the file (seconds).
        """
        self.file_path = file_path
        self.on_file_found_callback = on_file_found_callback
        self.check_interval = check_interval
        self._stop_event = threading.Event()
        self._thread = None
        logger.info(f"FilePoller initialized for file: {file_path}")
        
    def start(self):
        """Start polling in a background thread."""
        if self._thread and self._thread.is_alive():
            logger.warning("Poller already running")
            return
            
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._poll_file)
        self._thread.daemon = True
        self._thread.start()
        logger.info("FilePoller started")
        
    def stop(self):
        """Stop the polling thread."""
        self._stop_event.set()
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=2)
        logger.info("FilePoller stopped")
        
    def _poll_file(self):
        """Poll for the file existence."""
        while not self._stop_event.is_set():
            if os.path.exists(self.file_path):
                logger.info(f"Target file found: {self.file_path}")
                if self.on_file_found_callback:
                    self.on_file_found_callback()
                return
            time.sleep(self.check_interval)
