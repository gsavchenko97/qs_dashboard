"""
Utility scripts for application and global variables
"""
import os
import re
import json
from typing import Tuple, NoReturn
from pathlib import Path
import sys

import gettext

data_path = os.path.join(
    os.path.dirname(sys.argv[0]), "qs_dashboard", "locales"
)
# data_path = os.path.join(Path(__file__).resolve().parent, 'locales')
gettext.install("qs_dashboard", data_path)
print(data_path)

MAX_USERNAME_LENGTH = 30
MIN_USERNAME_LENGTH = 2

MAX_FIRSTNAME_LENGTH = 30
MIN_FIRSTNAME_LENGTH = 1

MAX_PASSWORD_LENGTH = 30
MIN_PASSWORD_LENGTH = 2

DB_FOLDER = Path(__file__).resolve().parent.parent / ".db"
USERNAME_FILE = "users.json"  # i know that it is not secure
DF_COLUMNS = [
    "measurement_name", "value", "metric", "day"
]
AVAILABLE_METRICS = {
    _("kg"), _("gr"),
    _("mg"), _("ton"),
    _("km"), _("m"),
    _("cm"), _("mm"),
    _("km ** 2"), _("m ** 2"),
    _("cm ** 2"), _("mm ** 2"),
    _("hour"), _("minute"), _("s"), _("ms"),
    _("km ** 3"), _("m ** 3"),
    _("cm ** 3"), _("mm ** 3"), _("liter"),
    _("ruble"), _("dollar"),
    _("euro")
}

PASSWORD_ALLOWED_CHARS = "A-Za-z0-9@#$%^&+="
PASSWORD_REQUIREMENTS = (
    _("Your password must consist of these characters: %s") %
    PASSWORD_ALLOWED_CHARS
    + _("Your password must be at least %s characters long") %
    MIN_PASSWORD_LENGTH
)


def match_username_password(
    username: str,
    password: str,
    db_filename: str = USERNAME_FILE
) -> bool:
    """
    Check whether the user with the given username and password exists
    :param username:
    :param password:
    :param db_filename:
    :return: True if the user exists otherwise False
    """
    username_file = DB_FOLDER / db_filename
    if username_file.exists():
        with open(username_file, "r") as f:
            username2info = json.load(f)
        if username not in username2info:
            return False
        if username2info[username]["password"] == password:
            return True
    return False


def user_exists(username: str, db_filename: str = USERNAME_FILE) -> bool:
    """
    Check whether the user with the given username exists
    :param username: username
    :param db_filename:
    :return: True if the user exists otherwise False
    """
    username_file = DB_FOLDER / db_filename
    if username_file.exists():
        with open(username_file, "r") as f:
            username2info = json.load(f)
        if username in username2info:
            return True
    return False


def create_new_user(
    username: str,
    password: str,
    firstname: str,
    gender: str,
    db_filename: str = USERNAME_FILE,
) -> NoReturn:
    """
    Adds to database a new user with given information
    :param username: username or login
    :param password: password to use in signing process
    :param firstname: firstname of the user
    :param gender: gender of the user
    :param db_filename:
    """
    os.makedirs(DB_FOLDER, exist_ok=True)

    username_file = DB_FOLDER / db_filename

    username2info = dict()
    if username_file.exists():
        with open(username_file, "r") as f:
            username2info = json.load(f)

    assert username not in username2info, _("%s username already exists") % \
        username

    username2info[username] = {
        "password": password,
        "firstname": firstname,
        "gender": gender,
    }
    with open(username_file, "w") as f:
        json.dump(username2info, f)


def delete_user(username: str, db_filename: str = USERNAME_FILE) -> NoReturn:
    """
    Deletes the user from the database
    :param username: username
    :param db_filename: username
    """
    username_file = DB_FOLDER / db_filename

    if not username_file.exists():
        raise FileNotFoundError(f"{username_file}" + "does not exist")

    with open(username_file, "r") as f:
        username2info = json.load(f)

    del username2info[username]

    if len(username2info) == 0:
        os.remove(username_file)
    else:
        with open(username_file, "w") as f:
            json.dump(username2info, f)


def check_password(password: str) -> Tuple[bool, str]:
    """
    Checks the password for the minimum requirements
    :param password: string from user
    :return:
        flag: True if the password is valid
        message: password requirements if it is not valid
    """

    if len(password) < MIN_PASSWORD_LENGTH:
        return (
            False,
            _("Your password must be at least %s "
              "characters long") % MIN_PASSWORD_LENGTH
        )

    if not re.match(rf"^[{PASSWORD_ALLOWED_CHARS}]+$", password):
        return False, PASSWORD_REQUIREMENTS

    return True, ""


def check_username(
    username: str,
    db_filename: str = USERNAME_FILE
) -> Tuple[bool, str]:
    """
    Checks if the given username already exists or it uses incorrect characters
    :param username: string from user
    :param db_filename:
    :return:
        flag: True if the username does not exist and it is correct
        message: what the user must change in the written username
    """

    if user_exists(username, db_filename):
        return (
            False,
            _("This username already exists. "
              "Please try another one.")
        )

    if len(username) < MIN_USERNAME_LENGTH:
        return (
            False,
            _("Your username must be at least %s "
              "characters long") % MIN_USERNAME_LENGTH
        )

    return True, ""


def check_firstname(firstname: str) -> Tuple[bool, str]:
    """
    Checks if the given firstname uses incorrect characters
    :param firstname: string from user
    :return:
        flag: True if the username is correct
        message: what the user must change in the written firstname
    """
    if len(firstname) < MIN_FIRSTNAME_LENGTH:
        return (
            False,
            _("Your first name must be at least %s "
              "characters long") % MIN_FIRSTNAME_LENGTH
        )
    return True, ""
