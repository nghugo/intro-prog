import pandas as pd

from interface_helper import input_until_valid


class InterfaceAdminOptions:
	def __init__(self, users, current_user):
		self.users = users
		self.current_user = current_user


	def execute_option(self, user_option):

		if user_option == "2":
			self.prompt_add_user()
		if user_option == "3":
			self.prompt_delete_user()
		if user_option == "4":
			self.prompt_activate_user()
		if user_option == "5":
			self.prompt_deactivate_user()
		if user_option == "6":
			self.prompt_modify_user()
		if user_option == "7":
			self.list_users()
		if user_option == "8":
			pass  # TODO: implement
		if user_option == "9":
			pass  # TODO: implement
		if user_option == "10":
			pass  # TODO: implement


	def prompt_add_user(self):
		username = input_until_valid(
			input_message="\nEnter the username for the new user:",
			is_valid=lambda user_input: user_input not in self.users.users,
			validation_message="Username already taken. Please enter a different username for the new user"
		)
		password = input_until_valid("Enter the password for the new user:")
		is_admin = input_until_valid(
			input_message="Specify if the new user is an admin (y/n):\n[y] Yes\n[n] No",
			is_valid=lambda user_input: user_input == "y" or user_input == "n",
			validation_message="Unrecognized input. Please specify if the new user is an admin (y/n):\n[y] Yes\n[n] No"
		)
		is_activated = input_until_valid(
			input_message="Specify if the new user is activated (y/n):\n[y] Yes\n[n] No",
			is_valid=lambda user_input: user_input == "y" or user_input == "n",
			validation_message="Unrecognized input. Please specify if the new user is activated (y/n):\n[y] Yes\n[n] No"
		)
		confirm = input_until_valid(
			input_message=f"Please confirm details of the new user (y/n):\n->Username: {username}\n->Password: {password}\n->Is Admin: {"yes" if is_admin else "no"}\n->Is Activated: {"yes" if is_activated else "no"}\n[y] Yes\n[n] No (abort)",
			is_valid=lambda user_input: user_input == "y" or user_input == "n",
			validation_message="Unrecognized input. Please confirm details of the new user (y/n):\n[y] Yes\n[n] No (abort)"
		)
		if confirm == "y":
			success = self.users.add_user(
				username=username, password=password, is_admin=is_admin, is_activated=is_activated)
			if success:
				print(f"Successfully added user {username}")
			else:
				print(f"Failed to add user {username}")
		else:
			print(f"Aborted user addition.")


	def prompt_activate_user(self):
		username = input_until_valid(
			input_message="\nEnter the username of the user to activate or leave empty to abort:",
			is_valid=lambda user_input: user_input in self.users.users or user_input == "",
			validation_message="Username not found. Please enter an existing username or leave empty to abort."
		)
		if username == "":
			print("User activation aborted.")
		else:
			self.users.modify_user(username, "is_activated", True)
			print(f"User {username} has been activated.")


	def prompt_deactivate_user(self):
		username = input_until_valid(
			input_message="\nEnter the username of the user to deactivate or leave empty to abort:",
			is_valid=lambda user_input: user_input in self.users.users or user_input == "",
			validation_message="Username not found. Please enter an existing username or leave empty to abort."
		)
		if username == "":
			print("User deactivation aborted.")
		elif username == self.current_user.username:
			print("You are not allowed to deactivate your own account. User deactivation aborted.")
		else:
			self.users.modify_user(username, "is_activated", False)
			print(f"User {username} has been deactivated.")

	@staticmethod
	def valid_inputs_of_field(field):
		if field in {"is_admin", "is_activated"}:
			return {"True", "False"}

	def prompt_modify_user(self):
		username = input_until_valid(
			input_message="\nEnter the username of the user to modify or leave empty to abort:",
			is_valid=lambda user_input: user_input in self.users.users or user_input == "",
			validation_message="Username not found. Please enter an existing username or leave empty to abort."
		)
		
		if username == "":
			print("User modification aborted.")
			return  # early termination
		
		field = input_until_valid(
			input_message="Enter the field (username/password/is_admin/is_activated) to modify:",
			is_valid=lambda user_input: user_input in {"username", "password", "is_admin", "is_activated", ""},
			validation_message="Unrecognized input. Please enter a valid field (username/password/is_admin/is_activated)."
		)
		if field in {"is_admin", "is_activated"}:
			if username == self.current_user.username:
				print(f"You are not allowed to modify the {field} field of your own account. Modification aborted.")
				return

			value = input_until_valid(
				input_message=f"Specify the new value for the field {field} (t/f):\n[t] True\n[f] False",
				is_valid=lambda user_input: user_input == "t" or user_input == "f",
				validation_message=f"Unrecognized input. Please specify the new value for the field {field} (t/f):\n[t] True\n[f] False"
				)
			value = True if value == "t" else False
		else:
			value = input_until_valid("Enter the new value for the field:")
		# TODO: dynamically check the valid inputs for the field
		# do not allow deactivation or admin disabling of own account

		confirm = input_until_valid(
			input_message=f"Please confirm details of the user modification (y/n):\n->Username: {username}\n->Field: {field}\n->Previous Value: {self.users.users[username][field] if field != "username" else username}\n->New Value: {value}\n[y] Yes\n[n] No (abort)",
			is_valid=lambda user_input: user_input == "y" or user_input == "n",
			validation_message="Unrecognized input. Please confirm details of the user modification (y/n):\n[y] Yes\n[n] No (abort)"
		)
		if confirm == "y":
			# modify persistent store and reload current_user if username matches
			self.users.modify_user(username, field, value)
			if username == self.current_user.username:
				if field == "username":
					self.current_user.set_username(value)
				elif field == "password":
					self.current_user.set_password(value)

			print("Successfully modified user.")
		else:
			print("User modification aborted.")


	def prompt_delete_user(self):

		username = input_until_valid(
			input_message="\nEnter the username of the user to delete or leave empty to abort:",
			is_valid=lambda user_input: user_input in self.users.users or user_input == "",
			validation_message="Username not found. Please enter an existing username or leave empty to abort."
		)
		if username == "":
			print("User deletion aborted.")
		elif username == self.current_user.username:
			print("You are not allowed to delete your own account. User deletion aborted.")
		else:
			self.users.delete_user(username)
			print(f"User {username} has been deleted.")

	def list_users(self):
		print("--- Users are as follows ---")
		users_df = pd.DataFrame.from_dict(self.users.users).transpose()  # using pandas just for pretty print
		print(users_df)
		print("--- End of users list ---")