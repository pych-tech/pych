from modules.utils.lexer import Lexer

class Interpreter:
    def __init__(self) -> None:
        pass

    def start(self) -> int:
        try:
            while True:
                string_stream = input("prompt> ")
                stream  = Lexer().lex(string_stream)
                if stream[0][0].lower() == "exit":
                    break
        except KeyboardInterrupt:
            self.start()
        except EOFError:
            return 1
        else:
            return 0