import subprocess
import logging

logger = logging.getLogger(__name__)

default_bin_dir = '/usr/app/bin'

def run_command(command, cwd=None, log_stdout=True, log_stderr=True):
    """Run a shell command and stream the output.
    
    Args:
        command (str): The command to run.
        cwd (str, optional): The working directory. Defaults to None.
        log_stdout (bool, optional): Whether to log the stdout. Defaults to True.
        log_stderr (bool, optional): Whether to log the stderr. Defaults to True.
    
    Returns:
        tuple: A tuple (stdout, stderr) containing the parsed stdout and stderr string.
    """
    process = subprocess.Popen(command, shell=True, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    stdout = []
    stderr = []
    
    for line in iter(process.stdout.readline, ''):
        content = line.strip()
        if log_stdout:
            logger.info(content)
        stdout.append(content)
    
    for line in iter(process.stderr.readline, ''):
        content = line.strip()
        if log_stderr:
            logger.error(content)
        stderr.append(content)
    
    process.wait()
    return "\n".join(stdout), "\n".join(stderr)