import json

class Auth:
	def __init__(self):
		self.users = self.loadUsers()  # username: {password: xxx, isAdmin: xxx, isActivated: xxx}
	
	@staticmethod
	def loadUsers():  # TODO exception handling
		with open("users.json", "r") as jsonFile:  # https://www.w3schools.com/python/ref_func_open.asp
			users= json.load(jsonFile)
		
	def addVolunteer():
		pass  # TODO json persistence
		# https://stackoverflow.com/questions/13949637/how-to-update-json-file-with-python
	
	def removeVolunteer():
		pass  # TODO json persistence
	
	def deactivateVolunteer():
		pass  # TODO json persistence
	
	def activateVolunteer():
		pass  # TODO json persistence
	
	def addAdmin():
		pass  # TODO json persistence
	
	def removeAdmin():
		pass  # TODO json persistence