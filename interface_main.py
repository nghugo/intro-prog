from current_user import CurrentUser
from interface_admin_options import InterfaceAdminOptions
from interface_volunteer_options import InterfaceVolunteerOptions
from interface_helper import input_until_valid

from users import Users
from plans import Plans

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
		account_type_or_exit = input_until_valid(
			input_message="\nEnter your account type for login (a/v) or exit (e):\n[a] Admin\n[v] Volunteer\n[e] Exit",
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
					"Your account has been deactivated, contact the administrator.\nYou may try another account.")
			else:
				self.current_user = CurrentUser(
					username = username,
					password = password,
					is_admin = is_admin
				)
		else:
			print("The username or password you entered is incorrect. Please try again:")

	def prompt_options(self):
		"""Provides options available to the currently logged in user"""
		users = Users()
		if self.current_user:
			if users.users[self.current_user.username]["is_admin"]:
				self.prompt_admin_options()
			else:
				self.prompt_volunteer_options()


	def prompt_admin_options(self):  # TODO: implement handling for the other user_option values
		users = Users()
		user_option = input_until_valid(
			# when extending this list, make sure the input message matches the is_valid validation function and the options in interface_admin_options.py
			input_message = f"\nPlease choose an option (logged in as {'admin' if users.users[self.current_user.username]["is_admin"] else 'volunteer'} {self.current_user.username}):\
				\n[1] Log out\
				\n[2] Add user\
				\n[3] Delete user\
				\n[4] Activate user\
				\n[5] Deactivate user\
				\n[6] Modify user\
				\n[7] List all users\
				\n[8] Create new humanitarian plan\
				\n[9] Edit humanitarian camps\
				\n[10] some other command (TODO placeholder)",
			is_valid=lambda user_input: user_input in {"1", "2", "3", "4", "5", "6", "7", "8", "9", "10"},
			validation_message="Unrecognized input. Please choose from the above list."
		)
		users = Users()
		interface_admin_options = InterfaceAdminOptions(users, self.current_user)
		if user_option == "1":
			self.prompt_logout()
		else:
			interface_admin_options.execute_option(user_option)



	def prompt_volunteer_options(self):  # TODO: implement handling for the other user_option values
		users = Users()
		user_option = input_until_valid(
			# when extending this list, make sure the input message matches the is_valid validation function and the options in interface_volunteer_options.py
			# interface_volunteer_options.py currently has not currently been built
			
			input_message = f"\nPlease choose an option (logged in as {'admin' if users.users[self.current_user.username]["is_admin"] else 'volunteer'} {self.current_user.username}):\
				\n[1] Log out\
				\n[2] Modify my details\
				\n[3] List my details\
				\n[4] Volunteer option 1 (TODO placeholder)\
				\n[5] Create refugee profile\
				\n[6] Volunteer option 2 (TODO placeholder)",
			is_valid=lambda user_input: user_input in {"1", "2", "3", "4", "5", "6"},
			validation_message="Unrecognized input. Please choose from the above list."
		)
		users = Users()
		interface_volunteer_options = InterfaceVolunteerOptions(users, self.current_user)
		if user_option == "1":
			self.prompt_logout()
		else:
			interface_volunteer_options.execute_option(user_option)
	
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

		
