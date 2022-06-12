from modules.commands.runnables.utils import Commands
from modules.commands.utils.returnable import CommandDone


class Creator:
    def __init__(self, command_name: str):
        self.name = command_name
        self.command_map = Commands()

    def run(self, arguments: list[str], returnable: CommandDone) -> CommandDone:

        command = self.command_map.get(self.name)
        if command is None:
            returnable.EXIT_CODE = 127
            returnable.command_output = f"pych: command not found {self.name}"
            return returnable
        else:
            command().run(arguments, returnable)
            return returnable
