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
            "description" : description,
            "location" : location,
            "start_date" : start_date
		}
		with open("plans.json", "w") as json_file:
			json.dump(data, json_file, indent=2)
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
			json.dump(data, json_file, indent=2)
		return True
		

	@staticmethod
	def modify_plan(plan_name, field, new_value):
		"""
		Overwrites the value in the field of a plan_name in plans.json.
		Halts and returns False if username is not existing or if the field is not found in plans.json (prevents typo)
		Otherwise, returns True indicating success.
		"""
		with open("plans.json", "r") as json_file:
			data = json.load(json_file)

		# reject if username does not match that of an existing user
		# also reject if field is not already defined in plans.json (prevents typo)
		if plan_name not in data or (field != "plan_name" and field not in data[plan_name]):
			return False

		if field != "plan_name":
			data[plan_name][field] = new_value
			with open("plans.json", "w") as json_file:
				json.dump(data, json_file, indent=2)
			return True
		# changing plan_name needs to be handled by modify_plan_name()
		else:
			return False
	
	@staticmethod
	def modify_plan_name(plan_name, new_name):
		# Open file in read mode
		with open("plans.json", "r") as json_file:
			data = json.load(json_file)
		# Check that plan_name exists
		if plan_name not in data:
			return False
		# Change plan_name to new name
		data[new_name] = data.pop(plan_name)
		# Open file in write mode and make changes to data
		with open("plans.json", "w") as json_file:
			json.dump(data, json_file, indent=2)
		return True