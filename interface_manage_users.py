import pandas as pd

from users import Users
from interface_helper import input_until_valid, input_until_valid_email

class InterfaceManageUsers:
	def __init__(self, current_user):
		self.current_user = current_user

	def prompt_admin_options(self):
		option = input_until_valid(
			# when extending this list, make sure the input message matches the is_valid validation function and the options in interface_admin_options.py
			input_message = f"\n<homepage/manage-users>\nPlease choose a user management option below:\
				\n[1] CANCEL\
				\n[2] Add user\
				\n[3] Delete user\
				\n[4] Activate user\
				\n[5] Deactivate user\
				\n[6] Modify user\
				\n[7] List all users",
			is_valid=lambda user_input: user_input.isdigit() and int(user_input) > 0 and int(user_input) <= 7,
			validation_message="Unrecognized input. Please choose from the above list."
		)
		if option == "1":
			return  # option 1 is cancel, so just return
		if option == "2":
			self.prompt_add_user()
		if option == "3":
			self.prompt_delete_user()
		if option == "4":
			self.prompt_activate_user()
		if option == "5":
			self.prompt_deactivate_user()
		if option == "6":
			self.prompt_modify_user()
		if option == "7":
			self.list_users()

	def prompt_add_user(self):
		users = Users.load_users()
		username = input_until_valid(
			input_message="\nEnter the username for the new user:",
			is_valid=lambda user_input: user_input != "" and user_input not in users,
			validation_message="Username cannot be empty or is already taken. Please enter a different username for the new user"
		)
		password = input_until_valid(
			input_message="Enter the password for the new user:",
			is_valid=lambda user_input: user_input != "",
			validation_message="Password cannot be empty"
			)
		email=input_until_valid_email("Enter the email for the new user (format: xxx@yyy.zzz with no spaces):")
		
		phone_number = input_until_valid(
			input_message=f"Enter the new phone number (5+ digits or leave empty):",
			is_valid=lambda user_input: (user_input == "") or (
				user_input.isdigit() and len(user_input) >= 5),
			validation_message=f"Unrecognized input. Please enter the new phone number (5+ digits or leave empty)"
		)
		is_admin = input_until_valid(
			input_message="Specify if the new user is an admin (t/f):\n[t] True\n[f] False",
			is_valid=lambda user_input: user_input == "t" or user_input == "f",
			validation_message="Unrecognized input. Please specify if the new user is an admin (t/f):\n[t] True\n[f] False"
		)
		is_activated = input_until_valid(
			input_message="Specify if the new user is activated (t/f):\n[t] True\n[f] False",
			is_valid=lambda user_input: user_input == "t" or user_input == "f",
			validation_message="Unrecognized input. Please specify if the new user is activated (t/f):\n[t] True\n[f] False"
		)
		confirm = input_until_valid(
			input_message=f"Please confirm details of the new user (y/n):\
				\n->Username: {username}\
				\n->Password: {password}\
				\n->Email: {email}\
				\n->phone_number: {phone_number}\
				\n->Is Admin: {"yes" if is_admin == "t" else "no"}\
				\n->Is Activated: {"yes" if is_activated == "t" else "no"}\
				\n[y] Yes\n[n] No (abort)",
			is_valid=lambda user_input: user_input == "y" or user_input == "n",
			validation_message="Unrecognized input. Please confirm details of the new user (y/n):\n[y] Yes\n[n] No (abort)"
		)
		if confirm == "y":
			success = Users.add_user(
				username=username, password=password, email=email,phone_number=phone_number, is_admin=is_admin == "t", is_activated=is_activated == "f")
			if success:
				print(f"Successfully added user {username}")
			else:
				print(f"Failed to add user {username}")
		else:
			print(f"Aborted user addition.")

	def prompt_activate_user(self):
		users = Users.load_users()
		username = input_until_valid(
			input_message="\nEnter the username of the user to activate or leave empty to abort:",
			is_valid=lambda user_input: user_input in users or user_input == "",
			validation_message="Username not found. Please enter an existing username or leave empty to abort."
		)
		if username == "":
			print("User activation aborted.")
		else:
			Users.modify_user(username, "is_activated", True)
			print(f"User {username} has been activated.")

	def prompt_deactivate_user(self):
		users = Users.load_users()
		username = input_until_valid(
			input_message="\nEnter the username of the user to deactivate or leave empty to abort:",
			is_valid=lambda user_input: user_input in users or user_input == "",
			validation_message="Username not found. Please enter an existing username or leave empty to abort."
		)
		if username == "":
			print("User deactivation aborted.")
		elif username == self.current_user.username:
			print(
				"You are not allowed to deactivate your own account. User deactivation aborted.")
		else:
			Users.modify_user(username, "is_activated", False)
			print(f"User {username} has been deactivated.")

	def prompt_modify_user(self):
		users = Users.load_users()
		username = input_until_valid(
			input_message="\nEnter the username of the user to modify or leave empty to abort:",
			is_valid=lambda user_input: user_input in users or user_input == "",
			validation_message="Username not found. Please enter an existing username or leave empty to abort."
		)

		if username == "":
			print("User modification aborted.")
			return  # early termination

		field = input_until_valid(
			input_message="Enter the field (username/password/email/phone_number/is_admin/is_activated) to modify:",
			is_valid=lambda user_input: user_input in {
				"username", "password", "email", "phone_number", "is_admin", "is_activated"},
			validation_message="Unrecognized input. Please enter a valid field (username/password/email/phone_number/is_admin/is_activated)."
		)
		if field in {"is_admin", "is_activated"}:
			if username == self.current_user.username:
				# do not allow deactivation or admin disabling of own account
				print(f"You are not allowed to modify the {
					  field} field of your own account. Modification aborted.")
				return

			value = input_until_valid(
				input_message=f"Specify the new value for the {field} field (t/f):\n[t] True\n[f] False",
				is_valid=lambda user_input: user_input == "t" or user_input == "f",
				validation_message=f"Unrecognized input. Please specify the new value for the {field} field (t/f):\n[t] True\n[f] False"
			)
			value = True if value == "t" else False
		elif field == "email":
			value=input_until_valid_email("Enter the new email (format: xxx@yyy.zzz with no spaces):")
		elif field == "phone_number":
			value = input_until_valid(
				input_message=f"Specify the new phone number (5+ digits or leave empty)",
				is_valid=lambda user_input: (user_input == "") or (
					user_input.isdigit() and len(user_input) >= 5),
				validation_message=f"Unrecognized input. Please specify the new phone number (5+ digits or leave empty)"
			)
		else:
			value = input_until_valid(f"Enter the new value for the {field} field:")

		confirm = input_until_valid(
			input_message=f"Please confirm details of the user modification (y/n):\n->Username: {username}\n->Field: {field}\n->Previous Value: {
				users[username][field] if field != "username" else username}\n->New Value: {value}\n[y] Yes\n[n] No (abort)",
			is_valid=lambda user_input: user_input == "y" or user_input == "n",
			validation_message="Unrecognized input. Please confirm details of the user modification (y/n):\n[y] Yes\n[n] No (abort)"
		)
		if confirm == "y":
			# modify persistent store and reload current_user if username matches
			Users.modify_user(username, field, value)
			
			print(f"field == 'username'{field == 'username'}")  # TODO: remove DEBUG
			print(f"username == self.current_user.username {username == self.current_user.username}")  # TODO: remove DEBUG

			if field == "username" and username == self.current_user.username:  # if modify username as admin, update current_user instance
				self.current_user.set_username(value)

			print("Successfully modified user.")
		else:
			print("User modification aborted.")

	def prompt_delete_user(self):
		users = Users.load_users()
		username = input_until_valid(
			input_message="\nEnter the username of the user to delete or leave empty to abort:",
			is_valid=lambda user_input: user_input in users or user_input == "",
			validation_message="Username not found. Please enter an existing username or leave empty to abort."
		)
		if username == "":
			print("User deletion aborted.")
		elif username == self.current_user.username:
			print(
				"You are not allowed to delete your own account. User deletion aborted.")
		else:
			Users.delete_user(username)
			print(f"User {username} has been deleted.")

	def list_users(self):
		users = Users.load_users()
		print("--- Users are as follows ---")
		# using pandas just for pretty print
		users_df = pd.DataFrame.from_dict(users).transpose()
		print(users_df)
		print("--- End of users list ---")
		input("Press Enter to continue...")