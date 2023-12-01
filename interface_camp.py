import pandas as pd

import json

from camp_modified import Camp
from users import Users
from interface_helper import input_until_valid

class InterfaceCamp:
	def __init__(self, current_user):
		self.current_user = current_user


	def prompt_admin_options(self):
		"""bring up an admin menu for camp functions """
		# camp_id = Camp()
		option = input_until_valid(
			input_message = f"\n<homepage/manage-camps>\nPlease choose an operation on camps below:\
				\n[1] CANCEL\
				\n[2] Add a camp\
				\n[3] Delete a camp\
				\n[4] Edit details of a camp\
				\n[5] Edit volunteers: add in/remove from a camp\
				\n[6] List all camps\
				\n[7] Display details of a camp (TODO)",
			is_valid=lambda user_input: user_input.isdigit() and int(user_input) > 0 and int(user_input) <= 7,
			validation_message="Unrecognized input. Please choose from the above list."
		)
		if option == "1":
			return  # CANCEL
		if option == "2":
			self.prompt_add_camp()
		if option == "3":
			self.prompt_delete_camp()
		if option == "4":
			self.edit_camp_details()
		if option == "5":
			self.edit_volunteer()
		if option == "6":
			self.prompt_list_all_camps_with_access_rights()
		if option == "7":
			self.prompt_camp_details()  # TODO: unfinished


	def prompt_volunteer_options(self):
		"""bring up a volunteer menu for camp functions """
		# camp_id = Camp()
		option = input_until_valid(
			input_message = f"\n<homepage/manage-camps>\nPlease choose an operation on camps below:\
				\n[1] CANCEL\
				\n[2] Edit details of a camp\
				\n[3] List all camps I have access to\
				\n[4] TODO\
				\n[5] TODO",
			is_valid=lambda user_input: user_input.isdigit() and int(user_input) > 0 and int(user_input) <= 5,
			validation_message="Unrecognized input. Please choose from the above list."
		)
		if option == "1":
			return  # CANCEL
		if option == "2":
			self.edit_camp_details()
		if option == "3":
			self.prompt_list_all_camps_with_access_rights()
		if option == "4":
			pass
		if option == "5":
			pass
		

	def prompt_add_camp(self):
		camp_data = Camp.loadCampData()

		self.print_existing_or_accessible_camps()

		camp_id = input_until_valid(
		input_message = "Please enter the new camp_id",
		is_valid = lambda user_input: user_input != "" and user_input not in camp_data,
		validation_message = "This camp_id already exists or cannot be empty."
	)
	
		location = input_until_valid(
			input_message = "Enter the country this camp is located in",
			is_valid = lambda user_input: user_input != "" and type(user_input) == str,
			validation_message = "This cannot be empty. Please enter the camp location"
		)

		capacity = input_until_valid(
			input_message = "Enter the camp capacity",
			is_valid=lambda user_input: user_input.isdigit() and int(user_input) >= 1,
			validation_message="Camp capacity must be a positive integer. Please re-enter."
		)
		
		humanitarian_plan_in = input_until_valid(
			input_message= "Please enter the humanitarian plan this camp belongs to",
			is_valid = lambda user_input: user_input != "" and type(user_input) == str,
			validation_message="This cannot be empty. Please enter the name of the humanitarian plan"
		)		

		confirm = input_until_valid(
			input_message=f"Please confirm details of the new camp (y/n):\
				\n->Camp ID: {camp_id}\
				\n->Location: {location}\
				\n->Capacity: {capacity}\
				\n->Associated humanitarian plan: {humanitarian_plan_in}\
				\n[y] Yes\
				\n[n] No (abort)",
			is_valid=lambda user_input: user_input == "y" or user_input == "n",
			validation_message="Unrecognized input. Please confirm details of the new camp (y/n):\n[y] Yes\n[n] No (abort)"
		)
		if confirm == "y":
			success = Camp.addCamp(
				camp_id, location , capacity, humanitarian_plan_in)
			if success:
				print(f"Successfully added {camp_id}")
			else:
				print(f"Failed to add {camp_id}")
		else:
			print(f"Aborted camp addition.")


	def prompt_delete_camp(self):

		camp_data = Camp.loadCampData()
		self.print_existing_or_accessible_camps()

		camp_id = input_until_valid(
			input_message= "Please enter the camp_id you would like to delete, or leave empty to abort:",
			is_valid=lambda user_input: user_input =="" or user_input in camp_data,
			validation_message="camp_id does not exist in camp data."
		)
		
		if camp_id == "":
			print("Camp deletion aborted.")
			return

		confirm = input_until_valid(
			input_message=f"Please confirm you want to delete this camp (y/n):\n->camp_id: {camp_id}\n[y] Yes\n[n] No (abort)",
			is_valid=lambda user_input: user_input == "y" or user_input == "n",
			validation_message="Unrecognized input. Please confirm to delete the camp (y/n):\n[y] Yes\n[n] No (abort)"
		)
		if confirm == "n":
			print("Camp deletion aborted.")
			return
		
		test = Camp.delete_camp(camp_id = camp_id, current_user = self.current_user)
		print(f"Successfully deleted {camp_id}" if test else f"Failed to delete {camp_id}")


	def edit_camp_details(self):
		camp_data = Camp.loadCampData()
		
		self.print_existing_or_accessible_camps()

		camp_id = input_until_valid(
				input_message="Please enter the camp_id of the camp you would like to change camp details of, or leave empty to abort",
				is_valid = lambda user_input: user_input == "" or user_input in camp_data,
				validation_message= "The camp_id does not exist. Please re-enter!"
			)   
		
		if camp_id == "":
			print("Camp modification aborted.")
		
		else:
			users = Users.load_users()
			if users[self.current_user.username]["is_admin"] or self.current_user.username == camp_data[camp_id]["volunteers_in_charge"]:
				attribute = input_until_valid(
				input_message="Enter the attribute (camp_id/location/capacity/humanitarian_plan_in/volunteers_in_charge) to modify:",
				is_valid=lambda user_input: user_input in {
				"camp_id", "location", "capacity", "humanitarian_plan_in", "volunteers_in_charge"},
				validation_message="Unrecognized input. Please enter a valid field (camp_id/location/capacity/humanitarian_plan_in/volunteers_in_charge)."
			)

				if attribute == "camp_id":
					new_value = input_until_valid(
					input_message = f"Please enter the new value for {attribute}",
					is_valid=lambda user_input: user_input not in list(camp_data.keys()),
					validation_message=f"This camp_id is alerady taken. Please enter another camp_id."
				)
				
				else:
					print(f"\ncurrent {attribute} value: {camp_data[camp_id][attribute]}\n")
					new_value = input_until_valid(
					input_message=f"Enter the new value for the {attribute}:",
					is_valid=lambda user_input: user_input != camp_data[camp_id][attribute],
					validation_message=f"Please enter the different value of {attribute} from current one."
				)

				confirm = input_until_valid(
					input_message=f"Please confirm you want to change {attribute} from previous value:\n {camp_id if attribute == "camp_id" else camp_data[camp_id][attribute]} to {new_value} \n[y] Yes\n[n] No (abort)",
					is_valid=lambda user_input: user_input == "y" or user_input == "n",
					validation_message="Unrecognized input. Please confirm (y/n):\n[y] Yes\n[n] No (abort)"
				)

				if confirm == "y":
					if attribute == "camp_id":
						test = Camp.edit_camp_details_id(camp_id = camp_id, new_identification = new_value, user = self.current_user.username)
					else:
						test = Camp.edit_camp_details(camp_id=camp_id, attribute=attribute, new_value=new_value, user = self.current_user.username)
					
					if test:
						print(f"You've changed the {attribute} successfully!")
					else:
						print(f'Failed to change {attribute}')

				else:
					print(f"Camp information modification aborted.")
			else:
				print("You are not allowed to edit camp information")
			
	def edit_volunteer(self):
		camp_data = Camp.loadCampData()
		users = Users.load_users()
		if users[self.current_user.username]["is_admin"]:
			self.print_existing_or_accessible_camps()

			camp_id = input_until_valid(
				input_message="Please enter the camp_id of the camp you would like to amend the volunteers in:",
				is_valid=lambda user_input: user_input =="" or user_input in camp_data,
				validation_message="The camp_id you entered does not exist! Please re-enter!"
			)
			# TODO: should add print camp data function here to show volunteers in the camp after entering the camp_id
			if camp_id =="":
				print("abort volunteers change")
			else:
				volunteer_list = Camp.get_volunteer_list(camp_id)
				method = input_until_valid(
				input_message= "Please enter the changing method to volunteers: add/remove:",
				is_valid=lambda user_input: user_input == "add" or user_input == "remove",
				validation_message=f"Please select from add/remove to edit volunteers in {camp_id}. Please re-enter!"
				)				
				print(f"\nexisting volunteers in {camp_id}:{volunteer_list}\n")
				if method == "add":
					volunteer = input_until_valid(
						input_message= f"please enter the volunteer you want to {method} into volunteer list",
						is_valid=lambda user_input: user_input not in camp_data[camp_id]["volunteers_in_charge"],
						validation_message="The volunteer you entered is already in the volunteer list. Please re-enter."
				)
				else:
					volunteer = input_until_valid(
						input_message=f"Please enter the volunteer you want to {method} from volunteer list",
						is_valid=lambda user_input: user_input in camp_data[camp_id]["volunteers_in_charge"],
						validation_message="The volunteer you entered is not in the volunteer list. Please re-enter!"
					)
				confirm = input_until_valid(
					input_message=f"Please confirm you want to {method} the {volunteer} \n[y] Yes\n[n] No (abort)",
					is_valid=lambda user_input: user_input == "y" or user_input == "n",
					validation_message="Unrecognized input. Please confirm (y/n):\n[y] Yes\n[n] No (abort)"
				)
				if confirm == "y":
					test = Camp.edit_volunteer(camp_id=camp_id, volunteer=volunteer, user = self.current_user.username, method = method)
					if test:
						print(f"You have {method} {volunteer} successfully!")
					else:
						print(f"Failed to {method} {volunteer}!")
				else:
					print(f"Aborted {method} volunteer operation")
		else:
			print("You are not allowed to edit volunteer list.")

	def load_camps_with_access_rights(self):
		""" If admin, always allow access
		If volunteer, only allow access if username is in volunteers_in_charge"""
		try:
			with open("camps.json", "r") as camp_json:
				filtered_camps = {}
				camps = json.load(camp_json)
				users = Users.load_users()
				for camp_id, camp_values in camps.items():
					if (users[self.current_user.username]["is_admin"]
		 				or self.current_user.username in camp_values["volunteers_in_charge"]):
						filtered_camps[camp_id] = camp_values
				return filtered_camps
		except FileNotFoundError:
			return {}

	def prompt_list_all_camps_with_access_rights(self):
		users = Users.load_users()
		user_is_admin = users[self.current_user.username]["is_admin"]
		filtered_camps = self.load_camps_with_access_rights()
		print("--- Camps are as follows ---" if user_is_admin else "--- Camps you have access to are as follows ---")
		filtered_camps_df = pd.DataFrame.from_dict(filtered_camps).transpose()  # use pandas for pretty print
		print(filtered_camps_df)
		print("--- End of camps list ---")
		input("Press Enter to continue...")
	
	def prompt_camp_details(self):
		pass
	
	def print_existing_or_accessible_camps(self):
		
		users = Users.load_users()
		is_admin =  users[self.current_user.username]["is_admin"]
		filtered_camps = self.load_camps_with_access_rights()

		message_key = "Existing camp(s):" if is_admin else "Camp(s) you have access to:"
		message_value = ", ".join(list(filtered_camps.keys())) if filtered_camps else "None found"
		print(f"{message_key} {message_value}")

	

		
	
	
	







