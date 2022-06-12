from modules.commands.runnables.utils import Executable
from modules.commands.utils.returnable import CommandDone


class ClearCommand(Executable):
    def __init__(self) -> None:
        pass

    def run(self, _: list[str], returnable: CommandDone) -> CommandDone:
        returnable.command_output = f"{chr(27)} 2[j \033c \x1bc"
        return returnable
