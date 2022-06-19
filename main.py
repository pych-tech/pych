from argparse import ArgumentParser
from sys import exit

from interpreter.interpreter import Interpreter
from modules.utils.syntax_analyzer import postfix_generation


def main() -> int:
    print(postfix_generation("let !(dyn) !(mut) Token = (($&Token)^Expression^Data) "))
    parser = ArgumentParser()

    parser.add_argument(
        "-i", "--interactive", help="start the interactive session", action="store_true"
    )

    args = parser.parse_args()

    if args.interactive:
        return Interpreter(kbd_count_break=True).start()
    else:
        print("non interactive sessions not yet implemented")
        return 1


if __name__ == "__main__":
    exit(main())
