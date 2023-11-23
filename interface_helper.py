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

from datetime import datetime 

def is_valid_date(date_input):
    try:
        datetime.datetime.strptime(date_input, "%d/%m/%Y")
        return True
    except ValueError:
        return False

