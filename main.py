from sys import exit
from argparse import ArgumentParser
from interpreter.interpreter import Interpreter

parser = ArgumentParser()

parser.add_argument("-i", "--interactive",
    help="start the interactive session",
    action="store_true"
)

args = parser.parse_args()

if __name__ == '__main__':
    if args.interactive:
        exit(Interpreter().start())
    else:
        print("non interactive sessions not yet implemented")
        exit(1)
