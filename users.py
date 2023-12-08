import os.path
import json
import hashlib
import binascii

class Users:
	
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
	def add_user(username, password, fullname, email, phone_number, is_admin, is_activated, salt):
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
			"fullname": fullname,
			"phone_number": phone_number,
			"email": email,
			"is_admin": is_admin,
			"is_activated": is_activated,
			"salt":salt
		}
		with open("users.json", "w") as json_file:
			json.dump(data, json_file, indent=2)
		return True
	
	@staticmethod
	def verify_password(username, password):
		'''
		Verifies if the provided password matches the stored password for the given username.
    	Returns True if the password is correct, otherwise False.
			
		'''
		users = Users.load_users()
		if username in users:
			stored_salt = users[username]["salt"]
			stored_password_hash = users[username]["password"]

			input_password_hash = hashlib.sha256((password + stored_salt).encode('utf-8')).hexdigest()

			return input_password_hash == stored_password_hash
		
		return False


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
			json.dump(data, json_file, indent=2)
		return True
		
	@classmethod
	def modify_user(cls, username, field, new_value):
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
			cls.remap_volunteers_of_camps(username, new_value)  # also cascade update the volunteer list

		with open("users.json", "w") as json_file:
			json.dump(data, json_file, indent=2)
		return True

	@classmethod
	def print_current_user_values(cls, username):
		users = cls.load_users()
		user_obj = users[username]
		print("\nCurrent values of the selected user:")
		print(f"-> username: {username}")
		for field, val in user_obj.items():
			if field == "salt":
				continue
			if field == "password":
				val = "[HIDDEN]"
			print(f"-> {field}: {val} {'(only modifiable by admin via manage users section)' if field in ['is_admin', 'is_activated'] else ''}")
	
		
	@staticmethod
	def remap_volunteers_of_camps(from_volunteer, to_volunteer):
		""" Remaps volunteer value in all camps"""
		with open("camps.json", "r") as camp_json:
			camps = json.load(camp_json)
			for camp_id in camps:
				vic_list = camps[camp_id]["volunteers_in_charge"]
				vic_list = [volunteer if volunteer != from_volunteer else to_volunteer for volunteer in vic_list ]
				camps[camp_id]["volunteers_in_charge"] = vic_list
		with open('camps.json', 'w') as file:
			json.dump(camps, file, indent=2)