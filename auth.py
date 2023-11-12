import json

class Auth:
	def __init__(self):
		self.users = self.load_users()  # username: {password: xxx, is_admin: xxx, is_activated: xxx}
	
	
	@staticmethod
	def load_users():  # TODO exception handling
		with open("users.json", "r") as json_file:  # https://www.w3schools.com/python/ref_func_open.asp
			return json.load(json_file)


	@staticmethod	
	def add_user(username, password, is_admin, is_activated):
		
		with open("users.json", "r") as json_file:
			data = json.load(json_file)
		
		if username in data:  # reject, as username collides with that of an existing user
			return False
		
		data[username] = {
			"password": password,
			"is_admin": is_admin,
			"is_activated": is_activated,
		}
		with open("users.json", "w") as json_file:
			json.dump(data, json_file)
		return True


	@staticmethod
	def remove_user(username):

		with open("users.json", "r") as json_file:
			data = json.load(json_file)
		
		if username not in data:
			return False  # reject, as username does not match that of an existing user
		
		del data[username]
		with open("users.json", "w") as json_file:
			json.dump(data, json_file)
		return True
		

	@staticmethod
	def modify_user(username, field, new_value):

		with open("users.json", "r") as json_file:
			data = json.load(json_file)

		if username not in data:
			return False  # reject, as username does not match that of an existing user
			
		data[username][field] = new_value
		with open("users.json", "w") as json_file:
			json.dump(data, json_file)
		return True
	
	