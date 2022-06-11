from modules.commands.utils.creator import Creator
from modules.commands.utils.returnable import CommandDone
from modules.stream import evaluate
from modules.utils.extra import TerminateSession
from modules.utils.parsers import Token
from modules.utils.parsers.lexer import Lexer


class Interpreter:
    def __init__(self, kbd_count_break: bool = False) -> None:
        self.EXIT_CODE = 0
        self.kbd_interrupt_count: int = 0
        self.kbd_count_break = kbd_count_break
        self.terminate_session: bool = False
        pass

    def __read_stream(self, prompt: str) -> list[Token]:
        instring = input(prompt)
        return Lexer().lex(instring)

    def __execute_stream(self, token_stream: list[Token]) -> CommandDone:
        self.kbd_interrupt_count = 0
        cmd_out = evaluate(token_stream)
        self.EXIT_CODE = cmd_out.EXIT_CODE
        if cmd_out.terminate_session:
            raise TerminateSession()

        else:
            return cmd_out

    def start(self) -> int:
        try:
            while True:
                token_stream = self.__read_stream("prompt> ")
                print(self.__execute_stream(token_stream).command_output)

        except KeyboardInterrupt:
            self.kbd_interrupt_count += 1
            if self.kbd_interrupt_count == 3 and self.kbd_count_break:
                return 130
            self.start()
        except EOFError:
            return 1
        except TerminateSession:
            return self.EXIT_CODE

        return 0
