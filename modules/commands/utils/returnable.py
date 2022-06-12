from dataclasses import dataclass, field
from typing import Union

from modules.utils import VariableProperties


@dataclass(kw_only=True, slots=True)
class CommandDone:
    command_name: str
    new_env_variables: dict[str, Union[str, VariableProperties]]
    EXIT_CODE: int = field(default_factory=int, init=False)
    command_output: str = field(default_factory=str, init=False)
    terminate_session: bool = field(default_factory=bool, init=False, repr=False)
