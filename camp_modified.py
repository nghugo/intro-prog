
import json
from users import Users

class Camp:
	"""camp is used for store and modify data regard with camps;

	 :parameter:
	 --------------------------------
	 camp_id(str): refer to camp_1,camp_2,camp_3 (don't overlap even in different humanitarian plan);
	 location(str): detailed location;
	 capacity(int):  flexible and size of the camp which is varied from hundreds to thousands;
	 occupancy(int): current amount of people settled in
	 humanitarian_plan_in: the humanitarian plan that the camp is in;
	 volunteers_in_charge(str_list): a list storing volunteer who in charge of the camp
	 ### notice: if one volunteer can only charge one camp(of his own),
	 I am not sure would it be easier to add attribute in volunteer, since storing list in json is some kinda strange
	"""


	# attributes
		# camp_id
		# location
		# capacity
		# occupancy (determined by linear scan, not by setting a number)
		# humanitarian_plan_in
		# volunteers_in_charge


	@staticmethod
	def loadCampData():
		"""load all data from camps.json"""
		with open('camps.json', 'r') as file:
			try:
				camp_data = json.load(file)
			except ValueError:
				camp_data = {}
			return camp_data
		
	@staticmethod
	def addCamp(camp_id, location, capacity, humanitarian_plan_in, volunteers_in_charge = None):
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
			"capacity": capacity,
			"humanitarian_plan_in": humanitarian_plan_in,
			"volunteers_in_charge": volunteers_in_charge if volunteers_in_charge != None else [],
		}

		with open("camps.json", "w") as json_file:
			json.dump(data, json_file, indent=2)
		return True
	

	#edit camp with either id or other attributtes
	@staticmethod
	def delete_camp(camp_id, username):
		users = Users.load_users()
		if not users[username]['is_admin']:  # only admin gets to delete camp
			return False
		data = Camp.loadCampData()
		if camp_id not in data:
			return False
		data.pop(camp_id)
		with open('camps.json','w') as file:
			json.dump(data,file,indent=2)
		return True


	@staticmethod
	def edit_camp_id(camp_id, new_identification, user):
		# TODO: data validation either here or in admin/volunteer interface
		"""edit the camp_id
		user require to be admin or volunteer in charge.
		:return: boolean value. True if edited, False if not accessible"""
		users = Users.load_users()
		camp_data = Camp.loadCampData()
		if user in users and (user == 'admin' or user in camp_data[camp_id]["volunteers_in_charge"]):
			camp_data[new_identification] = camp_data.pop(camp_id)
			with open('camps.json','w') as file:
				json.dump(camp_data, file, indent=2)
			return True
		else:
			return False

	@staticmethod
	def edit_camp_details(camp_id, attribute, new_value, user):
		# TODO: data validation of id,attribute, new_attributes
		"""edit the camp information
				user require to be admin or volunteer in charge.
				:return: boolean value. True if edited, False if not accessible"""
		users = Users.load_users()
		camp_data = Camp.loadCampData()

		print("*** DEBUG ***")
		print(f'camp_data[camp_id]["volunteers_in_charge"]: {camp_data[camp_id]["volunteers_in_charge"]}')
		print("*** DEBUG END ***")

		if user in users and (user == 'admin' or user in camp_data[camp_id]["volunteers_in_charge"]):
			camp_data[camp_id][attribute] = new_value
			with open('camps.json', 'w') as file:
				json.dump(camp_data, file, indent=2)
			return True
		else:
			return False
	# what is the attribute list? location/capacity/occupancy?

	@staticmethod
	def edit_volunteer(camp_id, volunteer, username, method = "add"):
		"""add volunteer to volunteers_in_charge list
		:parameter: method = "add" or "remove" where add means add volunteer to list and remove means remove volunteer from list"""
		
		users = Users.load_users()
		camp_data = Camp.loadCampData()
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
		# TODO: data validation of id
		"""get volunteer list of camp_id"""
		camp_data = Camp.loadCampData()
		volunteer_list = camp_data[camp_id]["volunteers_in_charge"]
		return volunteer_list

	@staticmethod
	def load_camps_user_has_access_to(username):
		""" If admin, always allow access
		If volunteer, only allow access if username is in volunteers_in_charge"""
		try:
			with open("camps.json", "r") as camp_json:
				filtered_camps = {}
				camps = json.load(camp_json)
				users = Users.load_users()
				for camp_id, camp_values in camps.items():
					if (users[username]["is_admin"]
		 				or username in camp_values["volunteers_in_charge"]):
						filtered_camps[camp_id] = camp_values
				return filtered_camps
		except FileNotFoundError:
			return {}
	
	@staticmethod
	def user_has_access(camp_id, username):
		users = Users.load_users()
		with open("camps.json", "r") as camp_json:
			camps = json.load(camp_json)
			if camp_id not in camps:
				print("Error: camp_id {camp_id} not in the list of camps {camps}")
				return False
			if users[username]["is_admin"] or username in camps[camp_id]["volunteers_in_charge"]:
				return True
		return False
			






# Camp.delete_camp('camp1', 'admin')
# camp = Camp('camp1','China',30,"planA",[])
# print(Camp.edit_camp_details('camp1','capacity',20,'admin'))







