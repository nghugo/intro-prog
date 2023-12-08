import hashlib

from users import Users
from interface_helper import input_until_valid, input_until_valid_email, input_until_valid_name

class InterfaceVolunteerUserDetails:
	
	def __init__(self, current_user):
		self.current_user = current_user

	def prompt_manage_my_details_options(self):
		option = input_until_valid(			
			input_message = f"\n<homepage/manage-own-account>\nPlease choose an option to manage your user account:\
				\n[1] CANCEL\
				\n[2] List my details\
				\n[3] Edit my details",
			is_valid=lambda user_input: user_input.isdigit() and int(user_input) > 0 and int(user_input) <= 3,
			validation_message="Unrecognized input. Please choose from the above list."
		)
		if option == "1":
			return # CANCEL
		if option == "2":
			self.list_my_details()
		if option == "3":
			self.prompt_modify_my_details()

	def prompt_modify_my_details(self):
		Users.print_current_user_values(self.current_user.username)
		users = Users.load_users()
		field = input_until_valid(
			input_message="Enter the field (username/password/fullname/email/phone_number) to modify, or leave empty to abort:",
			is_valid=lambda user_input: user_input == "" or user_input in {"username", "password", "fullname", "email", "phone_number"},
			validation_message="Unrecognized input. Please enter a valid field (username/password/fullname/email/phone_number)."
		)
		if field == "":
			print("User modification aborted.")
			return
		if field == "username":
			value = input_until_valid(
				input_message=f"Enter the new username",
				is_valid=lambda user_input: user_input not in users,
				validation_message=f"Username already taken. Please enter a different username."
			)
		elif field == "phone_number":
			value = input_until_valid(
				input_message=f"Enter the new phone number (5+ digits or leave empty)",
				is_valid=lambda user_input: (user_input == "") or (
					user_input.isdigit() and len(user_input) >= 5),
				validation_message=f"Unrecognized input. Please enter the new phone number (5+ digits or leave empty)"
			)
		elif field == "fullname":
			value = input_until_valid_name(
				input_message = "Please enter your new full name",
				validation_message = "Your full name can only contain letters and spaces. Please re-enter."
				)
		elif field == "email":
			value=input_until_valid_email("Enter the new email (format: xxx@yyy.zzz with no spaces):")
		elif field == "password":
			plain_text_password = input_until_valid(f"Please enter the new password:") 
			salt = users[self.current_user.username]["salt"]
			hashed_password = hashlib.sha256((plain_text_password + salt).encode('utf-8')).hexdigest()
			value = hashed_password
		else:  # field == "password"
			value = input_until_valid(f"Enter the new value for the {field} field:")

		if field == "username":
			prev_value = self.current_user.username
		elif field == "password":
			prev_value = "[HIDDEN]"
		else:
			prev_value = users[self.current_user.username][field]

		confirm = input_until_valid(
			input_message=f"Please confirm details of the user detail modification (y/n):\
				\n->Field: {field}\
				\n->Previous Value: {prev_value}\
				\n->New Value: {value if field != "password" else plain_text_password}\
				\n[y] Yes\
				\n[n] No (abort)",
			is_valid=lambda user_input: user_input == "y" or user_input == "n",
			validation_message="Unrecognized input. Please confirm details of the user modification (y/n):\n[y] Yes\n[n] No (abort)"
		)
		if confirm == "y":
			# modify persistent store and reload current_user if username matches
			Users.modify_user(self.current_user.username, field, value)
			if field == "username":
				self.current_user.set_username(value)

			print("Successfully modified user.")
		else:
			print("User modification aborted.")

	def list_my_details(self):
		users = Users.load_users()
		print("--- Your details are as follows ---")
		print(f'{"username":16}{self.current_user.username}')
		for field, value in users[self.current_user.username].items():
			if field == "salt":
				continue
			if field == "password":
				value = "[HIDDEN]"
			print(f'{field:16}{value}')
		print("--- End of your details ---")
		input("Press Enter to continue...")

