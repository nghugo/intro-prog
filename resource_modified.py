import json


class CampResources:
	
	
	#thresholds set based on population per day (or could set to per week?)
	#food packets 3 packets per person
	#medical packets 1 pack per person
	#water packets 2 packets per person
	#shelter packets 1 packet per person
	#colthing packets 1 packet per person
	#baby packets (don't set threshold)
	#sanitation packets 2 pack per person
	#class variables
	
	factor_food = 3
	factor_medical = 1
	factor_water = 2
	factor_shelter = 1
	factor_clothing = 1
	factor_sanitation = 2
	warning_days = 1

	def __init__(self):
		self.resources = self.load_ALL_resources()

	@staticmethod
	# load resources from camp_resouces.json
	def load_active_resources():
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
			finally:
				active_camps = {key: val for key, val in camp_data.items() if plans[val["humanitarian_plan_in"]]["status"] == "Active"}

		try:
			with open('camp_resources.json', 'r') as file:
				resources = json.load(file)
		except (FileNotFoundError, ValueError):
			resources = {}
		return {key: val for key, val in resources.items() if key in active_camps}

	@staticmethod
	# load resources from camp_resouces.json
	def load_ALL_resources():
		try:
			with open('camp_resources.json', 'r') as file:
				resources = json.load(file)
		except (FileNotFoundError, ValueError):
			resources = {}
		return resources

	# display active resources in a specific camp
	def display_active_resources(self, camp_id):
		active_resources = self.load_active_resources()
		if camp_id in active_resources:
			camp_resources = active_resources[camp_id]
			print(f"Resources for {camp_id}:")
			for resource, amount in camp_resources.items():
				print(f"-> {resource}: {amount}")
			return True # return True when resources are avaliable 
		return False
	
	# display all resources in a specific camp
	def display_ALL_resources(self, camp_id):
		ALL_resources = self.load_ALL_resources()
		if camp_id in ALL_resources:
			camp_resources = ALL_resources[camp_id]
			print(f"Resources for {camp_id}:")
			for resource, amount in camp_resources.items():
				print(f"-> {resource}: {amount}")
			return True # return True when resources are avaliable 
		return False


	def overwrite_resources_amount(self, camp_id, resource_kind, amount):
		"""Set the amount of a resource to the given value."""
		if camp_id in self.resources and resource_kind in self.resources[camp_id]:
			self.resources[camp_id][resource_kind] = amount
			self.save_resources()
			return True
		return False
	
	def increment_resources_amount(self, camp_id, resource_kind, relative_amount):
		"""Adjust the amount of a resource by a relative amount (positive or negative)."""
		if camp_id in self.resources and resource_kind in self.resources[camp_id]:
			self.resources[camp_id][resource_kind] += relative_amount
			self.save_resources()
			return True
		return False

	# save resources to json
	def save_resources(self):
		with open('camp_resources.json', 'w') as file:
			json.dump(self.resources, file, indent=2)
		return True

	def check_resource_threshold(self,camp_id):
		"""Check if a resource above threshold"""
		if camp_id in self.resources:
			for resource,amount in self.resources[camp_id].items():
				threshold = self.calculate_threshold(resource)
				if amount < threshold:
					print(f"Warning: {resource} is below threshold")
			return True
		return False


	def resource_factor(self):
		"""Return the threshold for a given resource."""
		#thresholds set based on population per day (or could set to per week?)
		#food packets 3 packets per person
		#medical packets 1 pack per person
		#water packets 2 packets per person
		#shelter packets 1 packet per person
		#colthing packets 1 packet per person
		#baby packets (don't set threshold)
		#sanitation packets 2 pack per person

		#here need to fix to based on population 
		factors = {
			"food_packets": self.factor_food,
			"medical_packets": self.factor_medical,
			"water_packets": self.factor_water,
			"shelter_packets": self.factor_shelter,
			"clothing_packets": self.factor_clothing,
			"sanitation_packets": self.factor_sanitation
		}
		return factors
	
	@classmethod   
	def reset_factor(factor_diction):
		CampResources.factor_food = factor_diction["food_packets"]
		CampResources.factor_medical = factor_diction["medical_packets"]
		CampResources.factor_water = factor_diction["water_packets"]
		CampResources.factor_shelter = factor_diction["shelter_packets"]
		CampResources.factor_clothing = factor_diction["clothing_packets"]
		CampResources.factor_sanitation = factor_diction["sanitation_packets"]
		CampResources.warning_days = factor_diction["warning_days"]

dic = {'food_packets': 2, 'medical_packets': 3, 'water_packets': 1, 'shelter_packets': 1, 'clothing_packets': 1, 'sanitation_packets': 1, 'warning_days': 1}

print(CampResources.factor_medical)
#circular import problems