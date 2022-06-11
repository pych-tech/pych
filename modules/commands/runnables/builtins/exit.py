from modules.commands.utils.returnable import CommandDone

from .. import Executable


class ExitCommand(Executable):
    def __init__(self) -> None:
        super().__init__()

    def run(self, _: list[str], returnable: CommandDone) -> CommandDone:
        returnable.command_name = "exit"
        returnable.EXIT_CODE = 0
        returnable.terminate_session = True
        return returnable
