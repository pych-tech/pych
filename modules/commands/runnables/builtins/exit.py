import argparse
from argparse import ArgumentParser

from modules.commands.utils.returnable import CommandDone

from .. import Executable


class ExitCommand(Executable):
    def __init__(self) -> None:
        super().__init__()

    def run(self, arguments: list[str], returnable: CommandDone) -> CommandDone:
        parser = ArgumentParser(
            prog="exit",
            description="Quit the current pych session",
            add_help=False,
            usage="exit [args]",
        )
        parser.add_argument(
            "-q",
            "--quiet",
            action="store_true",
            help="quit the session without returning the exit code",
        )
        parser.add_argument(
            "-h", "--help", action="store_true", help="show this help message and quit"
        )
        args = parser.parse_args(arguments)

        if args.quiet:
            returnable.EXIT_CODE = 0
        returnable.command_name = "exit"
        if args.help:
            parser.print_help()
        else:
            returnable.terminate_session = True
        return returnable
