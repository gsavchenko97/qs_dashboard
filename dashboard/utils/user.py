import os
import re
import json
from typing import Tuple, NoReturn
from pathlib import Path

MAX_USERNAME_LENGTH = 30
MIN_USERNAME_LENGTH = 2

MAX_FIRSTNAME_LENGTH = 30
MIN_FIRSTNAME_LENGTH = 1

MAX_PASSWORD_LENGTH = 30
MIN_PASSWORD_LENGTH = 2

DB_FOLDER = Path(__file__).resolve().parent.parent.parent / ".db"
USERNAME_FILE = "users.json"  # i know that it is not secure
DF_COLUMNS = [
    "measurement_name", "value", "metric", "day"
]
AVAILABLE_METRICS = {
    "kg", "gr",
    "mg", "ton",
    "km", "m",
    "cm", "mm",
    "km ** 2", "m ** 2",
    "cm ** 2", "mm ** 2",
    "hour", "minute", "s", "ms",
    "km ** 3", "m ** 3",
    "cm ** 3", "mm ** 3", "liter",
    "ruble", "dollar",
    "euro"
}

PASSWORD_ALLOWED_CHARS = "A-Za-z0-9@#$%^&+="
PASSWORD_REQUIREMENTS = (
    f"Your password must consist of these characters: "
    f"{PASSWORD_ALLOWED_CHARS} \n"
    f"Your password must be at least {MIN_PASSWORD_LENGTH} characters long"
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

    assert username not in username2info, f"{username} already exists"

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
        raise FileNotFoundError(f"{username_file} does not exist")

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
            f"Your password must be at least {MIN_PASSWORD_LENGTH} "
            f"characters long"
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
            "This username already exists. Please try another one."
        )

    if len(username) < MIN_USERNAME_LENGTH:
        return (
            False,
            f"Your username must be at least {MIN_USERNAME_LENGTH} "
            f"characters long"
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
            f"Your first name must be at least {MIN_FIRSTNAME_LENGTH} "
            f"characters long"
        )
    return True, ""


class User:
    def __init__(self, username: str):
        username_file = DB_FOLDER / USERNAME_FILE

        if not username_file.exists():
            raise FileNotFoundError(f"{username_file} does not exist")

        with open(username_file, "r") as f:
            username2info = json.load(f)

        if username not in username2info:
            raise ValueError(f"'{username}' user does not exists")

        info = username2info[username]
        self.username = username
        self.firstname = info["firstname"]
        self.gender = info["gender"]
