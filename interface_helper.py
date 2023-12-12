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

def string_to_date(date_input):
	intStr = date_input.replace("/", "")
	return datetime.strptime(intStr, "%d%m%Y").date()

# Returns true when date is after today, returns false if date is today or before.
def is_future_date(date_input):
	date_input_datetime = datetime.strptime(date_input, '%d/%m/%Y')
	return date_input_datetime > datetime.now()

def is_valid_name(name_input):
	if (not isinstance(name_input, str) 
		or not name_input.replace(" ", "").isalpha()
		or name_input.strip() == ""):
		return False
	return True

def input_until_valid_name(input_message, validation_message):
	name = input_until_valid(
		input_message = input_message,
		is_valid = is_valid_name,
		validation_message = validation_message
	)
	return " ".join(name.title().split())  # remove extra whitespaces and Capitalize first letter of each word


# def input_until_valid_password(input_message: str) -> str:
# 	"""
# 	Validate user's password.

# 	Parameters:
# 	----------
# 	input_message: str
# 		The prompt message for the user to input the password.

# 	Return: str
# 		The validated password.
# 	"""
# 	special_symbols = {"!", "@", "#", "$", "%", "^", "&", "*",
# 					   "(", ")", "-", "_", "+", "=", "~", "`", ";", ":", "'", '"', ",", ".", "<", ">", "/", "?", }

# 	while True:
# 		password = input(input_message)
# 		if len(password) < 8:
# 			print("\nPassword must be at least 8 characters long.\n")
# 		elif not any(char.isdigit() for char in password):
# 			print("\nPassword must contain at least one digit.\n")
# 		elif not any(char.isupper() for char in password):
# 			print("\nPassword must contain at least one uppercase letter.\n")
# 		elif not any(char in special_symbols for char in password):
# 			print("\nPassword must contain at least one special symbol.\n")
# 		else:
# 			return password


def is_valid_email(email):
	email = email.strip().lower()
	
	if " " in email or "@" not in email:
		return False
	local, domain = email.split('@', 1)
	
	if not local:
		return False

	if '.' not in domain[1:]:
		return False
	domain_prefix, domain_suffix = domain.split(".", 1)
	
	if not domain_prefix or not domain_suffix:
		return False
	
	return True



def input_until_valid_email(input_email: str) -> str:
	"""
	Validate user email format.

	Parameters:
	----------
	:param email_prompt: str
	:return: str
	"""

	email = input_until_valid(
		input_message = input_email,
		is_valid = is_valid_email,
		validation_message = "Invalid email address. Email must be in xxx@yyy.zzz format with no spaces."
	)
	return email.strip().lower()
