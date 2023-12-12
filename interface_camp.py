import pandas as pd

from camp_modified import Camp
from users import Users
from plans import Plans
from interface_helper import input_until_valid

from collections import defaultdict

from refugees import get_num_families_and_members_by_camp

class InterfaceCamp:
	def __init__(self, current_user):
		self.current_user = current_user


	def prompt_admin_options(self):
		"""bring up an admin menu for camp functions """
		# camp_id = Camp()
		option = input_until_valid(
			input_message = f"\n<homepage/manage-camps>\nPlease choose an operation on camps below:\
				\n[1] CANCEL\
				\n[2] List all camps (under any active plan)\
				\n[3] List all camps under a specific active plan\
				\n[4] Add a camp\
				\n[5] Delete a camp\
				\n[6] Edit camp details\
				\n[7] Edit volunteers: add to/remove from a camp",
			is_valid = lambda user_input: user_input.isdigit() and int(user_input) > 0 and int(user_input) <= 7,
			validation_message = "Unrecognized input. Please choose from the above list."
		)
		if option == "1":
			return  # CANCEL
		if option == "2":
			self.list_active_camps_user_has_access_to()
		if option == "3":
			self.prompt_list_all_camps_under_specific_plan()
			pass  # list all camps under a plan
		if option == "4":
			self.prompt_add_camp()
		if option == "5":
			self.prompt_delete_camp()
		if option == "6":
			self.prompt_edit_camp_details()
		if option == "7":
			self.prompt_edit_volunteer()


	def prompt_volunteer_options(self):
		"""bring up a volunteer menu for camp functions """
		# camp_id = Camp()
		option = input_until_valid(
			input_message = f"\n<homepage/manage-camps>\nPlease choose an operation on camps below:\
				\n[1] CANCEL\
				\n[2] View plans of camps that you have access rights to\
				\n[3] List all camps that you have access rights to\
				\n[4] Edit camp details",
			is_valid = lambda user_input: user_input.isdigit() and int(user_input) > 0 and int(user_input) <= 4,
			validation_message = "Unrecognized input. Please choose from the above list."
		)
		if option == "1":
			return  # CANCEL
		if option == "2":
			self.view_plans_of_active_accessible_camps()
		if option == "3":
			self.list_active_camps_user_has_access_to()
		if option == "4":
			self.prompt_edit_camp_details()
		

	def prompt_add_camp(self):
		camp_data = Camp.loadALLCampData()

		self.print_existing_or_accessible_ALL_camps()

		camp_id = input_until_valid(
			input_message = "Please enter the new camp ID (must be different from existing IDs)",
			is_valid = lambda user_input: user_input != "" and user_input not in camp_data,
			validation_message = "This camp_id already exists or cannot be empty."
		)

		plans = Plans.load_active_plans()
		print(f"\nExisting active plan(s): {", ".join(plans) if plans else 'None found'}")
		humanitarian_plan_in = input_until_valid(
			input_message= "Please enter the humanitarian plan this camp belongs to. Choose from the above list, or leave empty to abort.",
			is_valid = lambda user_input: user_input == "" or user_input in plans,
			validation_message = "Invalid value. Please enter the name of the humanitarian plan from the above list, or leave empty to abort."
		)
		if humanitarian_plan_in == "":
			print("Camp creation aborted.")
			return
	
		location = input_until_valid(
			input_message = f"Enter the location this camp is located in (within {plans[humanitarian_plan_in]["country"]} as specified in {humanitarian_plan_in})",
			is_valid = lambda user_input: user_input != "" and type(user_input) == str,
			validation_message = "This cannot be empty. Please enter the camp location"
		)

		max_capacity = input_until_valid(
			input_message = "Enter the camp max_capacity",
			is_valid = lambda user_input: user_input.isdigit() and int(user_input) >= 1,
			validation_message = "Camp max_capacity must be a positive integer. Please re-enter."
		)

		confirm = input_until_valid(
			input_message = f"Please confirm details of the new camp (y/n):\
				\n->Camp ID: {camp_id}\
				\n->Associated humanitarian plan: {humanitarian_plan_in}\
				\n->Max capacity: {max_capacity}\
				\n->Location: {location}\
				\n[y] Yes\
				\n[n] No (abort)",
			is_valid = lambda user_input: user_input == "y" or user_input == "n",
			validation_message = "Unrecognized input. Please confirm details of the new camp (y/n):\n[y] Yes\n[n] No (abort)"
		)
		if confirm == "y":
			success = Camp.addCamp(
				camp_id, location , max_capacity, humanitarian_plan_in)
			if success:
				print(f"Successfully added {camp_id}")
			else:
				print(f"Failed to add {camp_id}")
		else:
			print(f"Aborted camp addition.")


	def prompt_delete_camp(self):

		camps = Camp.loadActiveCampData()
		self.print_existing_or_accessible_active_camps()

		camp_id = input_until_valid(
			input_message= "Please enter the camp_id you would like to delete, or leave empty to abort:",
			is_valid = lambda user_input: user_input == "" or user_input in camps,
			validation_message = "The camp_id you entered does not exist. Please re-enter or leave empty to abort."
		)
		
		if camp_id == "":
			print("Camp deletion aborted.")
			return
		
		print("Camp to delete:")
		selected_camp = camps[camp_id]
		print(f"-> Camp ID: {camp_id}")
		for attr, val in selected_camp.items():
			print(f"-> {attr}: {val}")

		confirm = input_until_valid(
			input_message = f"Please confirm you want to delete this camp (y/n):\n->camp_id: {camp_id}\n[y] Yes\n[n] No (abort)",
			is_valid = lambda user_input: user_input == "y" or user_input == "n",
			validation_message = "Unrecognized input. Please confirm to delete the camp (y/n):\n[y] Yes\n[n] No (abort)"
		)
		if confirm == "n":
			print("Camp deletion aborted.")
			return
		
		test = Camp.delete_camp(camp_id = camp_id, username = self.current_user.username)
		print(f"Successfully deleted {camp_id}" if test else f"Failed to delete {camp_id}")


	def prompt_edit_camp_details(self):
		
		filtered_active_camps = Camp.load_active_camps_user_has_access_to(self.current_user.username)
		filtered_ALL_camps = Camp.load_ALL_camps_user_has_access_to(self.current_user.username)
		ALL_camps = Camp.loadALLCampData()
		self.print_existing_or_accessible_active_camps()

		camp_id = input_until_valid(
			input_message = "Please enter the camp_id of the camp you would like to change camp details of, or leave empty to abort",
			is_valid = lambda user_input: user_input == "" or user_input in filtered_active_camps,
			validation_message= "This camp_id does not exist or you do not have access rights to it. Please re-enter or leave empty to abort."
		)   
		
		if camp_id == "":
			print("Camp modification aborted.")
			return

		users = Users.load_users()
		is_admin = users[self.current_user.username]["is_admin"]
		
		print("\nCurrent values of the selected camp:")
		print(f"-> camp_id: {camp_id}")
		selected_camp = filtered_active_camps[camp_id]
		for field, val in selected_camp.items():
			# do not print "volunteers_in_charge", since this method does not handle it
			if field == "volunteers_in_charge" and not is_admin:
				continue
			elif field == "volunteers_in_charge":
				print(f"-> {field}: {val} (not modified here (*))")
			elif field == "humanitarian_plan_in" and not is_admin:
				print(f"-> {field}: {val} (only modifiable by admin via manage camps section)")
			else:
				print(f"-> {field}: {val}")
		
		if is_admin:
			print("(*) To modify volunteers, please exit and choose the edit volunteers option rather than edit camp details option")
		
		if is_admin:
			attribute = input_until_valid(
				input_message = "Enter the attribute (camp_id/humanitarian_plan_in/location/max_capacity) to modify:",
				is_valid = lambda user_input: user_input in {"camp_id", "location", "max_capacity", "humanitarian_plan_in"},
				validation_message = "Unrecognized input. Please enter a valid field (camp_id/humanitarian_plan_in/location/max_capacity)."
			)
		else:
			attribute = input_until_valid(
				input_message = "Enter the attribute (camp_id/location/max_capacity) to modify:",
				is_valid = lambda user_input: user_input in {"camp_id", "location", "max_capacity"},
				validation_message = "Unrecognized input. Please enter a valid field (camp_id/location/max_capacity)."
			)

		

		if attribute == "camp_id":
			print(f"Existing camp IDs: {", ".join(ALL_camps.keys()) if ALL_camps else "None found"}")
			new_value = input_until_valid(
				input_message = f"Please enter the new value for camp_id that is not in the above list",
				is_valid = lambda user_input: user_input != "" and user_input not in list(ALL_camps.keys()),
				validation_message = "The new camp_id must not be an existing camp_id. Please re-enter."
			)

		elif attribute == "max_capacity":
			current_population_size = get_num_families_and_members_by_camp()[camp_id]["num_members"]
			print(f"The current population size under {camp_id} is {current_population_size}.")

			new_value = input_until_valid(
				input_message = "Enter the camp max_capacity. Note, it must be a positive integer that is no smaller than the current population size.",
				is_valid = lambda user_input: user_input.isdigit() and int(user_input) >= max(1, current_population_size),
				validation_message = "Camp max_capacity must be a positive integer that is no smaller than the current population size. Please re-enter."
			)
		elif attribute == "humanitarian_plan_in":
			plan_keys = Plans.load_active_plans().keys()
			print(f"\nExisting active plan(s): {", ".join(plan_keys) if plan_keys else 'None found'}")
			new_value = input_until_valid(
				input_message= "Enter the humanitarian plan this camp belongs to. Choose from the above list, or leave empty to abort.",
				is_valid = lambda user_input: user_input == "" or user_input in plan_keys,
				validation_message = "Humanitarian plan must be chosen from the above list. Please re-enter or leave empty to abort."
			)
		elif attribute == "location":
			plans = Plans.load_active_plans()
			humanitarian_plan_in = filtered_active_camps[camp_id]["humanitarian_plan_in"]
			print(f"\nCurrent location: {filtered_active_camps[camp_id]["location"]}")
			new_value = input_until_valid(f"Enter the new value for the location (within {plans[humanitarian_plan_in]["country"]} as specified in {humanitarian_plan_in}):")
			
		else:  
			print(f"\nCurrent {attribute} value: {filtered_active_camps[camp_id][attribute]}")
			new_value = input_until_valid(f"Enter the new value for the {attribute}:")

		confirm = input_until_valid(
			input_message = f"Please confirm you want to change {attribute} from previous value:\n {camp_id if attribute == "camp_id" else filtered_active_camps[camp_id][attribute]} to {new_value} \n[y] Yes\n[n] No (abort)",
			is_valid = lambda user_input: user_input == "y" or user_input == "n",
			validation_message = "Unrecognized input. Please confirm (y/n):\n[y] Yes\n[n] No (abort)"
		)

		if confirm == "n":
			print(f"Camp information modification aborted.")
			return

		if attribute == "camp_id":
			test = Camp.edit_camp_id(camp_id = camp_id, new_id = new_value, username = self.current_user.username)
		else:
			test = Camp.edit_camp_details(camp_id=camp_id, attribute=attribute, new_value=new_value, username = self.current_user.username)
		
		if test:
			print(f"You've changed the {attribute} successfully!")
		else:
			print(f'Failed to change {attribute}')
			
		
			
	def prompt_edit_volunteer(self):
		camp_data = Camp.loadActiveCampData()
		users = Users.load_users()
		if not users[self.current_user.username]["is_admin"]:
			print("You are not allowed to edit volunteer list.")

		self.print_existing_or_accessible_active_camps()

		camp_id = input_until_valid(
			input_message = "Please enter the camp_id of the camp you would like to amend the volunteers in, or leave empty to abort:",
			is_valid = lambda user_input: user_input == "" or user_input in camp_data,
			validation_message = "The camp_id you entered does not exist. Please re-enter or leave empty to abort."
		)
		
		if camp_id =="":
			print("Aborted changing volunteer list.")
			return
		
		volunteer_list = Camp.get_volunteer_list(camp_id)
		print(f"\nExisting volunteers in {camp_id}: {', '.join(volunteer_list) if volunteer_list else 'None found'} (total: {len(volunteer_list)})")
		print(f"\nExisting volunteers in {camp_id}: {', '.join(volunteer_list) if volunteer_list else 'None found'} (total: {len(volunteer_list)})")

		method_char = input_until_valid(
		input_message= "Please choose an operation, or leave empty to abort:\
				\n[a] Add a volunteer\
				\n[r] Remove a volunteer",
		is_valid = lambda user_input: user_input in {"a", "r", ""},
		validation_message = f"Invalid input. Please select (a/r) to either add or remove a volunteer in camp {camp_id}, or leave empty to abort."
		)
		if method_char == "":
			print("Aborted changing volunteer list.")
			return
		

		all_volunteers_from_users = {k for k,v in users.items() if not v["is_admin"]}
		volunteers_to_add = all_volunteers_from_users.difference(set(volunteer_list))

		if method_char == "a":
			print(f"Volunteer usernames you can add: {', '.join(volunteers_to_add) if volunteers_to_add else 'None found'}")
			print(f"Volunteer usernames you can add: {', '.join(volunteers_to_add) if volunteers_to_add else 'None found'}")
			volunteer = input_until_valid(
				input_message= f"Please enter the volunteer username you want to add into volunteer list for {camp_id}, or leave empty to abort.",
				is_valid = lambda user_input: user_input == "" or (user_input not in camp_data[camp_id]["volunteers_in_charge"] and user_input in volunteers_to_add),
				validation_message = f"The username must come from an existing volunteer user that is not already in the volunteer list for {camp_id}. Please re-enter."
		)
		else:
			volunteer = input_until_valid(
				input_message = f"Please enter the volunteer username you want to remove from volunteer list for {camp_id},  or leave empty to abort.",
				is_valid = lambda user_input: user_input == "" or user_input in camp_data[camp_id]["volunteers_in_charge"],
				validation_message = f"The volunteer you entered is not in the volunteer list for {camp_id}. Please re-enter or leave empty to abort."
			)

		method = "add" if method_char == "a" else "remove"
		if volunteer == "":
			print(f"Volunteer operation ({method}) aborted.")
			return  # early termination
		confirm = input_until_valid(
			input_message = f"Please confirm you want to {method} {volunteer} {'into' if method == 'add' else 'from'} the camp {camp_id} \n[y] Yes\n[n] No (abort)",
			is_valid = lambda user_input: user_input == "y" or user_input == "n",
			validation_message = "Unrecognized input. Please confirm (y/n):\n[y] Yes\n[n] No (abort)"
		)
		if confirm == "n":
			print(f"Aborted {method} volunteer operation")
			return

		test = Camp.edit_volunteer(camp_id = camp_id, volunteer = volunteer, username = self.current_user.username, method = method)
		if test:
			print(f"You have {'added' if method == 'add' else 'removed'} {volunteer} successfully!")
			print(f"You have {'added' if method == 'add' else 'removed'} {volunteer} successfully!")
		else:
			print(f"Failed to {method} {volunteer}!")
			
			
	def list_active_camps_user_has_access_to(self):
		users = Users.load_users()
		user_is_admin = users[self.current_user.username]["is_admin"]
		filtered_active_camps = Camp.load_active_camps_user_has_access_to(self.current_user.username)
		
		print("--- Camps are as follows ---" if user_is_admin else "--- Camps you have access rights to AND under active plans are as follows ---")
		filtered_active_camps_df = pd.DataFrame.from_dict(filtered_active_camps).transpose()  # use pandas for pretty print
		print(filtered_active_camps_df if not filtered_active_camps_df.empty else "None found")
		print("--- End of camps list ---")
		input("Press Enter to continue...")
	
	def prompt_list_all_camps_under_specific_plan(self):
		""" This is intended for admin only """
		
		filtered_active_camps = Camp.load_active_camps_user_has_access_to(self.current_user.username)

		plan_keys = Plans.load_active_plans().keys()
		print(f"\nExisting active plan(s): {", ".join(plan_keys) if plan_keys else 'None found'}")
		selected_plan = input_until_valid(
			input_message= "Please enter the humanitarian plan to view camps under, or leave empty to abort.",
			is_valid = lambda user_input: user_input == "" or user_input in plan_keys,
			validation_message = "Invalid value. Please enter the name of the humanitarian plan from the above list, or leave empty to abort."
		)
		if selected_plan == "":
			print("Camp viewing aborted.")
			return
		
		print(f"--- Camps under {selected_plan} are as follows ---")
		filtered_active_camps_df = pd.DataFrame.from_dict(filtered_active_camps).transpose()  # use pandas for pretty print
		filtered_active_camps_df = filtered_active_camps_df[filtered_active_camps_df["humanitarian_plan_in"] == selected_plan]  # filter by humanitarian_plan_in
		print(filtered_active_camps_df if not filtered_active_camps_df.empty else "None found")
		print("--- End of camps list ---")
		input("Press Enter to continue...")

	
	def print_existing_or_accessible_active_camps(self):
		"""All existing camps if user is admin type
		Accessible camps if user is volunteer type """
		
		users = Users.load_users()
		is_admin = users[self.current_user.username]["is_admin"]
		filtered_active_camps = Camp.load_active_camps_user_has_access_to(self.current_user.username)

		message_key = "\nExisting camp(s) under active an plan:" if is_admin else "Camp(s) you have access rights to:"
		message_value = ", ".join(list(filtered_active_camps.keys())) if filtered_active_camps else "None found"
		print(f"{message_key} {message_value}")
	
	def print_existing_or_accessible_ALL_camps(self):
		"""All existing camps if user is admin type
		Accessible camps if user is volunteer type """
		
		users = Users.load_users()
		is_admin =  users[self.current_user.username]["is_admin"]
		filtered_ALL_camps = Camp.load_ALL_camps_user_has_access_to(self.current_user.username)

		message_key = "\nExisting camp(s):" if is_admin else "Camp(s) you have access rights to:"
		message_value = ", ".join(list(filtered_ALL_camps.keys())) if filtered_ALL_camps else "None found"
		print(f"{message_key} {message_value}")

	def view_plans_of_active_accessible_camps(self):
		plans = Plans.load_active_plans()
		camps = Camp.load_active_camps_user_has_access_to(self.current_user.username)

		planToCamps = defaultdict(list)
		for camp_id in camps:
			planToCamps[camps[camp_id]["humanitarian_plan_in"]].append(camp_id)

		planDict = {
			"description": "Description",
			"country": "Country",
			"start_date": "Start Date",
			"end_date": "End Date",
			"status": "Status"
		}

		campDict = {
			"location": "Location",
			"start_date": "Start Date",
			"max_capacity": "Max Capacity",
		}
		
		for plan_id in planToCamps:
			print("\n" + "-"*10 + f"Plan ID: {plan_id}" + "-"*10)
			for attr, val in plans[plan_id].items():
				print(f"{planDict[attr]}: {val}")
			print(f"Camps under {plan_id}:")
			for camp_id in planToCamps[plan_id]:
				print(f"\n  Camp ID: {camp_id}")
				for attr, val in camps[camp_id].items():
					if attr in {"humanitarian_plan_in", "volunteers_in_charge"}:
						continue
					print(f"  -> {campDict[attr]}: {val}")
		input("Press Enter to continue ...")
		



		
	
	
	







