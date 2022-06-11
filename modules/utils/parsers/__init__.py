from dataclasses import dataclass, field


def _split_stream(string: str) -> list[str]:
    token_container: list[str] = []
    token_string: str = ""
    token_sub_string: str = ""
    opening_braces: str = "({["
    closing_braces: str = ")}]"
    brace_check: bool = False
    brace_close: str = ""
    nest_count: int = 0
    single_quote_check: bool = False
    double_quote_check: bool = False

    for ch in string:
        previous_check_state: bool = (
            brace_check or single_quote_check or double_quote_check
        )

        if ch == "'" and not (double_quote_check or brace_check):
            if single_quote_check:
                token_sub_string += ch
            single_quote_check = not single_quote_check

        elif ch == '"' and not (single_quote_check or brace_check):
            if double_quote_check:
                token_sub_string += ch
            double_quote_check = not double_quote_check

        if not (double_quote_check or single_quote_check):
            if ch in opening_braces and brace_check:
                nest_count += 1

            if ch in opening_braces and not brace_check:
                brace_check = True
                brace_close = closing_braces[opening_braces.find(ch)]

            if ch == brace_close and brace_check:
                if nest_count:
                    nest_count -= 1

                elif previous_check_state == (
                    brace_check or single_quote_check or double_quote_check
                ):
                    token_sub_string += ch
                    brace_check = False

        if brace_check or double_quote_check or single_quote_check:
            token_sub_string += ch

        else:
            if ch not in "\t ":
                if (
                    brace_check or single_quote_check or double_quote_check
                ) == previous_check_state:
                    token_string += ch

            else:
                if token_string:
                    token_container.append(token_string)
                    token_string = ""
                continue
        if (
            not (brace_check or single_quote_check or double_quote_check)
            and token_sub_string
        ):
            token_container.append(token_sub_string)
            token_sub_string = ""

        elif brace_check and token_string:
            token_container.append(token_string)
            token_string = ""

    if token_string:
        token_container.append(token_string)
        token_string = ""

    if token_sub_string:
        token_container.append(token_sub_string)
        token_sub_string = ""

    return token_container


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
class CommandStream:
    stream: str = field(default_factory=str, repr=False)
    name: str = field(default_factory=str, init=False)
    arguments: list[str] = field(default_factory=list, init=False)

    def __post_init__(self):
        stream = _split_stream(self.stream)
        self.name = stream[0]
        self.arguments = stream[1::]
