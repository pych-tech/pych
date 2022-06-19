_OPERATOR_MAP: dict[str, int] = {
    "!": 1,  # Optional
    "|": 2,  # Select any
    "^": 2,  # Select anyone
    "&": 2,  # Select all
}


def postfix_generation(stream: str) -> list[str]:
    eval_stack: list[str] = []
    eval_string: str = ""
    operator_stack: list[str] = []
    for ch in stream:
        op = _OPERATOR_MAP.get(ch)
        if op is not None:
            if eval_string:
                eval_stack.append(eval_string)
                eval_string = ""
            operator_stack.append(ch)
        else:
            if ch == " ":
                if eval_string:
                    eval_stack.append(eval_string)
                    eval_string = ""
            elif ch == "(":
                if eval_string:
                    eval_stack.append(eval_string)
                    eval_string = ""
                operator_stack.append(ch)
            elif ch == ")":
                if eval_string:
                    eval_stack.append(eval_string)
                    eval_string = ""
                while True:
                    if operator_stack and operator_stack[-1] == "(":
                        operator_stack.pop()
                        break
                    elif operator_stack:
                        eval_stack.append(operator_stack.pop())
                if operator_stack and operator_stack[-1] == "!":
                    eval_stack.append(operator_stack.pop())
            else:
                eval_string += ch
    return eval_stack
