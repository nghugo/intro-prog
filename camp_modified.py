
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
	def addCamp(camp_id, location, capacity, humanitarian_plan_in, volunteers_in_charge = None, occupancy = 0):
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
			"occupancy": occupancy,
			"humanitarian_plan_in": humanitarian_plan_in,
			"volunteers_in_charge": volunteers_in_charge if volunteers_in_charge != None else [],
		}

		with open("camps.json", "w") as json_file:
			json.dump(data, json_file, indent=2)
		return True
	

	#edit camp with either id or other attributtes
	@staticmethod
	def delete_camp(camp_id, user):
		# TODO: make sure delete_camp does not appear on volunteer's list of options
		data = Camp.loadCampData()
		if user == "admin":
			if camp_id not in data:
				return False
			else:
				data.pop(camp_id)
				with open('camps.json','w') as file:
					json.dump(data,file,indent=2)
				return True
		else:
			return False


	@staticmethod
	def edit_camp_information_id(camp_id, new_identification, user):
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
	def edit_camp_informationid(camp_id, attribute, new_value, user):
		# TODO: data validation of id,attribute, new_attributes
		"""edit the camp information
				user require to be admin or volunteer in charge.
				:return: boolean value. True if edited, False if not accessible"""
		users = Users.load_users()
		camp_data = Camp.loadCampData()
		if user in users and (user == 'admin' or user in camp_data[camp_id]["volunteers_in_charge"]):
			camp_data[camp_id][attribute] = new_value
			with open('camps.json', 'w') as file:
				json.dump(camp_data, file, indent=2)
			return True
		else:
			return False
	# what is the attribute list? location/capacity/occupancy?

	@staticmethod
	def edit_volunteer(camp_id, volunteer, user, method = "add"):
		# TODO: data validation of id and if for remove method, volunteer should be in list
		"""add volunteer to volunteers_in_charge list
		:parameter: method = "add" or "remove" where add means add volunteer to list and remove means remove volunteer from list"""
		camp_data = Camp.loadCampData()
		if method == "add":
			if user == 'admin':
				volunteer_list = Camp.get_volunteer_list(camp_id)
				volunteer_list.append(volunteer)
				camp_data[camp_id]["volunteers_in_charge"] = volunteer_list
				with open('camps.json', 'w') as file:
					json.dump(camp_data, file, indent=2)
					return True
			else:
				return False
		elif method == "remove":
			if user == 'admin':
				volunteer_list = Camp.get_volunteer_list(camp_id)
				volunteer_list.remove(volunteer)
				camp_data[camp_id]["volunteers_in_charge"] = volunteer_list
				with open('camps.json', 'w') as file:
					json.dump(camp_data, file, indent=2)
				return True
			else:
				return False
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





# Camp.delete_camp('camp1', 'admin')
# camp = Camp('camp1','China',30,"planA",[])
# print(Camp.edit_camp_informationid('camp1','capacity',20,'admin'))







