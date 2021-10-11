import argparse
import sys

from gitswitch.installer import get_github_path, github_install
from gitswitch.switcher import switcher, setup


def parse_args():
    parser = argparse.ArgumentParser(
        description="GitHub Desktop Account switcher"
    )

    subparser = parser.add_subparsers(title='Options', dest='script')

    switch_parser = subparser.add_parser('switch', help="Switch github account")
    switch_parser.add_argument('-d', '--do-not-start-github', help="Do NOT Start github after switching account",
                               action="store_false", default=True)

    setup_parser = subparser.add_parser('init', help="Initial Setup (should only be used once)")
    setup_parser.add_argument("-c", "--current-user", help="Store current user login as (do not delete current user)",
                              type=str, default=None, metavar="USERNAME")
    setup_parser.add_argument("-u", "--users", help="all usernames seperated by space", nargs="+", metavar='USERNAME')

    add_user_parser = subparser.add_parser('add_user', help="Add more users each user proceeded with a space")
    add_user_parser.add_argument('user', metavar="USERNAME", nargs='+')

    install_parser = subparser.add_parser('install', help="Install Github")
    install_parser.add_argument('-b', '--beta', help="Install GitHub Desktop Beta", action="store_true")

    """if len(sys.argv) == 1:
        parser.print_help()
        sys.exit()"""

    return parser.parse_args()


def main(args=None):
    if not args:
        args = vars(parse_args())

    script = args.get('script')
    if script != "install":
        # Check if github is installed
        if not get_github_path:
            print("Github Not found install it manually or using the install script")
    if script == "switch" or not script:
        switcher(start_github=not args.get('do_not_start_github'))
    elif script == "init":
        accounts = args.get('users')
        if accounts:
            if args.get('current_user') in accounts:
                accounts.remove(args.get('current_user'))

        if not accounts and not args.get('current_user'):
            print("specify -c and or -u with username for init")
            sys.exit(-1)

        setup(setup_accounts=accounts, current_user=args.get('current_user'), setup_type='init')
    elif script == "add_user":
        setup(setup_accounts=args.get('user'))
        print('\nmake sure to modify the accounts in script to add new users')
    elif script == "install":
        github_install(beta=args.get("beta"))


if __name__ == '__main__':
    main(vars(parse_args()))
