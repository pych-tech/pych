from sys import exit
from modules.utils.lexer import Lexer

def main() -> int:
    try:
        while True:
            string_stream = input("prompt> ")
            stream = Lexer().lex(string_stream)
            if stream[0][0].lower() == "exit":
                break
    except KeyboardInterrupt:
        main()
    except EOFError:
        return 0
    return 0

if __name__ == "__main__":
    exit(main())