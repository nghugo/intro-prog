from datetime import datetime


def input_until_valid(input_message, is_valid=lambda user_input: True, validation_message=""):
    """
    Loops through input() until a valid input is provided.

    Parameters:
    ----------
    input_message: message printed on terminal before input()
    is_valid (optional): validation function that checks if the user_input is valid, returns Boolean
    validation_message (optional): message printed on terminal when invalid input is recevied from current_user
    """
    print(input_message)
    validated_input = None
    while validated_input is None:
        user_input = input()
        if is_valid(user_input):
            validated_input = user_input
        else:
            print(validation_message)
    return validated_input


def is_valid_date(date_input):
    try:
        datetime.strptime(date_input, "%d/%m/%Y")
        return True
    except ValueError:
        return False


def is_validate_password(input_message: str) -> str:
    """
    Validate user's password.

    Parameters:
    ----------
    input_message: str
        The prompt message for the user to input the password.

    Return: str
        The validated password.
    """
    special_symbols = [
        "!",
        "@",
        "#",
        "$",
        "%",
        "^",
        "&",
        "*",
        "(",
        ")",
        "-",
        "_",
        "+",
        "=",
        "~",
        "`",
        ";",
        ":",
        "'",
        '"',
        ",",
        ".",
        "<",
        ">",
        "/",
        "?",
    ]

    while True:
        password = input(input_message)
        if len(password) < 8:
            print("\nPassword must be at least 8 characters long.\n")
        elif not any(char.isdigit() for char in password):
            print("\nPassword must contain at least one digit.\n")
        elif not any(char.isupper() for char in password):
            print("\nPassword must contain at least one uppercase letter.\n")
        elif not any(char in special_symbols for char in password):
            print("\nPassword must contain at least one special symbol.\n")
        else:
            return password


def is_validate_email(input_message: str) -> str:
    """
    Validate user email format.

    Parameters:
    ----------
    :param email_prompt: str
    :return: str
    """
    error_email_message = "Invalid email address. Email must be in xxx@yyy.zzz format with no spaces."

    while True:
        email = (
            input(input_message).strip().lower()
        )
        
        if " " in email or "@" not in email:
            print(f"{error_email_message}")
        else:
            _, domain = email.split('@', 1)
            if '.' not in domain[1:]:
                print(f"{error_email_message}")
            else:
                return email
