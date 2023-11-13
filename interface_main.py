from current_user import CurrentUser
from interface_admin_options import InterfaceAdminOptions
from interface_helper import input_until_valid

from users import Users

class InterfaceMain:

	def __init__(self, current_user = None):
		self.current_user = current_user
		self.terminate = False  # TODO: use this attribute to exit the program


	def start(self):
		"""Starts the user interface and immediately prompts login. Any application logic stems from login."""
		print("\nWelcome to the humanitarian management system.")
		while not self.terminate:
			if not self.current_user:
				self.prompt_login()
			self.prompt_options()  # prompt corresponding features (add resources, edit names, etc)


	def prompt_login(self):
		"""Asks the user to log in, and checks against persisted (existing) users using methods from Users class"""
		accountType = input_until_valid(
			input_message="\nEnter your account type for login (a/v) or exit(e):\n[a] Admin\n[v] Volunteer\n[e] Exit",
			is_valid=lambda user_input: user_input in {"a", "v", "e"},
			validation_message="Unrecognized input. Please enter account type for login (a/v) or exit(e)\n[a] Admin\n[v] Volunteer\n[e] Exit"
		)

		if accountType == "e":
			self.prompt_exit()
			return  # early termination

		username = input_until_valid("Enter your username:")
		password = input_until_valid("Enter your password:")

		users = Users()
		if users.users and username in users.users and users.users[username]['password'] == password:
			if not users.users[username]["is_activated"]:
				print(
					"Your account has been deactivated, contact the administrator.\nYou may try another account.")
			else:
				self.current_user = CurrentUser(
					username=username,
					password=password,
					is_admin=accountType == "a"
				)
		else:
			print("The username or password you entered is incorrect. Please try again:")

	def prompt_options(self):
		"""Provides options available to the currently logged in user"""
		if self.current_user:
			if self.current_user.is_admin:
				self.prompt_admin_options()
			else:
				self.prompt_volunteer_options()


	def prompt_admin_options(self):  # TODO: implement handling for the other user_option values
		user_option = input_until_valid(
			# make sure the input message matches the is_valid validation function and the options in interface_admin_options.py
			input_message = f"\nPlease choose an option (logged in as {'admin' if self.current_user.is_admin else 'volunteer'} {self.current_user.username}):\
				\n[1] Log out\
				\n[2] Add user\
				\n[3] Activate user\
				\n[4] Deactivate user\
				\n[5] Modify user\
				\n[6] Delete user\
				\n[7] some other command (TODO placeholder)\
				\n[8] some other command (TODO placeholder)",
			is_valid=lambda user_input: user_input in {"1", "2", "3", "4", "5", "6"},
			validation_message="Unrecognized input. Please choose from the above list."
		)
		users = Users()
		interface_admin_options = InterfaceAdminOptions(users)
		if user_option == "1":
			self.prompt_logout()
		else:
			interface_admin_options.execute_option(user_option)


	def prompt_volunteer_options(self):  # TODO: implement handling for the other user_option values
		user_option = input_until_valid(
			input_message = f"\nPlease choose an option (logged in as {'admin' if self.current_user.is_admin else 'volunteer'} {self.current_user.username}):\
				\n[1] Log out\
				\n[2] Volunteer option 1 (TODO placeholder)\
				\n[3] Volunteer option 2 (TODO placeholder)",
			is_valid=lambda user_input: user_input in {"1", "2", "3"},
			validation_message="Unrecognized input. Please choose from the above list."
		)
		if user_option == "1":
			self.prompt_logout()
	
	def prompt_logout(self):
		print("\nAre you sure you want to log out?")
		
		user_input = input_until_valid(
			input_message="Please confirm your logout (y/n):\n[y] Yes\n[n] No",
			is_valid=lambda user_input: user_input == "y" or user_input == "n",
			validation_message="Unrecognized input. Please confirm your logout (y/n):\n[y] Yes\n[n] No"
		)

		if user_input == "y":
			print(f"Goodbye {self.current_user.username}! You are now logged out.")
			self.current_user = None
			
	
	def prompt_exit(self):
		print("\nAre you sure you want to exit?")

		user_input = input_until_valid(
			input_message="Please confirm your exit (y/n):\n[y] Yes\n[n] No",
			is_valid=lambda user_input: user_input == "y" or user_input == "n",
			validation_message="Unrecognized input. Please confirm your exit (y/n):\n[y] Yes\n[n] No"
		)

		if user_input == "y":
			print("Thanks for using the humanitarian management system. See you soon.")
			self.current_user = None
			self.terminate = True

		
