import os.path
import json

class Users:
	def __init__(self):
		self.users = self.load_users()  # username: {password: xxx, is_admin: xxx, is_activated: xxx}
	
	@staticmethod
	def load_users():
		"""Loads users from users.json (persistent). Creates users.json if not found."""
		
		if not os.path.exists("users.json"):
			open('users.json', 'x').close()

		with open("users.json", "r") as json_file:  # https://www.w3schools.com/python/ref_func_open.asp
			try: 
				json_load = json.load(json_file)
			except ValueError: 
				json_load = {}
			finally:
				return json_load

	@staticmethod
	def add_user(username, password, email, phone_number, is_admin, is_activated):
		"""
		Adds user to users.json. 
		Halts and returns False if username already exists.
		Otherwise, returns True indicating success.
		"""
		with open("users.json", "r") as json_file:
			data = json.load(json_file)
		
		if username in data:  # reject, as username collides with that of an existing user
			return False
		
		data[username] = {
			"password": password,
			"phone_number": phone_number,
			"email": email,
			"is_admin": is_admin,
			"is_activated": is_activated,
		}
		with open("users.json", "w") as json_file:
			json.dump(data, json_file)
		return True

	@staticmethod
	def delete_user(username):
		"""
		Deletes user from users.json. 
		Halts and returns False if username is not existing.
		Otherwise, returns True indicating success.
		"""
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
		"""
		Overwrites the value in the field of a user in users.json.
		Halts and returns False if username is not existing or if the field is not found in users.json (prevents typo)
		Otherwise, returns True indicating success.
		"""
		with open("users.json", "r") as json_file:
			data = json.load(json_file)

		# reject if username does not match that of an existing user
		# also reject if field is not already defined in users.json (prevents typo)
		if username not in data or (field != "username" and field not in data[username]):
			return False

		if field != "username":
			data[username][field] = new_value
		else:  # changing username needs to be handled differently than other fields, as they are on different levels
			data[new_value] = data.pop(username)

		with open("users.json", "w") as json_file:
			json.dump(data, json_file)
		return True
	
	