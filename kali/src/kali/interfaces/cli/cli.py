import argparse

from .commands.activate import activate
from .commands.doctor import doctor
from .commands.info import info
from .commands.init import init_project
from .commands.login import login
from .commands.new import new_project
from .commands.run import run_operator
from .commands.status import status
from .commands.upgrade import upgrade


def main():
    parser = argparse.ArgumentParser(prog="kali")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("activate")
    sub.add_parser("doctor")
    sub.add_parser("info")
    sub.add_parser("init")
    sub.add_parser("login")

    new_cmd = sub.add_parser("new")
    new_cmd.add_argument("name")

    run_cmd = sub.add_parser("run")
    run_cmd.add_argument("file")

    sub.add_parser("status")
    sub.add_parser("upgrade")

    args = parser.parse_args()

    if args.command == "activate":
        activate()
    elif args.command == "doctor":
        doctor()
    elif args.command == "info":
        info()
    elif args.command == "init":
        init_project()
    elif args.command == "login":
        login()
    elif args.command == "new":
        new_project(args.name)
    elif args.command == "run":
        run_operator(args.file)
    elif args.command == "status":
        status()
    elif args.command == "upgrade":
        upgrade()
    else:
        parser.print_help()
