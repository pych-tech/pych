from typing import Any

from modules.commands.utils.returnable import CommandDone
from modules.utils.parsers import CommandStream, Token
from typeguard import check_type

from ..commands.utils.creator import Creator

__keywords: list[str] = [
    "if",
    "else",
    "elif",
    "for",
    "while",
    "loop",
    "match",
    "case",
    "default",
]


def __validate_type(value: Any, object_type, name: str | None = None) -> bool:
    obj_name: str = ""
    if name is None:
        try:
            obj_name = value.__name__
        except AttributeError:
            obj_name = "unknown"
    try:
        check_type(obj_name, value, object_type)
    except TypeError:
        return False
    return True


def evaluate(
    token_stream: list[Token] | None = None, string_stream: str | None = None
) -> CommandDone:
    if not (type(string_stream) is str or __validate_type(token_stream, list[Token])):
        required_type, found_type = (
            ("list[Token]", f"{type(token_stream).__name__}")
            if token_stream is not None
            else ("str", f"{type(string_stream).__name__}")
        )
        raise TypeError(f"Expected type: {required_type} found {found_type}")
    command_stream: CommandStream | None = None
    if string_stream is not None:
        if token_stream and string_stream.split()[0] not in __keywords:
            command_stream = CommandStream(string_stream)
    elif token_stream is not None:
        token_identifier = (
            token_stream[0].token_value
            if token_stream[0].token_type == "STREAM-IDENTIFIER"
            else None
        )
        if token_identifier is not None:
            if token_identifier in __keywords:
                cmd_out = CommandDone(
                    command_name=token_identifier, new_env_variables={}
                )
                cmd_out.command_output = "pych: tokens not implemented"
                cmd_out.EXIT_CODE = 1
                return cmd_out
            command_stream = CommandStream(
                "".join([token.token_value for token in token_stream])
            )
        else:
            command_stream = None

    if command_stream is not None:
        print(command_stream)
        return Creator(command_stream.name).run(
            command_stream.arguments,
            CommandDone(command_name=command_stream.name, new_env_variables={}),
        )
    else:
        cmd_out = CommandDone(command_name="", new_env_variables={})
        cmd_out.EXIT_CODE = 127
        cmd_out.command_output = "pych: command not found error"
        return cmd_out
