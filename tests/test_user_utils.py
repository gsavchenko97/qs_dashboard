import pytest

from dashboard.utils.user import check_password


@pytest.fixture
def valid_password():
    return "validpassword"


@pytest.fixture
def short_password():
    return "1"


@pytest.fixture
def invalid_password():
    return "asdf()())()"


@pytest.fixture
def empty_password():
    return ""


def test_check_password_valid_password(valid_password):
    output = check_password(valid_password)
    assert isinstance(output, tuple), "check_password must return a tuple"
    assert len(output) == 2, "check_password must return flag and message as a tuple"
    valid, msg = output
    assert valid is True, f"'{valid_password}' is a valid password, but check_password says it isn't"
    assert isinstance(msg, str), "check_password must return a string as a message"


def test_check_password_short_password(short_password):
    output = check_password(short_password)
    assert isinstance(output, tuple), "check_password must return a tuple"
    assert len(output) == 2, "check_password must return flag and message as a tuple"
    valid, msg = output
    assert valid is False, f"'{short_password}' is a short password, but check_password says it is valid"
    assert isinstance(msg, str), "check_password must return a string as a message"


def test_check_password_invalid_password(invalid_password):
    output = check_password(invalid_password)
    assert isinstance(output, tuple), "check_password must return a tuple"
    assert len(output) == 2, "check_password must return flag and message as a tuple"
    valid, msg = output
    assert valid is False, f"'{invalid_password}' is not a valid password, but check_password says it is"
    assert isinstance(msg, str), "check_password must return a string as a message"


def test_check_password_empty_password(empty_password):
    output = check_password(empty_password)
    assert isinstance(output, tuple), "check_password must return a tuple"
    assert len(output) == 2, "check_password must return flag and message as a tuple"
    valid, msg = output
    assert valid is False, f"'{empty_password}' is not a valid password, but check_password says it is"
    assert isinstance(msg, str), "check_password must return a string as a message"
