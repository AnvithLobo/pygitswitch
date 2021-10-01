import os
import subprocess
import shlex
import sys
from pathlib import Path
import argparse
import time
import shutil
import ctypes


# Add Users here
accounts = ['user1', 'user2', 'user3']

app_data_path = Path(os.getenv("appdata"))
github_folder = "GitHub Desktop"
github_base_path = app_data_path / github_folder
github_executable = "GitHubDesktop.exe"
config_file = Path('~').expanduser().absolute() / ".gitconfig"


def run(command):
    subprocess.run(command, stderr=sys.stderr, stdout=sys.stdout)


def run_no_output(command):
    return subprocess.run(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def launch_github():
    """
    Launch Github Desktop
    """

    # this makes github think we're trying to open a repository in current directory
    """where_github = run_no_output('where github')
    if where_github.returncode != 0:
        raise Exception(f"Error finding github path \n {where_github.stderr.decode()}")
    github_path = Path(where_github.stdout.decode().splitlines()[-1])"""

    github_path = (app_data_path / "..\Local\GitHubDesktop\GitHubDesktop.exe").resolve()
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
        kill_status = run_no_output(f"taskkill /f /im {github_executable}")
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


def setup(setup_accounts):
    """
    Initial accounts setup / method to setup more accounts
    """
    kill_github()

    existing_data_handler(folder_ext="-backup", config_ext="-backup")

    for user in setup_accounts:

        if (github_base_path.parent / (github_folder + user)).exists():
            raise Exception(f"user: {user} already added. \n If you're using init try add_user method instead.")

        print(f"\n\nSetting up account for user : {user}")
        print(f"\tLaunching github please login... ")

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

    print("\n\nFinished setting up account/s")
    print("\n run (switcher.py switch) to start using github")


def symlink(host, symlink_to, is_dir=False):
    command = f"mklink \"{symlink_to}\" \"{host}\""
    if is_dir:
        command += " /d"

    # spend an hour to find how sudo in windows works !
    command = "/c " + command
    ctypes.windll.shell32.ShellExecuteW(None, "runas", 'cmd.exe', command, None, 1)
    # run(command)


def copy(host, copy_to, is_dir=False):
    shutil.copy(host, copy_to)


def switcher(start_github=False):
    while github_process():
        kill_github()
        time.sleep(1)

    # delete current_data 
    existing_data_handler(delete=True)

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


def parse_args():
    parser = argparse.ArgumentParser(
        description="GitHub Desktop Account switcher"
    )

    subparser = parser.add_subparsers(title='Options', dest='script')

    switch_parser = subparser.add_parser('switch', help="Switch github account")
    switch_parser.add_argument('-d', '--not-start-github', help="Start github after switching account",
                               action="store_false")

    setup_parser = subparser.add_parser('init', help="Initial Setup (should only be used once)")

    add_user_parser = subparser.add_parser('add_user', help="Add more users each user proceeded with a space")
    add_user_parser.add_argument('user', metavar="username", nargs='+')

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit()

    return parser.parse_args()


def main(args):
    script = args.get('script')
    if script == "switch":
        switcher(start_github=not args.get('start_github'))
    elif script == "init":
        setup(setup_accounts=accounts)
    elif script == "add_user":
        setup(setup_accounts=args.get('user'))
        print('\nmake sure to modify the accounts in script to add new users')


if __name__ == '__main__':
    main(vars(parse_args()))
