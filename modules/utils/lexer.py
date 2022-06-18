from dataclasses import dataclass

from modules.utils.extra import isfloat


@dataclass(slots=True, frozen=True)
class Token:
    value: str
    token_type: str


class InvalidTokenErr(Exception):
    pass


class Lexer:
    def __init__(self) -> None:
        self.character_map: dict[str, str] = {
            "if": "CHECK_CONDITION",
            "else": "CHECK_CONDITION_INVERSE",
            "for": "ITERATE_RANGER",
            "while": "ITERATE_CONDITIONAL",
            "switch": "CONDITION_MATCH",
            "case": "PATTERN_MATCH",
            "let": "VARIABLE_ASSIGNMENT",
            "dyn": "DYNAMIC_ASSIGNMENT",
            "mut": "MUTABLE_ASSIGNMENT",
            "exit": "TERMINATE",
            "true": "BOOLEAN",
            "false": "BOOLEAN",
            "in": "IN_RANGE",
            "&&": "CONJUNCTION",
            "||": "DISJUNCTION",
            "==": "CHECK_EQUALS",
            "+=": "INCREMENT_ASSIGNMENT",
            "-=": "DECREMENT_ASSIGNMENT",
            "=": "ASSIGN",
            "$": "EXPAND",
        }

    def __string_type(self, string: str) -> Token:
        return Token(
            string,
            "Data_NUMBER"
            if string.isdecimal()
            else "Data_FLOAT"
            if isfloat(string)
            else "Data_BOOLEAN"
            if self.character_map.get(string) is not None
            and self.character_map.get(string) == "BOOLEAN"
            else f"Keyword_{self.character_map.get(string)}"
            if self.character_map.get(string) is not None
            else "Token",
        )

    def __token_type(self, string: str, follow=False) -> Token:
        tmp = self.character_map.get(string)
        if tmp is not None:
            return Token(string, f"Operator_{tmp}{'_' if follow else ''}")
        else:
            return Token(string, f"Operator_SPECIAL{'_' if follow else ''}")

    def lex(self, string: str) -> list[Token]:
        token_map: list[Token] = []
        eval_string: str = ""
        eval_sub_string: str = ""
        eval_subtoken_string: str = ""
        brace_types: dict[str, str] = {"(": ")", "{": "}", "[": "]"}
        brace: bool = False
        brace_close: str = ""
        brace_nest: int = 0
        single_quote: bool = False
        double_quote: bool = False
        braced: bool = False
        for token in string:
            if token == "#":
                break
            previous_state: bool = single_quote or double_quote or brace
            if token == "'" and not (double_quote or brace):
                single_quote = not single_quote
            elif token == '"' and not (single_quote or brace):
                double_quote = not double_quote

            if not (single_quote or double_quote):
                close = brace_types.get(token)
                if close is not None:
                    if brace:
                        if close == brace_close:
                            brace_nest += 1
                    else:
                        brace = True
                        brace_close = close
                        continue
                elif token == brace_close:
                    if brace_nest > 0:
                        brace_nest -= 1
                    elif previous_state == brace:
                        brace = False
                        braced = True

            if brace or single_quote or double_quote:
                if not (
                    (token == "'" and single_quote) or (token == '"' and double_quote)
                ):
                    eval_sub_string += token
            else:
                if token.isalnum() or token == "." or token == "_":
                    if eval_subtoken_string:
                        token_map.append(self.__token_type(eval_subtoken_string, True))
                        eval_subtoken_string = ""
                    eval_string += token
                elif (
                    token != " "
                    and token != "\t"
                    and token != '"'
                    and token != "'"
                    and token != "("
                    and token != ")"
                    and token != "{"
                    and token != "}"
                    and token != "["
                    and token != "]"
                ):
                    if eval_string:
                        token_map.append(self.__string_type(eval_string))
                        eval_string = ""
                    eval_subtoken_string += token
                else:
                    if eval_subtoken_string:
                        token_map.append(self.__token_type(eval_subtoken_string))
                        eval_subtoken_string = ""
                    if eval_string:
                        token_map.append(self.__string_type(eval_string))
                    eval_string = ""

            if eval_sub_string and not (brace or single_quote or double_quote):
                if braced:
                    token_map.append(
                        Token(
                            eval_sub_string,
                            "CODE_BLOCK"
                            if brace_close == "}"
                            else "COLLECTION"
                            if brace_close == "]"
                            else "EXPRESSION",
                        )
                    )
                else:
                    token_map.append(Token(eval_sub_string, "Data_STRING"))
                eval_sub_string = ""

            if brace or single_quote or double_quote:
                if eval_subtoken_string:
                    token_map.append(self.__token_type(eval_subtoken_string))
                    eval_subtoken_string = ""
                if eval_string:
                    token_map.append(self.__string_type(eval_string))
                    eval_string = ""

        if eval_string:
            token_map.append(self.__string_type(eval_string))
        if eval_subtoken_string:
            token_map.append(self.__token_type(eval_subtoken_string))
        if eval_sub_string or brace or single_quote or double_quote:
            raise InvalidTokenErr

        return token_map
