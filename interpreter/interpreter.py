from modules.utils.lexer import Lexer

class Interpreter:
    def __init__(self) -> None:
        pass

    def start(self) -> int:
        try:
            while True:
                string_stream = input("prompt> ")
                if Lexer().lex(string_stream)[0].token_value.lower() == "exit":
                    break
        except KeyboardInterrupt:
            self.start()
        except EOFError:
            return 1
        else:
            return 0