import pytest
import json

from dashboard.utils.user import (
    check_password, check_username,
    match_username_password, user_exists,
    create_new_user, delete_user,
    DB_FOLDER,
)


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
    assert isinstance(output, tuple), "check_password must return " \
                                      "a tuple"
    assert len(output) == 2, "check_password must return flag " \
                             "and message as a tuple"
    valid, msg = output
    assert valid is True, f"'{valid_password}' is a valid password, " \
                          f"but check_password says it isn't"
    assert isinstance(msg, str), "check_password must return " \
                                 "a string as a message"


def test_check_password_short_password(short_password):
    output = check_password(short_password)
    assert isinstance(output, tuple), "check_password must return a tuple"
    assert len(output) == 2, "check_password must return flag and " \
                             "message as a tuple"
    valid, msg = output
    assert valid is False, f"'{short_password}' is a short password, " \
                           f"but check_password says it is valid"
    assert isinstance(msg, str), "check_password must return " \
                                 "a string as a message"


def test_check_password_invalid_password(invalid_password):
    output = check_password(invalid_password)
    assert isinstance(output, tuple), "check_password must return a tuple"
    assert len(output) == 2, "check_password must return flag and " \
                             "message as a tuple"
    valid, msg = output
    assert valid is False, f"'{invalid_password}' is not a valid password, " \
                           f"but check_password says it is"
    assert isinstance(msg, str), "check_password must return a " \
                                 "string as a message"


def test_check_password_empty_password(empty_password):
    output = check_password(empty_password)
    assert isinstance(output, tuple), "check_password must return a tuple"
    assert len(output) == 2, "check_password must return flag and " \
                             "message as a tuple"
    valid, msg = output
    assert valid is False, f"'{empty_password}' is not a valid password," \
                           f" but check_password says it is"
    assert isinstance(msg, str), "check_password must return a string " \
                                 "as a message"


@pytest.fixture
def empty_username():
    return ""


def test_check_username_empty(empty_username):
    output = check_username(empty_username)
    assert isinstance(output, tuple), "check_username must return a tuple"
    assert len(output) == 2, "check_username must return flag " \
                             "and message as a tuple"
    valid, msg = output
    assert valid is False, f"'{empty_password}' is too short, but " \
                           f"check_username says it is correct"
    assert isinstance(msg, str), "check_username must return a " \
                                 "string as a message"


@pytest.fixture
def test_username():
    return "###TESTUSERNAME###"


@pytest.fixture
def test_password():
    return "mystrongpassword"


@pytest.fixture
def test_firstname():
    return "alex"


@pytest.fixture
def test_gender():
    return "Male"


def test_create_new_user(
    test_username, test_password, test_firstname, test_gender
):
    create_new_user(
        test_username, test_password, test_firstname, test_gender, "test_db"
    )
    db_path = DB_FOLDER / "test_db"
    with open(db_path, "r") as f:
        username2info = json.load(f)
    assert test_username in username2info, f"'{test_username}' was not created"
    u = username2info[test_username]
    assert u["password"] == test_password, "password was saved incorrectly"
    assert u["firstname"] == test_firstname, "firstname was saved incorrectly"
    assert u["gender"] == test_gender, "gender was saved incorrectly"
    delete_user(test_username, "test_db")


def test_delete_user(
    test_username, test_password, test_firstname, test_gender
):
    test_username1 = test_username + "q"
    create_new_user(
        test_username, test_password, test_firstname, test_gender, "test_db"
    )
    create_new_user(
        test_username1, test_password, test_firstname, test_gender, "test_db"
    )

    delete_user(test_username, "test_db")
    db_path = DB_FOLDER / "test_db"
    with open(db_path, "r") as f:
        username2info = json.load(f)
    assert test_username not in username2info, f"'{test_username}' was not " \
                                               f"deleted from db"

    delete_user(test_username1, "test_db")
    assert not db_path.exists(), f"'{test_username1}' was not deleted from db"


def test_user_exists(
    test_username, test_password, test_firstname, test_gender
):
    create_new_user(
        test_username, test_password, test_firstname, test_gender, "test_db"
    )
    assert user_exists(test_username, "test_db")
    delete_user(test_username, "test_db")


def test_match_username_password(
    test_username, test_password, test_firstname, test_gender
):
    create_new_user(
        test_username, test_password, test_firstname, test_gender, "test_db"
    )
    assert match_username_password(test_username, test_password, "test_db")
    delete_user(test_username, "test_db")


def test_check_username(
    test_username, test_password, test_firstname, test_gender
):
    output = check_username(test_username)
    assert isinstance(output, tuple), "check_username must return " \
                                      "a tuple"
    assert len(output) == 2, "check_username must return flag " \
                             "and message as a tuple"
    valid, msg = output
    assert valid is True, f"'{empty_password}' is correct, " \
                          f"but check_username says it isn't"
    assert isinstance(msg, str), "check_username must return " \
                                 "a string as a message"

    create_new_user(
        test_username, test_password, test_firstname, test_gender, "test_db"
    )

    output = check_username(test_username, "test_db")
    assert isinstance(output, tuple), "check_username must return a tuple"
    assert len(output) == 2, "check_username must return flag and " \
                             "message as a tuple"
    valid, msg = output
    assert valid is False, f"'{empty_password}' already exists, " \
                           f"but check_username says it is correct"
    assert isinstance(msg, str), "check_username must return " \
                                 "a string as a message"
    delete_user(test_username, "test_db")
