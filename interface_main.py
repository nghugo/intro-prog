from current_user import CurrentUser
from interface_admin_options import InterfaceAdminOptions
from interface_volunteer_options import InterfaceVolunteerOptions
from interface_helper import input_until_valid

from users import Users

class InterfaceMain:

	def __init__(self, current_user = None):
		self.current_user = current_user
		self.terminate = False

	def start(self):
		"""Starts the user interface and immediately prompts login. Any application logic stems from login."""
		print("\nWelcome to the humanitarian management system.")
		while not self.terminate:
			if not self.current_user:
				self.prompt_login()
			self.prompt_options()  # prompt corresponding features (add resources, edit names, etc)


	def prompt_login(self):
		"""Asks the user to log in, and checks against persisted (existing) users using methods from Users class"""
		account_type_or_exit = input_until_valid(
			input_message="\n<login>\nEnter your account type for login (a/v) or exit (e):\n[a] Admin\n[v] Volunteer\n[e] Exit",
			is_valid=lambda user_input: user_input in {"a", "v", "e"},
			validation_message="Unrecognized input. Please enter account type for login (a/v) or exit (e)\n[a] Admin\n[v] Volunteer\n[e] Exit"
		)

		if account_type_or_exit == "e":
			self.prompt_exit()
			return  # early termination

		username = input_until_valid("Enter your username:")
		password = input_until_valid("Enter your password:")
		is_admin = account_type_or_exit=="a"

		users = Users()
		if (users.users  # check that the users dictionary (from persistent storage) is not empty
	  		and username in users.users  # check if the specified username matches a user
			and users.users[username]['password'] == password  # check against password associated with the username
			and users.users[username]['is_admin'] == is_admin  # check if user is of correct type (admin vs volunteer)
		):
			if not users.users[username]["is_activated"]:
				print(
					"\nYour account has been deactivated, contact the administrator.\nYou may try another account.")
			else:
				self.current_user = CurrentUser(
					username = username,
					password = password,
					is_admin = is_admin
				)
				print(
					f"\nLogin successful.")
		else:
			print("\nThe username or password you entered is incorrect. Please try again:")

	def prompt_options(self):
		"""Provides options available to the currently logged in user"""
		users = Users()
		
		if self.current_user:
			if users.users[self.current_user.username]["is_admin"]:
				interface_admin_options = InterfaceAdminOptions(users, self.current_user, self)
				interface_admin_options.prompt_admin_options()
			else:
				interface_volunteer_options = InterfaceVolunteerOptions(users, self.current_user, self)
				interface_volunteer_options.prompt_volunteer_options() 
	
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

		
