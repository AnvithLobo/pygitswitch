import sys
from pathlib import Path
from shutil import which
from gitswitch.helpers import run_command


def github_install(beta=False):
    # Check for winget ( windows package manager available by default in windows 11)
    # https://github.com/microsoft/winget-cli

    if beta:
        package = "GitHub.GitHubDesktopBeta"
    else:
        package = "GitHub.GitHubDesktop"

    if which("winget"):
        print("Found Windows Package Manager installing GitHub Desktop using winget \n\n")

        # Search for package
        return_data = run_command(f"winget show -e {package}", std_output=True)
        if return_data.return_code != 0:
            print(f"\n\nProcess exited with return code {return_data.return_code}")
            print("If retrying does not work open a support ticket "
                  "https://github.com/AnvithLobo/github-switch/issues/new")
            sys.exit(-1)

        # Install Package
        print("\n\n")
        return_data = run_command(f"winget install -e {package}", std_output=True)
        if return_data.return_code != 0:
            print(f"\n\n Failed to install process exited {return_data.return_code}")
            print("If retrying does not work open a support ticket "
                  "https://github.com/AnvithLobo/github-switch/issues/new")
            sys.exit(-1)

    else:
        # ToDo: Add a installer method when winget is not available
        print("Windows Package Manager (winget) is currently not installed please install GitHub manually for now")
        sys.exit(-1)


def get_github_path():
    """
    returns pathlib.Path(Github path) or None
    """
    if which('github'):
        github_bat_path = Path(which('github'))
        github_folder = github_bat_path.parents[1]
        github_exe_path = github_folder / "GitHubDesktop.exe"
        return github_exe_path
    else:
        return None
