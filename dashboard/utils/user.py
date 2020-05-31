

def check_if_user_exists(
        username: str, password: str
) -> bool:
    """
    Check whether the user with the given username and password exists
    :param username:
    :param password:
    :return: True if the user exists otherwise False
    """
    raise NotImplementedError()


def create_new_user(
        username: str,
        password: str,
        first_name: str,
        gender: str
):
    raise NotImplementedError()