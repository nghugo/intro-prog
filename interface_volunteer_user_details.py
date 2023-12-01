from users import Users

from interface_helper import input_until_valid, input_until_valid_email

class InterfaceVolunteerUserDetails:
	
	def __init__(self, current_user):
		self.current_user = current_user

	def prompt_modify_my_details(self):
		users = Users.load_users()
		field = input_until_valid(
			input_message="Enter the field (username/password/email/phone_number) to modify:",
			is_valid=lambda user_input: user_input in {
				"username", "password", "email", "phone_number"},
			validation_message="Unrecognized input. Please enter a valid field (username/password/email/phone_number)."
		)
		if field == "username":
			value = input_until_valid(
				input_message="\nEnter the new username:",
				is_valid=lambda user_input: user_input != "" and user_input not in users,
				validation_message="Username cannot be empty or is already taken. Please enter a different username"
			)
		elif field == "phone_number":
			value = input_until_valid(
				input_message=f"Enter the new phone number (5+ digits or leave empty)",
				is_valid=lambda user_input: (user_input == "") or (
					user_input.isdigit() and len(user_input) >= 5),
				validation_message=f"Unrecognized input. Please enter the new phone number (5+ digits or leave empty)"
			)
		elif field == "email":
			value=input_until_valid_email("Enter the new email (format: xxx@yyy.zzz with no spaces):")
		else:  # field == "password"
			value = input_until_valid(f"Enter the new value for the {field} field:")

		confirm = input_until_valid(
			input_message=f"Please confirm details of your user detail modification (y/n):\n->Field: {field}\n->Previous Value: {users[self.current_user.username][field] if field != "username" else self.current_user.username}\n->New Value: {value}\n[y] Yes\n[n] No (abort)",
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
		print("--- Your details are follows ---")
		print(f'{"username":16}{self.current_user.username}')
		for field, value in users[self.current_user.username].items():
			# print(field, ":", value)
			print(f'{field:16}{value}')
		print("--- End of your details ---")
		input("Press Enter to continue...")

