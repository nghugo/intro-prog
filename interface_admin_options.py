from interface_helper import input_until_valid

class InterfaceAdminOptions:
	def __init__(self, users):
		self.users = users

	def execute_option(self, user_option):

		# return success and message
		if user_option == "2":
			username = input_until_valid(
				input_message="Enter the username for the new user:",
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
			success = self.prompt_add_user(username, password, is_admin, is_activated)
			if success:
				print(f"Successfully added user {username}")
			else:
				print(f"Failed to add user {username}")


		if user_option == "3":
			self.prompt_activate_user()
		if user_option == "4":
			self.prompt_deactivate_user()
		if user_option == "5":
			self.prompt_modify_user()
		if user_option == "6":
			self.prompt_delete_user()
		if user_option == "7":
			pass  # TODO: implement
		if user_option == "8":
			pass  # TODO: implement

	def prompt_add_user(self, username, password, is_admin, is_activated):
		
		success = self.users.add_user(username=username, password=password, is_admin=is_admin,
							is_activated=is_activated)
		return success

	def prompt_activate_user(self):
		# TODO: for testing only, delete later
		self.users.modify_user("vol4", "is_activated", False)
		print("User has been activated")

	def prompt_deactivate_user(self):
		# TODO: for testing only, delete later
		self.users.modify_user("vol4", "is_activated", True)
		print("User has been deactivated")

	def prompt_modify_user(self):
		# TODO: for testing only, delete later
		self.users.modify_user("vol4", "is_activated", False)
		print("User has been modified")

	def prompt_delete_user(self):
		# TODO: for testing only, delete later
		self.users.delete_user("vol4", "is_activated", False)
		print("User has been deleted")
