from user import User

class Interface:

	def __init__(self, auth, user = None):
		self.auth = auth
		self.user = user
		self.terminate = False  # TODO: use this attribute to exit the program
	
	def start(self):
		while not self.terminate:
			if not self.user:
				self.prompt_login()
			self.prompt_options()  # prompt corresponding features (add resources, edit names, etc)
	
	@staticmethod
	def input_until_valid(input_message, is_valid = lambda x: True, validation_message = ""):
		print(input_message)
		validated_input = None
		while validated_input is None:
			candiate_input = input()
			if is_valid(candiate_input):
				validated_input = candiate_input
			else:
				print(validation_message)
		return validated_input 
	
	def prompt_login(self):
		accountType = self.input_until_valid(
			input_message = "Enter your account type (a or v):\n[a] Admin\n[v] Volunteer", 
			is_valid = lambda x: x=="a" or x=="v", 
			validation_message = "Unrecognized input, please try again (a or v)\n[a] Admin\n[v] Volunteer"
		)
		username = self.input_until_valid("Enter your username:")
		password = self.input_until_valid("Enter your password:")
		
		# auth.add_user("vol4", "112", False, True)
		# auth.remove_user("vol4")
		
		if self.auth.users and username in self.auth.users and self.auth.users[username]['password'] == password:
			if not self.auth.users[username]["is_activated"]:
				print("Your account has been deactivated, contact the administrator.\nYou may try another account.")
			else:
				self.user = User(
					username = username, 
					password = password, 
					is_admin = accountType == "a"
				)
				print(f"You are now logged in as {self.user.username} ({'admin' if self.user.is_admin else 'volunteer'})")
		else:
			print("Account not found or incorrect password. Please try again:")
	
	def prompt_options(self):
		if self.user:
			if self.user.is_admin:
				self.prompt_admin_options()
			else:
				self.prompt_volunteer_options()
	
	@staticmethod
	def prompt_admin_options():
		print("[1] Log out")
		print("[2] Add resources as admin")
		print("[3] Remove resources as admin")
		option = input()
		print("Your option has been received")
	
	@staticmethod
	def prompt_volunteer_options():
		print("[1] Log out")
		print("[2] Volunteer option 1")
		print("[3] Volunteer option 2")
		option = input()
		print("Your option has been received")
		
	def prompt_logout(user):
		pass
	
	def exit(self, user):
		self.user = None
		self.terminate = True