import json


class CampResources:
	def __init__(self):
		self.resources = self.load_active_resources()

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
	def load_all_resources():
		try:
			with open('camp_resources.json', 'r') as file:
				resources = json.load(file)
		except (FileNotFoundError, ValueError):
			resources = {}
		return resources

	# display resources in a specific camp
	def display_resources(self, camp_id):
		if camp_id in self.resources:
			camp_resources = self.resources[camp_id]
			print(f"Resources for {camp_id}:")
			for resource, amount in camp_resources.items():
				print(f"-> {resource}: {amount}")
			return True # return True when resources are avaliable 
		else:
			return False
	
	# define add_resources 
	def add_resources(self,camp_id,resource_kind,amount):
		if camp_id in self.resources and resource_kind in self.resources[camp_id]:
			self.resources[camp_id][resource_kind] += amount
			self.save_resources()
			return True
		else:
			return False

	# update specific resources in a specfic camp
	def update_resources(self, camp_id, resource_kind, amount):
		if camp_id in self.resources and resource_kind in self.resources[camp_id]:
			self.resources[camp_id][resource_kind] = amount
			self.save_resources()
			return True
		else:
			return False

	# save resources to json
	def save_resources(self):
		with open('camp_resources.json', 'w') as file:
			json.dump(self.resources, file, indent=4)
		return True