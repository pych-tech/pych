from typing import Type

from . import Executable, InvalidCommandType, MapNotParsedError
from .builtins.clear import ClearCommand
from .builtins.exit import ExitCommand


class InvalidCommandType(Exception):
    def __init__(self, *args: object, defector: object | None = None) -> None:
        self.defector = defector
        super().__init__(*args)


command_map: dict[str, Type[Executable]] = {"exit": ExitCommand, "clear": ClearCommand}


class Commands:
    def __init__(self) -> None:
        self.__command_map = None
        self.__post_init__()
        pass

    def __post_init__(self) -> None:
        for key, value in command_map.items():
            if type(key) is not str:
                raise TypeError(f"Expected `str` found `{type(key)}` for key: {key}")

            if not issubclass(value, Executable):
                raise InvalidCommandType(
                    "Builtin command must inherit from `Executable`", defector=value
                )

        self.__command_map = command_map

    def get(self, command_name) -> Type[Executable] | None:
        if self.__command_map is None:
            raise MapNotParsedError()
        return self.__command_map.get(command_name)
