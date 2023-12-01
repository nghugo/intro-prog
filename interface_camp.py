import json

from camp_modified import Camp
from users import Users
from interface_helper import input_until_valid

class InterfaceCamp:
	def __init__(self, current_user):
		self.current_user = current_user


	def prompt_admin_options(self):
		"""bring up an admin menu for camp functions """
		# camp_identification = Camp()
		option = input_until_valid(
			input_message = f"\n<homepage/manage-camps>\nPlease choose an operation on camps below:\
				\n[1] CANCEL\
				\n[2] Add camp\
				\n[3] Delete camp\
				\n[4] Edit camp information\
				\n[5] Edit volunteers: add in/remove from a specific camp",
			is_valid=lambda user_input: user_input.isdigit() and int(user_input) > 0 and int(user_input) <= 5,
			validation_message="Unrecognized input. Please choose from the above list."
		)
		if option == "1":
			return  # CANCEL
		if option == "2":
			self.add_camp()
		if option == "3":
			self.delete_camp()
		if option == "4":
			self.Edit_camp_information()
		if option == "5":
			self.Edit_volunteer()
		

	def add_camp(self):
		camp_data = Camp.loadCampData()

		print(f"Existing camp(s): {", ".join(list(camp_data.keys())) if camp_data else "None found"}")

		camp_identification = input_until_valid(
		input_message = "Please enter the new CampID",
		is_valid = lambda user_input: user_input != "" and user_input not in camp_data,
		validation_message = "CampID cannot be empty or this campID already exists."
	)
	
		location = input_until_valid(
			input_message = "Enter the country this camp is located in",
			is_valid = lambda user_input: user_input != "" and type(user_input) == str,
			validation_message = "This cannot be empty. Please enter the camp location"
		)

		capacity = input_until_valid(
			input_message = "Enter the camp capacity",
			is_valid=lambda user_input: user_input != "" and type(user_input) == str,
			validation_message="This cannot be empty! Please enter the integer as camp capacity!"
		)
		
		humanitarian_plan_in = input_until_valid(
			input_message= "Please enter the humanitarian plan this camp belongs to",
			is_valid = lambda user_input: user_input != "" and type(user_input) == str,
			validation_message="This cannot be empty. Please enter the name of the humanitarian plan"
		)

		# NOTE: commented out (remove this field) because we do not need to enforce that a camp has a volunteer upfront
		# volunteer_in_charge = input_until_valid(
		#     input_message="Enter the volunteer name who charges this camp",
		#     is_valid=lambda user_input: user_input!="",
		#     validation_message="volunteer does not exist or volunteer is in other camps! Please retry."
		# )
		# TODO: refer volunteerlist to add more deciding criteria in is_valid
		
		confirm = input_until_valid(
			input_message=f"Please confirm details of the new camp (y/n):\n->CampID: {camp_identification}\n->location: {location}\n->capacity: {capacity}\n->in {humanitarian_plan_in} humanitarian plan\n[y] Yes\n[n] No (abort)",
			is_valid=lambda user_input: user_input == "y" or user_input == "n",
			validation_message="Unrecognized input. Please confirm details of the new camp (y/n):\n[y] Yes\n[n] No (abort)"
		)
		if confirm == "y":
			success = Camp.addCamp(
				camp_identification, location , capacity, humanitarian_plan_in)
			if success:
				print(f"Successfully added {camp_identification}")
			else:
				print(f"Failed to add {camp_identification}")
		else:
			print(f"Aborted camp addition.")


	def delete_camp(self):
		with open("users.json", "r") as json_file:
			data = json.load(json_file)

		username = self.current_user.username
		if data[username]['is_admin']:
			user = "admin"
		else:
			user != "admin"

		camp_data = Camp.loadCampData()
		print(f"Existing camp(s): {", ".join(list(camp_data.keys())) if camp_data else "None found"}")

		camp_identification = input_until_valid(
			input_message= "Please enter the campID you would like to delete, or leave empty to abort:",
			is_valid=lambda user_input: user_input =="" or user_input in camp_data,
			validation_message="CampID does not exist in camp data."
		)
		if camp_identification == "":
			print("Camp deletion aborted.")

		else:
			confirm = input_until_valid(
			input_message=f"Please confirm you want to delete this camp (y/n):\n->CampID: {camp_identification}\n[y] Yes\n[n] No (abort)",
			is_valid=lambda user_input: user_input == "y" or user_input == "n",
			validation_message="Unrecognized input. Please confirm to delete the camp (y/n):\n[y] Yes\n[n] No (abort)"
		)
			if confirm == "y":
				test = Camp.delete_camp(camp_identification = camp_identification, user = self.current_user.username)
				if test: 
					print(f'Successfully delete {camp_identification}')
				else: 
					print(f'Failed to delete {camp_identification} as {camp_identification} not in camp list')
			else:
				print(f"Aborted delete this camp.")


	def Edit_camp_information(self):
		camp_data = Camp.loadCampData()
		
		print(f"Existing camp(s): {", ".join(list(camp_data.keys())) if camp_data else "None found"}")

		camp_identification = input_until_valid(
				input_message="Please enter the campID of the camp you would like to change camp details of, or leave empty to abort",
				is_valid = lambda user_input: user_input == "" or user_input in camp_data,
				validation_message= "The campID does not exist. Please re-enter!"
			)   
		
		if camp_identification == "":
			print("Camp modification aborted.")
		
		else:
			users = Users.load_users()
			if users[self.current_user.username]["is_admin"] or self.current_user.username == camp_data[camp_identification]["volunteer_in_charge"]:
				attribute = input_until_valid(
				input_message="Enter the attribute (camp_identification/location/capacity/humanitarian_plan_in/volunteer_in_charge) to modify:",
				is_valid=lambda user_input: user_input in {
				"camp_identification", "location", "capacity", "humanitarian_plan_in", "volunteer_in_charge"},
				validation_message="Unrecognized input. Please enter a valid field (camp_identification/location/capacity/humanitarian_plan_in/volunteer_in_charge)."
			)

				if attribute == "camp_identification":
					
					new_value = input_until_valid(
					input_message = f"Please enter the new value for {attribute}",
					is_valid=lambda user_input: user_input not in list(camp_data.keys()),
					validation_message="Please enter the new campID different from current one."
				)
				
				else:
					print(f"\ncurrent {attribute} value: {camp_data[camp_identification][attribute]}\n")
					new_value = input_until_valid(
					input_message=f"Enter the new value for the {attribute}:",
					is_valid=lambda user_input: user_input != camp_data[camp_identification][attribute],
					validation_message=f"Please enter the different value of {attribute} from current one."
				)

				confirm = input_until_valid(
					input_message=f"Please confirm you want to change {attribute} from previous value:\n {camp_identification if attribute == "camp_identification" else camp_data[camp_identification][attribute]} to {new_value} \n[y] Yes\n[n] No (abort)",
					is_valid=lambda user_input: user_input == "y" or user_input == "n",
					validation_message="Unrecognized input. Please confirm (y/n):\n[y] Yes\n[n] No (abort)"
				)

				if confirm == "y":
					if attribute == "camp_identification":
						test = Camp.edit_camp_information_id(camp_identification = camp_identification, new_identification = new_value, user = self.current_user.username)
					else:
						test = Camp.edit_camp_information(camp_identification=camp_identification, attribute=attribute, new_value=new_value, user = self.current_user.username)
					
					if test:
						print(f"You've changed the {attribute} successfully!")
					else:
						print(f'Failed to change {attribute}')

				else:
					print(f"Camp information modification aborted.")
			else:
				print("You are not allowed to edit camp information")
			
	def Edit_volunteer(self):

		camp_data = Camp.loadCampData()

		users = Users.load_users()

		if users[self.current_user.username]["is_admin"]:
		  
			print(f"Existing camp(s): {", ".join(list(camp_data.keys())) if camp_data else "None found"}")

			camp_identification = input_until_valid(
				input_message="Please enter the campID of the camp you would like to amend the volunteers in:",
				is_valid=lambda user_input: user_input =="" or user_input in camp_data,
				validation_message="The campID you entered does not exist! Please re-enter!"
			)
			# TODO: should add print camp data function here to show volunteers in the camp after entering the campID
			if camp_identification =="":
				print("abort volunteers change")

			else:
				volunteer_list = Camp.get_volunteer_list(camp_identification)
				
				method = input_until_valid(
				input_message= "Please enter the changing method to volunteers: add/remove:",
				is_valid=lambda user_input: user_input == "add" or user_input == "remove",
				validation_message=f"Please select from add/remove to edit volunteers in {camp_identification}. Please re-enter!"
				)
				
				print(f"\nexisting volunteers in {camp_identification}:{volunteer_list}\n")

				if method == "add":
					volunteer = input_until_valid(
						input_message= f"please enter the volunteer you want to {method} into volunteer list",
						is_valid=lambda user_input: user_input not in camp_data[camp_identification]["volunteer_in_charge"],
						validation_message="The volunteer you entered is already in the volunteer list. Please re-enter."
				)
				else:
					volunteer = input_until_valid(
						input_message=f"Please enter the volunteer you want to {method} from volunteer list",
						is_valid=lambda user_input: user_input in camp_data[camp_identification]["volunteer_in_charge"],
						validation_message="The volunteer you entered is not in the volunteer list. Please re-enter!"
					)
   
				confirm = input_until_valid(
					input_message=f"Please confirm you want to {method} the {volunteer} \n[y] Yes\n[n] No (abort)",
					is_valid=lambda user_input: user_input == "y" or user_input == "n",
					validation_message="Unrecognized input. Please confirm (y/n):\n[y] Yes\n[n] No (abort)"
				)

				if confirm == "y":
					test = Camp.edit_volunteer(camp_identification=camp_identification, volunteer=volunteer, user = self.current_user.username, method = method)
					if test:
						print(f"You have {method} {volunteer} successfully!")
					else:
						print(f"Failed to {method} {volunteer}!")
				
				else:
					print(f"Aborted {method} volunteer operation")
		else:
			print("You are not allowed to edit volunteer list.")




		
	
	
	






