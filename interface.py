from auth import Auth
from user import User

class Interface:
	def __init__(self, user = None, existingUserSet = None):
		self.user = user
		self.terminate = False
	
	def start(self):
		while not self.terminate:
			if not self.user:
				self.promptLogin()
			self.promptOptions()  # prompt corresponding features (add resources, edit names, etc)
	
	@staticmethod
	def inputUntilValid(inputMessage, isValid = lambda x: True, validationMessage = ""):
		print(inputMessage)
		validatedInput = None
		while validatedInput is None:
			candiateInput = input()
			if isValid(candiateInput):
				validatedInput = candiateInput
			else:
				print(validationMessage)
		return validatedInput 
	
	
	def promptLogin(self):
		accountType = self.inputUntilValid(
			inputMessage = "Enter your account type (a for admin, v for volunteer):", 
			isValid = lambda x: x=="a" or x=="v", 
			validationMessage = "Unrecognized input. Please enter a for admin or v for volunteer:"
		)
		username = self.inputUntilValid("Enter your username:")
		password= self.inputUntilValid("Enter your password:")
		
		auth = Auth()
		
		if auth.users and username in auth.users:
			if not auth.users[username]["isActivated"]:
				print("Your account has been deactivated, contact the administrator.")
			else:
				self.user = User(
					username = username, 
					password = password, 
					isAdmin = accountType  == "a"
				)
				print(f"You are now logged in as {self.user.username} ({'admin' if self.user.isAdmin else 'volunteer'})")
		else:
			print("Account not found. Please try again:")
	
	
	def promptOptions(self):
		if self.user:
			if self.user.isAdmin:
				self.promptAdminOptions()
			else:
				self.promptVolunteerOptions()
	
	@staticmethod
	def promptAdminOptions():
		print("Option 1: Exit")
		print("Option 2: Add resources as admin")
		print("Option 3: Remove resources as admin")
		option = input()
		print("Your option has been received")
	
	@staticmethod
	def promptVolunteerOptions():
		print("Option 1: Exit")
		print("Option 2: Volunteer option 1")
		print("Option 3: Volunteer option 2")
		option = input()
		print("Your option has been received")
		
	def promptLogout(user):
		pass
	
	def exit(self, user):
		self.user = None
		self.terminate = True