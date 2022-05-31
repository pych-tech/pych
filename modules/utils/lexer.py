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
            '_': 'UNDERSCORE',
            ' ': 'SPACE'
        }

    def lex(self, string: str) -> list[tuple[str, str]]:
        evalutated_token_stream: str = ""
        token_map: list[tuple[str, str]] = []
        is_integer: bool = False
        is_decimal: bool = False
        is_string_token: bool = False
        
        for token in string:
        
            if token.isalpha():
                evalutated_token_stream+=token
                is_integer: bool = False
                is_decimal: bool = False
                is_string_token: bool = True
        
            elif token.isdigit():
                evalutated_token_stream+=token
        
                if not (is_string_token or is_decimal):
                    is_integer = True
                else:
                    is_integer = False
        
            else:
                token_property = self.character_map.get(token, 'UNKNOWN')
                if is_string_token:
                    if (token_property == "MINUS"
                        or token_property == "UNDERSCORE"):
                        evalutated_token_stream+=token
                    else:
                        token_stream = ""
        
                        for token_item in evalutated_token_stream:
                            token_stream+=token_item
                        
                        token_map.append((token_stream, 'STRING'))
                        token_map.append((token, token_property))

                        is_string_token = False
                        evalutated_token_stream = ""
                
                elif is_integer:
                    if token_property == 'STOP':
                        evalutated_token_stream+=token
                        is_decimal = True
                        is_integer = False
                
                    else:
                        token_stream = ""
                        for token_item in evalutated_token_stream:
                            token_stream+=token_item
                        
                        token_map.append((token_stream, 'NUMBER'))
                        token_map.append((token, token_property))
                        
                        evalutated_token_stream = ""
                        is_decimal = False
                        is_integer = False
                
                elif is_decimal:
                    token_stream = ""
                    for token_item in evalutated_token_stream:
                        token_stream+=token_item
                    
                    token_map.append((token_stream, 'FLOAT'))
                    token_map.append((token, token_property))
                    
                    is_decimal = False
                    evalutated_token_stream = ""
                
                else:
                    token_map.append((token, token_property))
                    
                    is_integer: bool = False
                    is_decimal: bool = False
                    is_string_token: bool = False
        if evalutated_token_stream:
            token_stream = ""

            for token_item in evalutated_token_stream:
                token_stream+=token_item

            if is_decimal:
                token_map.append((token_stream, 'FLOAT'))

            elif is_string_token:
                token_map.append((token_stream, 'STRING'))

            elif is_integer:
                token_map.append((token_stream, 'NUMBER'))

            else:
                token_map.append((token, 'UNKNOWN'))

            evalutated_token_stream = ""

        token_map[0] = (token_map[0][0], 'STREAM-IDENTIFIER')
        return token_map
