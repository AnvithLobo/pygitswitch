import sys
import subprocess
import shlex


def run_command(command: str, std_output=False):
    """
        run command using subprocess and return exit code
    """
    command = shlex.split(command)
    if std_output:
        return_data = subprocess.run(command, stderr=sys.stderr, stdout=sys.stdout)
    else:
        return_data = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    return return_data.returncode
