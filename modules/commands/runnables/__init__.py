from abc import ABC, abstractmethod

from modules.commands.utils.returnable import CommandDone


class InvalidCommandType(Exception):
    def __init__(self, *args: object, defector: object | None = None) -> None:
        self.defector = defector
        super().__init__(*args)


class MapNotParsedError(Exception):
    pass


class Executable(ABC):
    """
    Abstract class to ensure that all builtin methods have a run method
    Make sure that all builtin commands inherit from `Executable`.

    This class makes sure that all the builtin executable classes have the run function
    accepting the same arguments and returning the same type
    """

    @abstractmethod
    def run(self, arguments: list[str], returnable: CommandDone) -> CommandDone:
        """Executable function for any builtin command"""
        return returnable
