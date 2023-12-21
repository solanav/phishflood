import zstandard
import io
from typing import List, Optional
from credfind.objects import Input, InputType
from random import choice, choices

print("Loading passwords to RAM...")
with open("data/passwords.txt.zst", "rb") as f:
    dctx = zstandard.ZstdDecompressor()
    stream_reader = dctx.stream_reader(f)
    text_stream = io.TextIOWrapper(stream_reader, encoding="latin-1")
    PASSWORDS = [l.replace("\n", "") for l in text_stream if l != ""]
print("Done loading passwords")

print("Loading emails to RAM...")
with open("data/emails.txt.zst", "rb") as f:
    dctx = zstandard.ZstdDecompressor()
    stream_reader = dctx.stream_reader(f)
    text_stream = io.TextIOWrapper(stream_reader, encoding="latin-1")
    EMAILS = [l.replace("\n", "") for l in text_stream if "@" in l]
print("Done loading emails")


def in_any(s: List[str], l: List[Optional[str]]) -> bool:
    """Checks if any of s is in any of the elements of l"""
    for s_ in s:
        if any([s_.lower() in (lo or "").lower() for lo in l]):
            return True

    return False


def fake_username() -> str:
    """Generates a random username"""
    username, _ = tuple(choice(EMAILS).split("@"))

    if len(username) < 5:
        return fake_username()

    return username


def fake_email() -> str:
    """Generates a random email"""
    email_providers = [
        "gmail.com",
        "yahoo.com",
        "hotmail.com",
        "aol.com",
        "msn.com",
        "me.com",
        "yandex.ru",
        "icloud.com",
        "comcast.net",
        "yahoo.co.uk",
        "live.com",
        "free.fr",
        "web.de",
        "att.net",
    ]

    username, provider = tuple(choice(EMAILS).split("@"))

    # Do not repeat the same provider
    if provider in email_providers:
        email_providers.remove(provider)

    return f"{username}@{choice(email_providers)}"


def fake_number(digits: int = 6) -> str:
    """Generates a random number of digits length"""
    return "".join(choices([str(n) for n in range(10)], k=digits))


def fake_password() -> str:
    """Generates a random password"""
    return choice(PASSWORDS)


def fake_dni() -> str:
    """Generates a random DNI"""
    key = "TRWAGMYFPDXBNJZSQVHLCKET"
    mod_key = 23

    nums = "".join(choices([str(n) for n in range(10)], k=8))
    letter = key[int(nums) % mod_key]

    return f"{nums}{letter}"


def fake_letters(len: int) -> str:
    """Generates a random string"""
    LETTERS = "abcdefghijklmnopqrstuvwxyz"
    return "".join(choices([str(n) for n in LETTERS], k=len))


def creds_from_input(inp: Input) -> str:
    # Check by keywords
    text_fields = [inp.name, inp.id_, inp.placeholder]

    if in_any(["email"], text_fields):
        return fake_email()
    elif in_any(["code", "key", "pin"], text_fields):
        return fake_number(6)
    elif in_any(["password"], text_fields):
        return fake_password()
    elif in_any(["user", "uid"], text_fields):
        return fake_username()
    elif in_any(["document", "dni"], text_fields):
        return fake_dni()

    # Check by basic type
    match inp.type_:
        case InputType.EMAIL:
            return fake_email()
        case InputType.PASSWORD:
            return fake_password()
        case InputType.TEL:
            return fake_number(12)

    return fake_letters(10)
