from dataclasses import dataclass, field
from multipledispatch import dispatch

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
