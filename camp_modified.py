
import json
from users import Users

class Camp:
	"""camp is used for store and modify data regard with camps;

	 :parameter:
	 --------------------------------
	 camp_identification(str): refer to camp_1,camp_2,camp_3 (don't overlap even in different humanitarian plan);
	 location(str): detailed location;
	 capacity(int):  flexible and size of the camp which is varied from hundreds to thousands;
	 occupancy(int): current amount of people settled in
	 humanitarian_plan_in: the humanitarian plan that the camp is in;
	 volunteer_in_charge(str_list): a list storing volunteer who in charge of the camp
	 ### notice: if one volunteer can only charge one camp(of his own),
	 I am not sure would it be easier to add attribute in volunteer, since storing list in json is some kinda strange
	"""


	# attributes
		# camp_identification
		# location
		# capacity
		# occupancy
		# humanitarian_plan_in
		# volunteer_in_charge
	
	# NOTE: (consider deleting the constructor) we do not need to set object attributes, since we are using the class entirely as static methods
	# #I am not sure since it seems we can do either object creation or handling the data directively using static method
	# def __init__(self,camp_identification,location,capacity,humanitarian_plan_in,volunteer_in_charge):
	# 	camp_data = Camp.loadCampData()
	# 	self.camp_identification = Camp.validateId(camp_identification,camp_data)
	# 	self.location = location
	# 	self.capacity = capacity
	# 	self.occupancy = 0
	# 	self.humanitarian_plan_in = humanitarian_plan_in
	# 	self.volunteer_in_charge = volunteer_in_charge
	# 	# # add camp
	# 	# if self.camp_identification != None:
	# 	#    self.dumpCampData()

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
	# TODO: 
	def addCamp(camp_identification, location , capacity, humanitarian_plan_in, volunteer_in_charge = None, occupancy = 0):
		"""
		Adds a camp to camps.json. 
		Halts and returns False if camp_identification already exists.
		Otherwise, returns True indicating success.
		"""
		with open("camps.json", "r") as json_file:
			data = json.load(json_file)

		if camp_identification in data:  # reject, as camp_identification collides with that of an existing camp
			return False
		
		data[camp_identification] = {
			"location": location,
			"capacity": capacity,
			"occupancy": occupancy,
			"humanitarian_plan_in": humanitarian_plan_in,
			"volunteer_in_charge": volunteer_in_charge if volunteer_in_charge != None else [],
		}

		with open("camps.json", "w") as json_file:
			json.dump(data, json_file)
		return True

	# NOTE: (consider deleting this method) commented out since we should not print unless we are in the interface, and we don't need a method for a simple key check
	# @staticmethod
	# def validateId(camp_identification, camp_data):
	# 	"""validate the camp_identification"""
	# 	if camp_identification in camp_data:
	# 		print('already exist. please create a new identification of the camp')
	# 		return None
	# 	else:
	# 		return camp_identification

	# NOTE: (consider deleting this method) commented out since this completely overwrites camps.json -> do we want this feature?
	# def dumpCampData(self):
	# 	"""write the new data of the new object into camps.json"""
	# 	json_data = {}
	# 	data = self.__dict__.copy()
	# 	data.pop("camp_identification")
	# 	json_data[self.camp_identification] = data

	# 	with open('camps.json','w') as file:
	# 		json.dump(json_data,file,indent=4)
	# 	return True



	#edit camp with either id or other attributtes
	@staticmethod
	def delete_camp(camp_identification, user):
		data = Camp.loadCampData()
		# TODO: volunteer does not have this function initially. need to decide the account?
		# response to TODO: Simply exclude the delete_camp method in the volunteer's list of options. We do not handle auth in the delete_camp method.
		if user == "admin":
			if camp_identification not in data:
				return False
			else:
				data.pop(camp_identification)
				with open('camps.json','w') as file:
					json.dump(data,file,indent=4)
				return True
		else:
			return False


	@staticmethod
	def edit_camp_information_id(camp_identification, new_identification, user):
		#todo: data validation either here or in admin/volunteer interface
		"""edit the camp_identification
		user require to be admin or volunteer in charge.
		:return: boolean value. True if edited, False if not accessible"""
		users = Users.load_users()
		camp_data = Camp.loadCampData()
		if user in users and (user == 'admin' or user in camp_data[camp_identification]["volunteer_in_charge"]):
			camp_data[new_identification] = camp_data.pop(camp_identification)
			with open('camps.json','w') as file:
				json.dump(camp_data,file)
			return True
		else:
			return False

	@staticmethod
	def edit_camp_information(camp_identification, attribute, new_value, user):
		# TODO: data validation of id,attribute, new_attributes
		"""edit the camp information
				user require to be admin or volunteer in charge.
				:return: boolean value. True if edited, False if not accessible"""
		users = Users.load_users()
		camp_data = Camp.loadCampData()
		if user in users and (user == 'admin' or user in camp_data[camp_identification]["volunteer_in_charge"]):
			camp_data[camp_identification][attribute] = new_value
			with open('camps.json', 'w') as file:
				json.dump(camp_data, file)
			return True
		else:
			return False
	# what is the attribute list? location/capacity/occupancy?

	@staticmethod
	def edit_volunteer(camp_identification, volunteer, user, method = "add"):
		# TODO: data validation of id and if for remove method, volunteer should be in list
		"""add volunteer to volunteer_in_charge list
		:parameter: method = "add" or "remove" where add means add volunteer to list and remove means remove volunteer from list"""
		camp_data = Camp.loadCampData()
		if method == "add":
			if user == 'admin':
				volunteer_list = Camp.get_volunteer_list(camp_identification)
				volunteer_list.append(volunteer)
				camp_data[camp_identification]["volunteer_in_charge"] = volunteer_list
				with open('camps.json', 'w') as file:
					json.dump(camp_data, file)
					return True
			else:
				return False
		elif method == "remove":
			if user == 'admin':
				volunteer_list = Camp.get_volunteer_list(camp_identification)
				volunteer_list.remove(volunteer)
				camp_data[camp_identification]["volunteer_in_charge"] = volunteer_list
				with open('camps.json', 'w') as file:
					json.dump(camp_data, file)
				return True
			else:
				return False
		else:
			print("wrong method")



	@staticmethod
	#getter method
	def get_volunteer_list(camp_identification):
		# TODO: data validation of id
		"""get volunteer list of camp_id"""
		camp_data = Camp.loadCampData()
		volunteer_list = camp_data[camp_identification]["volunteer_in_charge"]
		return volunteer_list





# Camp.delete_camp('camp1', 'admin')
# camp = Camp('camp1','China',30,"planA",[])
# print(Camp.edit_camp_information('camp1','capacity',20,'admin'))







