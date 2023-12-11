from credfind.objects import Input, InputType

def fake_email() -> str:
    return "fakeemail@gmail.com"


def fake_password() -> str:
    return "password123"

def fake_randomw() -> str:
    "asldkjalskdj"

def creds_from_input(inp: Input) -> str:
    match inp.type_:
        case InputType.EMAIL:
            return fake_email()
        case InputType.PASSWORD:
            return fake_password()
        case _:
            return fake_random()