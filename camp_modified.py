import json

from users import Users
from db_relocate import update_all_camp_values_in_refugees, update_all_camp_values_in_camp_resources
from resource_modified import CampResources
class Camp:
	"""camp is used for store and modify data regard with camps;

	 :parameter:
	 --------------------------------
	 camp_id(str): refer to camp_1,camp_2,camp_3 (don't overlap even in different humanitarian plan);
	 location(str): detailed location;
	 max_capacity(int):  flexible and size of the camp which is varied from hundreds to thousands;
	 humanitarian_plan_in: the humanitarian plan that the camp is in;
	 volunteers_in_charge(str_list): a list storing volunteer who in charge of the camp
	 ### notice: if one volunteer can only charge one camp(of his own),
	 I am not sure would it be easier to add attribute in volunteer, since storing list in json is some kinda strange
	"""


	# attributes
		# camp_id
		# location
		# max_capacity
		# occupancy (determined by linear scan, not by setting a number)
		# humanitarian_plan_in
		# volunteers_in_charge

	@staticmethod
	def loadALLCampData():
		"""load all camps under active/inactive plans from camps.json"""
		
		with open('camps.json', 'r') as file:
			try:
				camp_data = json.load(file)
			except ValueError:
				camp_data = {}
			return camp_data

	@staticmethod
	def loadActiveCampData():
		"""load all camps under active plans from camps.json"""

		with open("plans.json", "r") as json_file:  # https://www.w3schools.com/python/ref_func_open.asp
			try: 
				plans = json.load(json_file)
			except ValueError: 
				plans = {}

		with open('camps.json', 'r') as file:
			try:
				camp_data = json.load(file)
			except ValueError:
				camp_data = {}
			return {key: val for key, val in camp_data.items() if plans[val["humanitarian_plan_in"]]["status"] == "Active"}
		
	@staticmethod
	def addCamp(camp_id, location, max_capacity, humanitarian_plan_in, volunteers_in_charge = None):
		"""
		Adds a camp to camps.json. 
		Halts and returns False if camp_id already exists.
		Otherwise, returns True indicating success.
		"""
		with open("camps.json", "r") as json_file:
			data = json.load(json_file)

		if camp_id in data:  # reject, as camp_id collides with that of an existing camp
			return False
		
		data[camp_id] = {
			"location": location,
			"max_capacity": max_capacity,
			"humanitarian_plan_in": humanitarian_plan_in,
			"volunteers_in_charge": volunteers_in_charge if volunteers_in_charge != None else [],
		}

		with open("camps.json", "w") as json_file:
			json.dump(data, json_file, indent=2)

		#add camp_id to resource:
		with open("camp_resources.json", "r") as json_file:
			data_resource = json.load(json_file)

		if camp_id in data_resource:  # reject, as camp_id collides with that of an existing camp
			return False

		data_resource[camp_id] = {  #set all initial value into zero
			"food_packets": 0,
			"medical_packets": 0,
			"water_packets": 0,
			"shelter_packets": 0,
			"clothing_packets": 0,
			"first_aid_packets": 0,
			"baby_packets": 0,
			"sanitation_packets": 0,
		}

		with open('camp_resources.json', 'w') as json_file:
			json.dump(data_resource, json_file, indent = 2)

		return True
	

	#edit camp with either id or other attributtes
	@staticmethod
	def delete_camp(camp_id, username):
		users = Users.load_users()
		if not users[username]['is_admin']:  # only admin gets to delete camp
			return False
		data = Camp.loadActiveCampData()
		if camp_id not in data:
			return False
		data.pop(camp_id)
		with open('camps.json','w') as file:
			json.dump(data,file,indent=2)
		
		# cascade delete refugees of camp
		with open("refugees.json", "r") as json_file:
			json_load = json.load(json_file)
		refugees = json_load
		refugees_to_pop = []
		for refugee, vals in refugees.items():
			if vals["camp_id"] == camp_id:
				refugees_to_pop.append(refugee)
		for refugee in refugees_to_pop:
			refugees.pop(refugee)
		with open('refugees.json', 'w') as file:
			json.dump(refugees, file, indent=2)

		# cascade delete resources of camp
		data_resource = CampResources.load_ALL_resources()
		#delete resource in data_resource
		if camp_id not in data_resource:
			return False
		data_resource.pop(camp_id)
		with open('camp_resources.json', 'w') as file:
			json.dump(data_resource,file,indent=2)
		return True


	@staticmethod
	def edit_camp_id(camp_id, new_id, username):
		"""edit the camp_id
		user require to be admin or volunteer in charge.
		:return: boolean value. True if edited, False if not accessible"""
		users = Users.load_users()
		camp_data = Camp.loadActiveCampData()
		if username in users and (users[username]['is_admin'] or username in camp_data[camp_id]["volunteers_in_charge"]):
			camp_data[new_id] = camp_data.pop(camp_id)
			with open('camps.json','w') as file:
				json.dump(camp_data, file, indent=2)
			update_all_camp_values_in_refugees(camp_id, new_id)
			update_all_camp_values_in_camp_resources(camp_id, new_id)
			return True
		else:
			return False

	@staticmethod
	def edit_camp_details(camp_id, attribute, new_value, username):
		"""edit the camp information
		user require to be admin or volunteer in charge.
		:return: boolean value. True if edited, False if not accessible"""
		users = Users.load_users()
		camp_data = Camp.loadActiveCampData()

		if username in users and (users[username]['is_admin'] or username in camp_data[camp_id]["volunteers_in_charge"]):
			camp_data[camp_id][attribute] = new_value
			with open('camps.json', 'w') as file:
				json.dump(camp_data, file, indent=2)
			return True
		else:
			return False

	@staticmethod
	def edit_volunteer(camp_id, volunteer, username, method = "add"):
		"""add volunteer to volunteers_in_charge list
		:parameter: method = "add" or "remove" where add means add volunteer to list and remove means remove volunteer from list"""
		
		users = Users.load_users()
		camp_data = Camp.loadActiveCampData()

		if method == "add":
			if not users[username]["is_admin"]:
				return False
			volunteer_list = Camp.get_volunteer_list(camp_id)
			volunteer_list.append(volunteer)
			camp_data[camp_id]["volunteers_in_charge"] = volunteer_list
			with open('camps.json', 'w') as file:
				json.dump(camp_data, file, indent=2)
			return True
			
		elif method == "remove":
			if not users[username]["is_admin"]:
				return False
			volunteer_list = Camp.get_volunteer_list(camp_id)
			volunteer_list.remove(volunteer)
			camp_data[camp_id]["volunteers_in_charge"] = volunteer_list
			with open('camps.json', 'w') as file:
				json.dump(camp_data, file, indent=2)
			return True
			
		else:
			print("wrong method")



	@staticmethod
	#getter method
	def get_volunteer_list(camp_id):
		"""get volunteer list of camp_id"""
		camp_data = Camp.loadActiveCampData()
		volunteer_list = camp_data[camp_id]["volunteers_in_charge"]
		return volunteer_list

	@classmethod
	def load_active_camps_user_has_access_to(cls, username):
		""" If admin, always allow access
		If volunteer, only allow access if username is in volunteers_in_charge"""
		
		camps = cls.loadActiveCampData()
		filtered_camps = {}
		users = Users.load_users()
		for camp_id, camp_values in camps.items():
			if (users[username]["is_admin"]
				or username in camp_values["volunteers_in_charge"]):
				filtered_camps[camp_id] = camp_values
		return filtered_camps
	
	@classmethod
	def load_active_camps_user_has_access_to(cls, username):
		""" If admin, always allow access
		If volunteer, only allow access if username is in volunteers_in_charge"""
		
		camps = cls.loadActiveCampData()
		filtered_camps = {}
		users = Users.load_users()
		for camp_id, camp_values in camps.items():
			if (users[username]["is_admin"]
				or username in camp_values["volunteers_in_charge"]):
				filtered_camps[camp_id] = camp_values
		return filtered_camps

	@classmethod
	def load_ALL_camps_user_has_access_to(cls, username):
		""" If admin, always allow access
		If volunteer, only allow access if username is in volunteers_in_charge"""
		
		camps = cls.loadALLCampData()
		filtered_camps = {}
		users = Users.load_users()
		for camp_id, camp_values in camps.items():
			if (users[username]["is_admin"]
				or username in camp_values["volunteers_in_charge"]):
				filtered_camps[camp_id] = camp_values
		return filtered_camps
		
	
	@classmethod
	def user_has_access(cls, camp_id, username):
		users = Users.load_users()
		camps = cls.loadALLCampData()
		if camp_id not in camps:  # this is to handle deleted camps
			print("Error: camp_id {camp_id} not in the list of camps {camps}")
			return False
		if users[username]["is_admin"] or username in camps[camp_id]["volunteers_in_charge"]:
			return True
		return False




