import os
import subprocess
import sys
from pathlib import Path
import time
import shutil
import ctypes
from gitswitch.installer import get_github_path
from gitswitch.helpers import run_command, create_config, get_accounts, get_current_user

# ToDo: Works towards making this compatible on Linux (https://github.com/shiftkey/desktop) and MacOS
app_data_path = Path(os.getenv("appdata"))
github_folder = "GitHub Desktop"
github_base_path = app_data_path / github_folder
github_executable = "GitHubDesktop.exe"
config_file = Path('~').expanduser().absolute() / ".gitconfig"


def launch_github():
    """
    Launch Github Desktop
    """

    # this makes github think we're trying to open a repository in current directory
    """where_github = run_no_output('where github')
    if where_github.returncode != 0:
        raise Exception(f"Error finding github path \n {where_github.stderr.decode()}")
    github_path = Path(where_github.stdout.decode().splitlines()[-1])"""

    github_path = get_github_path()
    subprocess.Popen(github_path)


def github_process():
    return subprocess.check_output(['TASKLIST', '/FI', f'imagename eq {github_executable}']). \
        decode().splitlines()[-1].startswith(github_executable)


def kill_github():
    """
    Kill github process if running
    """
    github_running = github_process()

    if github_running:
        print("\nStopping Github Process")
        kill_status = run_command(f"taskkill /f /im {github_executable}")
        print(kill_status.returncode)
        if kill_status.returncode != 0 and "ERROR: The process" not in kill_status.stderr.decode():
            raise Exception(f"Error Killing {github_executable} with error \n {kill_status.stderr.decode()}")


def existing_data_handler(folder_ext="", config_ext="", delete=False):
    # move the current github folder if exists to Github Desktop-Backup
    if github_base_path.is_symlink():
        github_base_path.unlink(missing_ok=True)
    elif github_base_path.is_dir():
        if delete:
            shutil.rmtree(github_base_path, ignore_errors=True)
        else:
            github_base_path.rename(github_base_path.parent / (github_folder + folder_ext))

    if config_file.is_symlink():
        config_file.unlink(missing_ok=True)
    elif config_file.is_file():
        if delete:
            config_file.unlink(missing_ok=True)
        else:
            config_file.rename(config_file.parent / (".gitconfig" + config_ext))


def setup(setup_accounts, setup_type='switch', current_user=None):
    """
    Initial accounts setup / method to setup more accounts
    """
    kill_github()
    # add a init setup type method and create a gitswitch.json
    if setup_type == 'init':
        create_config(file=Path().home() / "gitswitch.json")

    # get previously setup accounts
    accounts = get_accounts()

    # check if account already exists
    if current_user:
        all_accounts = [current_user] + setup_accounts
    else:
        all_accounts = setup_accounts

    for user in all_accounts:
        if user in accounts:
            print(f"user:{user} already exists in config file {Path().home() / 'gitswitch.json'}")
            print("use a different username or use 'gitswich deluser' to delete the existing user before trying again")
            sys.exit(-1)

    if current_user:
        existing_data_handler(folder_ext=f"{current_user}", config_ext=f"{current_user}")
    else:
        existing_data_handler(folder_ext="-backup", config_ext="-backup")

    for user in setup_accounts:

        if (github_base_path.parent / (github_folder + user)).exists():
            raise Exception(f"user: {user} already added. \n If you're using init try add_user method instead.")

        print(f"\n\nSetting up account for user : {user}")
        print("\tLaunching github please login... ")

        launch_github()

        # wait for user to login
        input("\tHit Enter once logged in  : ")
        while github_process():
            # Need to manually close since killing github process doesn't seem store login data
            input("Please manually close github and hit Enter : ")
            time.sleep(1)
        print("\t waiting for all process to end")
        time.sleep(2)
        # rename the created folder and config with username at the end
        existing_data_handler(folder_ext=user, config_ext=user)

    # Write all accounts to JSON file
    create_config(file=Path().home() / "gitswitch.json", accounts=accounts + all_accounts)

    print("\n\nFinished setting up account/s")
    print("\n run (switcher.py switch) to start using github")


def symlink(host, symlink_to, is_dir=False):
    # ToDo : make this to actually rename folder and keep track of current user account in config file
    command = f"mklink \"{symlink_to}\" \"{host}\""
    if is_dir:
        command += " /d"

    # spend an hour to find how sudo in windows works !
    command = "/c " + command
    ctypes.windll.shell32.ShellExecuteW(None, "runas", 'cmd.exe', command, None, 1)
    # run(command)


def copy(host, copy_to, is_dir=False):
    shutil.copy(host, copy_to)


def switcher(accounts: list, start_github: bool = False) -> None:
    while github_process():
        kill_github()
        time.sleep(1)

    # delete current_data
    if not get_current_user():
        existing_data_handler(delete=True)
    else:
        # ToDo: Rename the current default folder to existing user
        pass

    print("Select Account")
    print("---------------\n")
    for index, user in enumerate(accounts):
        print(f"{index + 1}. {user}")

    while True:
        user_input = input(f"\n Enter Your Choice (1-{len(accounts)}) : ")
        try:
            user_input = int(user_input.strip())
            if user_input not in range(1, len(accounts) + 1):
                raise ValueError
            break
        except ValueError:
            print("Invalid input \n")

    print("---------------\n")
    selected_user = accounts[user_input - 1]
    print(f"\nSwitching account to user : {selected_user}")

    # symlink github folder and config file
    symlink(host=Path(github_base_path.as_posix() + selected_user), symlink_to=github_base_path, is_dir=True)
    copy(host=Path(config_file.as_posix() + selected_user), copy_to=config_file, is_dir=False)

    if start_github:
        launch_github()
    print("\nDone ")
