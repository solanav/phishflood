from credgen.utils import creds_from_input
from credfind.objects import Input, InputType


def test_creds_from_input_email():
    inp = Input(
        name="email", id_="email", placeholder="Enter your email", type_=InputType.TEXT
    )
    result = creds_from_input(inp)
    assert "@" in result


def test_creds_from_input_code():
    inp = Input(name="code", id_="code", placeholder="Enter code", type_=InputType.TEXT)
    result = creds_from_input(inp)
    assert len(result) == 6


def test_creds_from_input_password():
    inp = Input(
        name="password",
        id_="password",
        placeholder="Enter password",
        type_=InputType.PASSWORD,
    )
    result = creds_from_input(inp)
    assert len(result) >= 8


def test_creds_from_input_user():
    inp = Input(
        name="user", id_="user", placeholder="Enter username", type_=InputType.TEXT
    )
    result = creds_from_input(inp)
    assert len(result) >= 5


def test_creds_from_input_document():
    inp = Input(
        name="DNI",
        id_="document",
        placeholder="Enter document number",
        type_=InputType.TEXT,
    )
    result = creds_from_input(inp)
    assert len(result) >= 7


def test_creds_from_input_tel():
    inp = Input(
        name="tel", id_="tel", placeholder="Enter phone number", type_=InputType.TEL
    )
    result = creds_from_input(inp)
    assert len(result) == 12


def test_creds_from_input_default():
    inp = Input(
        name="input", id_="input", placeholder="Enter input", type_=InputType.TEXT
    )
    result = creds_from_input(inp)
    assert len(result) == 10
