def isfloat(string: str) -> bool:
    str_split = string.split('.')
    length: int = len(str_split)
    if 0 < length <= 2:
        for x in str_split:
            if not x.isdecimal():
                return False
        else:
            return True
    else:
        return False

class TerminateSession(SystemExit):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)