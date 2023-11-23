import os.path
import json

class Plans:
	def __init__(self):
		self.plans = self.load_plans()
	
	@staticmethod
	def load_plans():
		"""Loads plans from plans.json (persistent). Creates plans.json if not found."""
		
		if not os.path.exists("plans.json"):
			open('plans.json', 'x').close()

		with open("plans.json", "r") as json_file:  # https://www.w3schools.com/python/ref_func_open.asp
			try: 
				json_load = json.load(json_file)
			except ValueError: 
				json_load = {}
			finally:
				return json_load

	@staticmethod	
	def add_plan(plan_name, description, location, start_date):
		"""
		Adds plans to plans.json. 
		Halts and returns False if plan_name already exists.
		Otherwise, returns True indicating success.
		"""
		with open("plans.json", "r") as json_file:
			data = json.load(json_file)
		
		if plan_name in data:  # reject, as plan name collides with that of an existing plan
			return False
		
		data[plan_name] = {
			"plan_name" : plan_name,
            "description" : description,
            "location" : location,
            "start_date" : start_date
		}
		with open("plans.json", "w") as json_file:
			json.dump(data, json_file)
		return True

	@staticmethod
	def delete_plan(plan_name):
		"""
		Deletes plan from plans.json. 
		Halts and returns False if plan doesn't exist.
		Otherwise, returns True indicating success.
		"""
		with open("plans.json", "r") as json_file:
			data = json.load(json_file)
		
		if plan_name not in data:
			return False  # reject, as plan name does not match that of an existing plan
		
		del data[plan_name]
		with open("plans.json", "w") as json_file:
			json.dump(data, json_file)
		return True
		

	# @staticmethod
	# def modify_plan(username, field, new_value):
	# 	"""
	# 	Overwrites the value in the field of a user in plans.json.
	# 	Halts and returns False if username is not existing or if the field is not found in plans.json (prevents typo)
	# 	Otherwise, returns True indicating success.
	# 	"""
	# 	with open("plans.json", "r") as json_file:
	# 		data = json.load(json_file)

	# 	# reject if username does not match that of an existing user
	# 	# also reject if field is not already defined in plans.json (prevents typo)
	# 	if username not in data or (field != "username" and field not in data[username]):
	# 		return False

	# 	if field != "username":
	# 		data[username][field] = new_value
	# 	else:  # changing username needs to be handled differently than other fields, as they are on different levels
	# 		data[new_value] = data.pop(username)

	# 	with open("plans.json", "w") as json_file:
	# 		json.dump(data, json_file)
	# 	return True
	
	