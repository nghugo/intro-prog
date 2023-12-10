import os.path
import json

from db_relocate import update_all_plan_values_in_camps
from interface_helper import is_future_date
from camp_modified import Camp

class Plans:
	def __init__(self):
		self.plans = self.load_all_plans()
	
	@staticmethod
	def load_all_plans():
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
	def load_active_plans():
		"""Loads active plans from plans.json (persistent). Creates plans.json if not found."""
		
		if not os.path.exists("plans.json"):
			open('plans.json', 'x').close()

		with open("plans.json", "r") as json_file:  # https://www.w3schools.com/python/ref_func_open.asp
			try: 
				json_load = json.load(json_file)
			except ValueError: 
				json_load = {}
			finally:
				return {key: val for key, val in json_load.items() if val["status"]=="Active"}

	@staticmethod	
	def add_plan(plan_name, description, country, start_date, end_date):
		"""
		Adds plans to plans.json. 
		Halts and returns False if plan_name already exists.
		Otherwise, returns True indicating success.
		"""
		with open("plans.json", "r") as json_file:
			data = json.load(json_file)
		
		if plan_name in data:  # reject, as plan name collides with that of an existing plan
			return False
		
		# Sets status based on end_date
		status = Plans.status_checker(end_date)

		
		data[plan_name] = {
            "description" : description,
            "country" : country,
            "start_date" : start_date,
			"end_date" : end_date,
			"status" : status
		}
		with open("plans.json", "w") as json_file:
			json.dump(data, json_file, indent=2)
		return True


	@staticmethod
	def delete_plan(plan_name, username):
		data = Plans.load_all_plans()
		if plan_name not in data:
			return False
		
		data.pop(plan_name)
		with open('plans.json','w') as file:
			json.dump(data,file,indent=2)
		
		# cascade delete camps of plan
		camps = Camp.loadALLCampData()
		camp_ids_under_plan = [camp_id for camp_id, vals in camps.items() if vals["humanitarian_plan_in"] == plan_name]
		for camp_id in camp_ids_under_plan:
			Camp.delete_camp(camp_id, username)

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
		
		# Checks if new end date set is in the past or future, and updates status accordingly
		if field == "end_date":
			data[plan_name][field] = new_value
			data[plan_name]["status"] = Plans.status_checker(new_value)
			with open("plans.json", "w") as json_file:
				json.dump(data, json_file, indent=2)
			return True

		if field != "plan_name" and field != "end_date":
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
		update_all_plan_values_in_camps(plan_name, new_name)  # also update camps under the plan
		# Open file in write mode and make changes to data
		with open("plans.json", "w") as json_file:
			json.dump(data, json_file, indent=2)
		return True

	def status_checker(end_date):
		status = ""
		if is_future_date(end_date):
			status = "Active"
		else:
			status = "Ended"
		return status

