from user import User


class Interface:

	def __init__(self, auth, user=None):
		self.auth = auth
		self.user = user
		self.terminate = False  # TODO: use this attribute to exit the program

		# self.auth.add_user("vol4", "112", False, True)  # TODO: for testing only, remove later
		# self.auth.remove_user("vol4")  # TODO: for testing only, remove later
		# self.auth.modify_user("vol4", "is_admin", True)  # TODO: for testing only, remove later
		# self.auth.modify_user("vol4", "is_activated", False)  # TODO: for testing only, remove later
		# self.auth.modify_user("vol4", "is_admin", False)  # TODO: for testing only, remove later

	def start(self):
		"""Starts the user interface and immediately prompts login. Any application logic stems from login."""
		print("\nWelcome to the humanitarian management system.")
		while not self.terminate:
			if not self.user:
				self.prompt_login()
			self.prompt_options()  # prompt corresponding features (add resources, edit names, etc)

	@staticmethod
	def input_until_valid(input_message, is_valid=lambda user_input: True, validation_message=""):
		"""
		Loops through input() until a valid input is provided.

		Parameters:
		----------
		input_message: message printed on terminal before input()
		is_valid (optional): validation function that checks if the user_input is valid, returns Boolean
		validation_message (optional): message printed on terminal when invalid input is recevied from user
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

	def prompt_login(self):
		"""Asks the user to log in, and checks against persisted (existing) users using methods from Auth class"""
		accountType = self.input_until_valid(
			input_message="\nEnter your account type for login (a/v) or exit(e):\n[a] Admin\n[v] Volunteer\n[e] Exit",
			is_valid=lambda user_input: user_input in {"a", "v", "e"},
			validation_message="Unrecognized input. Please enter account type for login (a/v) or exit(e)\n[a] Admin\n[v] Volunteer\n[e] Exit"
		)

		if accountType == "e":
			self.prompt_exit()
			return  # early termination

		username = self.input_until_valid("Enter your username:")
		password = self.input_until_valid("Enter your password:")

		if self.auth.users and username in self.auth.users and self.auth.users[username]['password'] == password:
			if not self.auth.users[username]["is_activated"]:
				print(
					"Your account has been deactivated, contact the administrator.\nYou may try another account.")
			else:
				self.user = User(
					username=username,
					password=password,
					is_admin=accountType == "a"
				)
		else:
			print("The username or password you entered is incorrect. Please try again:")

	def prompt_options(self):
		"""Provides options available to the currently logged in user"""
		if self.user:
			if self.user.is_admin:
				self.prompt_admin_options()
			else:
				self.prompt_volunteer_options()


	def prompt_admin_options(self):  # TODO: implement handling for the other user_option values
		user_option = self.input_until_valid(
			input_message = f"\nPlease choose an option (logged in as {'admin' if self.user.is_admin else 'volunteer'} {self.user.username}):\
				\n[1] Log out\
				\n[2] Admin option 1 (TODO placeholder)\
				\n[3] Admin option 2 (TODO placeholder)",
			is_valid=lambda user_input: user_input in {"1", "2", "3"},
			validation_message="Unrecognized input. BRUHHHHH"
		)
		if user_option == "1":
			self.prompt_logout()


	def prompt_volunteer_options(self):  # TODO: implement handling for the other user_option values
		user_option = self.input_until_valid(
			input_message = f"\nPlease choose an option (logged in as {'admin' if self.user.is_admin else 'volunteer'} {self.user.username}):\
				\n[1] Log out\
				\n[2] Volunteer option 1 (TODO placeholder)\
				\n[3] Volunteer option 2 (TODO placeholder)",
			is_valid=lambda user_input: user_input in {"1", "2", "3"},
			validation_message="Unrecognized input. BRUHHHHH"
		)
		if user_option == "1":
			self.prompt_logout()
	
	def prompt_logout(self):
		print("\nAre you sure you want to log out?")
		
		user_input = self.input_until_valid(
			input_message="Please confirm your logout (y/n):\n[y] Yes\n[n] No",
			is_valid=lambda user_input: user_input == "y" or user_input == "n",
			validation_message="Unrecognized input. Please confirm your logout (y/n):\n[y] Yes\n[n] No"
		)

		if user_input == "y":
			print(f"Goodbye {self.user.username}! You are now logged out.")
			self.user = None
			
	
	def prompt_exit(self):
		print("\nAre you sure you want to exit?")

		user_input = self.input_until_valid(
			input_message="Please confirm your exit (y/n):\n[y] Yes\n[n] No",
			is_valid=lambda user_input: user_input == "y" or user_input == "n",
			validation_message="Unrecognized input. Please confirm your exit (y/n):\n[y] Yes\n[n] No"
		)

		if user_input == "y":
			print("Thank you for using the humanitarian management system. See you again soon.")
			self.user = None
			self.terminate = True

		
