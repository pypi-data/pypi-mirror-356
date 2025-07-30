import argparse


def main():
    parser = argparse.ArgumentParser(
        prog="accounts-api-client",
        description="Scripts for Accounts API Client",
    )

    # To add a sub-command, you can un-comment this snippet
    # More information on https://docs.python.org/3/library/argparse.html#sub-commands
    # commands = parser.add_subparsers(help="Explain your sub commands globally here")
    # my_command = commands.add_parser("commandX", help="Do something")
    # my_command.set_defaults(func=command_main)
    # my_command.add_argument("element_id", type=uuid.UUID)

    args = vars(parser.parse_args())
    if "func" in args:
        args.pop("func")(**args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
