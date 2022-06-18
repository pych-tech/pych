from dataclasses import dataclass, field


@dataclass(slots=True, frozen=True)
class Token:
    """
    Simple dataclass to represent a token with its type,

    Following are the attributes of `Token` type
    - `token_value`: represents the value stored in the token
    - `token_type`: represents the type of token stored
    """

    token_value: str
    token_type: str = field(default="UNKNOWN")


@dataclass(slots=True)
class VariableProperties:
    value: str
