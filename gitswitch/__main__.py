import argparse
import sys

from gitswitch.installer import get_github_path, github_install
from gitswitch.switcher import switcher, setup, delete_user


def parse_args():
    parser = argparse.ArgumentParser(
        description="GitHub Desktop Account switcher"
    )

    subparser = parser.add_subparsers(title='Options', dest='script')

    switch_parser = subparser.add_parser('switch', help="Switch github account")
    switch_parser.add_argument('-d', '--do-not-start-github', help="Do NOT Start github after switching account",
                               action="store_true", default=False)
    switch_parser.add_argument('-u', '--user', help="Run gitswitch and switch user with an argument", nargs="+", metavar="USERID")

    setup_parser = subparser.add_parser('init', help="Initial Setup (should only be used once)")
    setup_parser.add_argument("-c", "--current-user", help="Store current user login as (do not delete current user)",
                              type=str, default=None, metavar="USERNAME")
    setup_parser.add_argument("-u", "--users", help="all usernames seperated by space", nargs=1, metavar='USERNAME')

    add_user_parser = subparser.add_parser('adduser', help="Add more users each user proceeded with a space")
    add_user_parser.add_argument('user', metavar="USERNAME", nargs='+')

    install_parser = subparser.add_parser('install', help="Install Github")
    install_parser.add_argument('-b', '--beta', help="Install GitHub Desktop Beta", action="store_true")

    del_user_parser = subparser.add_parser('deluser', help="Delete users each user proceeded with a space")
    del_user_parser.add_argument('user', metavar="USERNAME", nargs='+')

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
        if not args.get('user'):
            temp = -1
        else:
            temp = args.get('user')[0]
        switcher(start_github=not args.get('do_not_start_github'), cli=int(temp))
    elif script == "init":
        accounts = args.get('users')
        if accounts:
            if args.get('current_user') in accounts:
                accounts.remove(args.get('current_user'))

        if not accounts and not args.get('current_user'):
            print("specify -c and or -u with username for init")
            sys.exit(-1)

        setup(setup_accounts=accounts, current_user=args.get('current_user'), setup_type='init')
    elif script == "adduser":
        setup(setup_accounts=args.get('user'))
    elif script == "install":
        github_install(beta=args.get("beta"))
    elif script == "deluser":
        delete_user(users=args.get("user"))


if __name__ == '__main__':
    main(vars(parse_args()))
