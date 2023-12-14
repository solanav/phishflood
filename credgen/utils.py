import zstandard
import io
from typing import List
from credfind.objects import Input, InputType
from random import choice, choices

print("Loading passwords to RAM...")
with open("data/passwords.txt.zst", "rb") as f:
    dctx = zstandard.ZstdDecompressor()
    stream_reader = dctx.stream_reader(f)
    text_stream = io.TextIOWrapper(stream_reader, encoding='latin-1')
    PASSWORDS = [l for l in text_stream if l != ""]
print("Done loading passwords")

print("Loading emails to RAM...")
with open("data/emails.txt.zst", "rb") as f:
    dctx = zstandard.ZstdDecompressor()
    stream_reader = dctx.stream_reader(f)
    text_stream = io.TextIOWrapper(stream_reader, encoding='latin-1')
    EMAILS = [l for l in text_stream if "@" in l]
print("Done loading emails")

def in_any(s: str, l: List[str]) -> bool:
    return any([s in (lo or "") for lo in l])

def fake_username() -> str:
    username, _ = tuple(choice(EMAILS).split("@"))
    
    if len(username) < 5:
        return fake_username()
    
    return username

def fake_email() -> str:
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


def fake_password() -> str:
    return choice(PASSWORDS)

def fake_dni() -> str:
    key = "TRWAGMYFPDXBNJZSQVHLCKET"
    mod_key = 23
    
    nums = ''.join(choices([str(n) for n in range(10)], k=8))
    letter = key[int(nums) % mod_key]
    
    return f"{nums}{letter}"

def fake_random() -> str:
    return "asldkjalskdj"

def creds_from_input(inp: Input) -> str:
    # Check by basic type
    match inp.type_:
        case InputType.EMAIL:
            return fake_email()
        case InputType.PASSWORD:
            return fake_password()
    
    # Check by keywords
    text_fields = [inp.name, inp.id_, inp.placeholder]
    if in_any("email", text_fields):
        return fake_email()
    elif in_any("password", text_fields):
        return fake_password()
    elif in_any("username", text_fields):
        return fake_username()
    
    return fake_random()