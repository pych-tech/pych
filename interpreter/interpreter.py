from modules.commands.utils.returnable import CommandDone
from modules.stream import evaluate
from modules.utils.extra import TerminateSession
from modules.utils.parsers import Token
from modules.utils.parsers.lexer import Lexer


class Interpreter:
    def __init__(self, kbd_count_break: bool = False) -> None:
        self.kbd_interrupt_count: int = 0
        self.kbd_count_break = kbd_count_break
        self.terminate_session: bool = False
        self.previous_command_state: CommandDone | None = None
        pass

    def __read_stream(self, prompt: str) -> list[Token]:
        instring = input(prompt)
        return Lexer().lex(instring)

    def __execute_stream(self, token_stream: list[Token]) -> CommandDone:
        self.kbd_interrupt_count = 0
        return evaluate(
            token_stream,
            command_out=self.previous_command_state,
            show_command_stream=False,
        )

    def start(self) -> int:
        try:
            while True:
                exit_code = (
                    self.previous_command_state.EXIT_CODE
                    if self.previous_command_state is not None
                    else 0
                )
                token_stream = self.__read_stream(f"pych:{exit_code}$> ")
                command_state = self.__execute_stream(token_stream)
                self.previous_command_state = command_state
                if command_state.terminate_session:
                    raise TerminateSession()
                print(command_state.command_output)

        except KeyboardInterrupt:
            self.kbd_interrupt_count += 1
            if self.kbd_interrupt_count == 3 and self.kbd_count_break:
                return 130
            self.start()
        except EOFError:
            return 1
        except TerminateSession:
            return (
                self.previous_command_state.EXIT_CODE
                if self.previous_command_state is not None
                else 0
            )

        return 0
