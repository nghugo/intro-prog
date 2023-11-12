import json

class Auth:
	def __init__(self):
		self.users = self.load_users()  # username: {password: xxx, is_admin: xxx, is_activated: xxx}
	
	def load_users(self):  # TODO exception handling
		with open("users.json", "r") as jsonFile:  # https://www.w3schools.com/python/ref_func_open.asp
			return json.load(jsonFile)
		
	def add_volunteer():
		pass  # TODO json persistence
		# https://stackoverflow.com/questions/13949637/how-to-update-json-file-with-python
	
	def remove_volunteer():
		pass  # TODO json persistence
	
	def deactivate_volunteer():
		pass  # TODO json persistence
	
	def activate_volunteer():
		pass  # TODO json persistence
	
	def add_admin():
		pass  # TODO json persistence
	
	def remove_admin():
		pass  # TODO json persistence