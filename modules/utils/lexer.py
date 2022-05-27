class Lexer:
    def __init__(self) -> None:
        self.character_map: dict[str, str] = {
            ';': 'SEMICOLON',
            ':': 'COLON',
            '&': 'AMPERSAND',
            '|': 'PIPE',
            '%': 'PERCENT',
            '@': 'AT',
            '!': 'EXCLAMATION',
            '#': 'POUND',
            '$': 'DOLLAR',
            '^': 'POWER',
            '*': 'ASTERISK',
            '+': 'PLUS',
            '-': 'MINUS',
            '/': 'FORWARDSLASH',
            '\\': 'BACKWARDSLASH',
            '~': 'TILDE',
            '`': 'BACKTICK',
            '=': 'EQUALS',
            '.': 'STOP',
            ',': 'COMMA',
            '?': 'QUESTION',
            '[': 'SQUARE-OPEN',
            ']': 'SQUARE-CLOSE',
            '{': 'BRACE-OPEN',
            '}': 'BRACE-CLOSE',
            '(': 'PAREN-OPEN',
            ')': 'PAREN-CLOSE',
            '>': 'ANGULAR-CLOSE',
            '<': 'ANGULAR-OPEN',
            '"': 'DOUBLE-QUOTE',
            '\'': 'SINGLE-QUOTE',
            '_': 'UNDERSCORE'
        }
    def lex(self, string: str) -> list[tuple[str, str]]:
        character_list: list[tuple[str, str]] = []
        token_map: list[tuple[str, str]] = []
        is_integer: bool = False
        is_decimal: bool = False
        is_string_token: bool = False
        for token in string:
            if token.isalpha():
                character_list.append((token, 'CHAR'))
                is_integer: bool = False
                is_decimal: bool = False
                is_string_token: bool = True
            elif token.isdigit():
                character_list.append((token, 'DIGIT'))
                if not (is_string_token and is_decimal):
                    is_integer = True
                else:
                    is_integer = False
            else:
                token_property = self.character_map.get(token)
                if is_string_token:
                    token_stream = ""
                    for token_item, _ in character_list:
                        token_stream+=token_item
                    token_map.append((token_stream, 'STRING'))
                    token_map.append((token, self.character_map.get(token)))
                    is_string_token = False
                    character_list.clear()
                elif is_integer:
                    if token_property == 'STOP':
                        character_list.append((token, token_property))
                        is_decimal = True
                        is_integer = False
                    else:
                        token_stream = ""
                        for token_item, _ in character_list:
                            token_stream+=token_item
                        token_map.append((token_stream, 'NUMBER'))
                        token_map.append((token, token_property))
                        character_list.clear()
                        is_decimal = False
                        is_integer = False
                elif is_decimal:
                    token_stream = ""
                    for token_item, _ in character_list:
                        token_stream+=token_item
                    token_map.append((token_stream, 'FLOAT'))
                    token_map.append((token, token_property))
                    is_decimal = False
                    character_list.clear()
                else:
                    token_map.append((token, token_property if token_property else 'UNKNOWN'))
                    is_integer: bool = False
                    is_decimal: bool = False
                    is_string_token: bool = False
        if character_list:
            token_stream = ""
            for token_item, _ in character_list:
                token_stream+=token_item
            if is_decimal:
                token_map.append((token_stream, 'FLOAT'))
            elif is_string_token:
                token_map.append((token_stream, 'STRING'))
            elif is_integer:
                token_map.append((token_stream, 'NUMBER'))
            else:
                token_map.append((token, 'UNKNOWN'))
            character_list.clear()
        token_map[0] = (token_map[0][0], 'STREAM-IDENTIFIER')
        return token_map
