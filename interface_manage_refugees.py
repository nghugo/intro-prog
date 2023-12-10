import json
import uuid
import pandas as pd


from interface_helper import input_until_valid, input_until_valid_name
from refugees import load_active_refugees, load_ALL_refugees, get_accessible_refugees, get_accessible_refugees_sep_by_camp, get_num_families_and_members_by_camp
from camp_modified import Camp
from users import Users



class InterfaceManageRefugees:
	def __init__(self, current_user):
		self.current_user = current_user
	

	def prompt_admin_options(self):
		option = input_until_valid(
			
			input_message = f"\n<homepage/manage-refugees>\nPlease choose a refugee management option below:\
				\n[1] CANCEL\
				\n[2] List all refugee profiles under all camps (in active plans)\
				\n[3] List all refugee profiles under a specific camp (in an active plan)\
				\n[4] Add a refugee profile\
				\n[5] Edit a refugee profile\
				\n[6] Delete a refugee profile",
			is_valid=lambda user_input: user_input.isdigit() and int(user_input) > 0 and int(user_input) <= 6,
			validation_message="Unrecognized input. Please choose from the above list."
		)
		if option == "1":
			return  # option 1 is cancel, so just return
		if option == "2":
			self.verbose_print_all_refugees_user_has_access_to()
		if option == "3":
			self.prompt_verbose_print_all_refugees_under_camp()
		if option == "4":
			self.prompt_add_refugee()
		if option == "5":
			self.prompt_modify_refugee()
		if option == "6":
			self.prompt_delete_refugee()


	def prompt_volunteer_options(self):
		option = input_until_valid(
			
			input_message = f"\n<homepage/manage-refugees>\nPlease choose a refugee management option below:\
				\n[1] CANCEL\
				\n[2] List all refugee profiles under all camps you have access rights to (under active plans)\
				\n[3] List all refugee profiles under a specific camp (under an active plan)\
				\n[4] Add a refugee profile\
				\n[5] Edit a refugee profile\
				\n[6] Delete a refugee profile",
			is_valid=lambda user_input: user_input.isdigit() and int(user_input) > 0 and int(user_input) <= 5,
			validation_message="Unrecognized input. Please choose from the above list."
		)
		if option == "1":
			return  # option 1 is cancel, so just return
		if option == "2":
			self.verbose_print_all_refugees_user_has_access_to()
		if option == "3":
			self.prompt_verbose_print_all_refugees_under_camp()
		if option == "4":
			self.prompt_add_refugee()
		if option == "5":
			self.prompt_modify_refugee()
		if option == "6":
			self.prompt_delete_refugee()
	

	def prompt_add_refugee(self):
		existing_ids = load_ALL_refugees().keys()

		# Done: volunteer is only able to add refugees to the camps that they have access rights to
		accessible_camps = Camp.load_active_camps_user_has_access_to(self.current_user.username)
		accessible_camps_ids = accessible_camps.keys()
		
		camp_id = input_until_valid(
			input_message=f"Enter camp ID for this refugee, or leave empty to abort:\
				\n(Note: Camp(s) under active plan(s) accessible by you are: {", ".join(accessible_camps_ids) if accessible_camps_ids else "None found"})",
			is_valid=lambda user_input: user_input == "" or user_input in accessible_camps_ids,
			validation_message="Camp ID not found. Please choose from the above list of camp IDs, or leave empty to abort."
		)
		if camp_id == "":
			print("Refugee creation aborted.")
			return

		camp_total_num_members = get_num_families_and_members_by_camp()[camp_id]["num_members"]
		max_capacity = accessible_camps[camp_id]["max_capacity"]
		remaining_spaces = max(max_capacity - camp_total_num_members, 0)
		
		if not remaining_spaces:
			print(f"The camp {camp_id} is already at maximum capacity ({max_capacity}). No refugees can be added.")
			return
		print(f"Note -> Remaining space(s) in {camp_id}: {remaining_spaces}")
		
		print(f"Existing refugee IDs: {", ".join(existing_ids) if existing_ids else "None found."}")
		refugee_id = input_until_valid(
			input_message="Enter a unique id to identify this refugee (different from above list), or leave empty to auto-generate:",
			is_valid=lambda user_input: user_input == "" or user_input not in existing_ids,
			validation_message="Refugee id already exists. Please try another id."
		)
		if refugee_id == "":
			refugee_id = uuid.uuid4().hex
		
		fullname = input_until_valid_name(
			input_message="Enter the full name of the refugee/ representitive of the family:",
			validation_message="Full name can only contain letters and spaces. Please re-enter."
		)
		
		print(f"Note -> Remaining space(s) in {camp_id}: {remaining_spaces}")
		number_of_members = int(input_until_valid(
			input_message="Enter the number of members in the refugee family:",
			is_valid=lambda user_input: user_input.isdigit() and int(user_input) >= 1 and int(user_input) <= remaining_spaces,
			validation_message=f"Number of family members must be a positive integer (1-{remaining_spaces} inclusive). Please re-enter."
		))
			
		medical_condition = input_until_valid(
			input_message="Enter medical condition:",
			is_valid=lambda user_input: user_input.strip() != "",
			validation_message="Medical condition cannot be empty. Please enter a valid medical condition."
		)  
		confirm = input_until_valid(
			input_message=f"Please confirm details of the new refugee (y/n):\
				\n->Refugee ID: {refugee_id}\
				\n->Full Name: {fullname}\
				\n->Number of family members: {number_of_members}\
				\n->Camp ID: {camp_id}\
				\n->Medical condition: {medical_condition}\
				\n[y] Yes\
				\n[n] No (abort)",
			is_valid=lambda user_input: user_input == "y" or user_input == "n",
			validation_message="Unrecognized input. Please confirm details of the new refugee (y/n):\n[y] Yes\n[n] No (abort)"
		)
		if confirm == "y":
			refugee_infomation = {
				"fullname": fullname,
				"number_of_members": number_of_members,
				"camp_id": camp_id,
				"medical_condition": medical_condition,
			}
			recorded_refugees = load_active_refugees()
			recorded_refugees[refugee_id] = refugee_infomation
			with open("refugees.json", "w") as json_file:
				json.dump(recorded_refugees, json_file, indent=2)
			print(f"Refugee {fullname} ({refugee_id}) has been added successfully.")
		else:
			print(f"Aborted refugee profile creation.")


	def verbose_print_all_refugees_user_has_access_to(self):
		accessible_refugees_sep_by_camp = get_accessible_refugees_sep_by_camp(username = self.current_user.username)
		users = Users.load_users()
		if users[self.current_user.username]["is_admin"]:
			print("\n--- List of refugees ---")
		else:
			print("\n--- List of refugees under camps you have access rights to (under active plans) ---")
		if not accessible_refugees_sep_by_camp:
			print("None found")
		else:
			refugee_count_dict = get_num_families_and_members_by_camp()
			for camp_id, refugee_id_values in accessible_refugees_sep_by_camp.items():
				refugee_count = refugee_count_dict[camp_id]
				self.print_refugees_one_camp_helper(camp_id, refugee_id_values, refugee_count)
				
		print("\n--- End of refugee list ---")
		input("Press Enter to continue...")

	@staticmethod
	def print_refugees_one_camp_helper(camp_id, refugee_id_values, refugee_count):
		camp_max_capacity = Camp.loadActiveCampData()[camp_id]["max_capacity"]
		print(f"\n{{{camp_id}}} (total members: {refugee_count["num_members"]}, remaining capacity: {camp_max_capacity - refugee_count["num_members"]})")
		for refugee_id, refugee_values in refugee_id_values:
			print(f"  {refugee_values["fullname"]} (ID: {refugee_id})")
			for attr, val in refugee_values.items():
				if attr != "fullname":
					print(f"  -> {attr}: {val}")


	def prompt_verbose_print_all_refugees_under_camp(self):
		users = Users.load_users()
		accessible_camps = Camp.load_active_camps_user_has_access_to(self.current_user.username)
		if users[self.current_user.username]["is_admin"]:
			print(f"Existing camp(s) under active plan(s): {", ".join(accessible_camps.keys() if accessible_camps else "None found")}")
		else:
			print(f"The camps that you have access to are: {", ".join(accessible_camps.keys() if accessible_camps else "None found")}")

		selected_camp = input_until_valid(
			input_message="Enter the camp ID of the camp under which you want to list all refugees",
			is_valid = lambda user_input: user_input in accessible_camps or user_input == "",
			validation_message="Camp ID does not exist, or you do not have access rights to it. Please enter an existing camp ID or leave empty to abort."
		)
		if selected_camp == "":
			print("Aborted listing refugees under camp.")
			return
		
		accessible_refugees_sep_by_camp = get_accessible_refugees_sep_by_camp(username = self.current_user.username)
		refugees_under_selected_camp = accessible_refugees_sep_by_camp[selected_camp]
		
		print(f"\n--- List of refugees under {selected_camp} ---")

		if not refugees_under_selected_camp:
			print("None found")
		else:
			refugee_count = get_num_families_and_members_by_camp()[selected_camp]
			self.print_refugees_one_camp_helper(selected_camp, refugees_under_selected_camp, refugee_count)
		print("\n--- End of refugee list ---")
		input("Press Enter to continue...")


	def succint_print_all_refugees_user_has_access_to(self):
		accessible_refugees_sep_by_camp = get_accessible_refugees_sep_by_camp(username = self.current_user.username)
		users = Users.load_users()

		if users[self.current_user.username]["is_admin"]:
			print("\nExisting refugees under camps of active plans:")
		else:
			print("\nExisting refugees under camps of active plans that have access rights to:")
		
		for camp, refugee_id_values in accessible_refugees_sep_by_camp.items():
			print(f"{camp}:")
			ref_list_in_camp = []
			for refugee_id, refugee_values in refugee_id_values:
				ref_list_in_camp.append(f"{refugee_values["fullname"]} (ID: {refugee_id})")
			print("-> " + ", ".join(ref_list_in_camp))


	def prompt_modify_refugee(self):
		accessible_refugees = get_accessible_refugees(self.current_user.username)
		self.succint_print_all_refugees_user_has_access_to()

		accessible_active_camps = Camp.load_active_camps_user_has_access_to(self.current_user.username)
		accessible_active_camps_ids = accessible_active_camps.keys()
		
		refugee_id = input_until_valid(
			input_message="Enter the refugee ID of the refugee profile to modify or leave empty to abort:",
			is_valid = lambda user_input: user_input in accessible_refugees or user_input == "",
			validation_message="Refugee ID not found or not accessible by you. Please enter an existing refugee ID or leave empty to abort."
		)
		if refugee_id == "":
			print("Aborted refugee profile edit.")
			return

		self.print_refugee_values(refugee_id, accessible_refugees[refugee_id])

		field = input_until_valid(
			input_message="Enter the field (fullname/number_of_members/camp_id/medical_condition) to modify, or leave empty to abort:",
			is_valid=lambda user_input: user_input in {
				"", "fullname", "number_of_members", "camp_id", "medical_condition"},
			validation_message="Unrecognized input. Please enter a valid field (fullname/number_of_members/camp_id/medical_condition)."
		)
		if field == "":
			print("Refugee modification aborted.")
			return

		if field == "fullname":
			value = input_until_valid_name(
				input_message="Enter the full name of the refugee/ representitive of the family:",
				validation_message="Full name can only contain letters and spaces. Please re-enter."
			)
		elif field == "number_of_members":
			
			camp_id = accessible_refugees[refugee_id]["camp_id"]
			camp_total_num_members = get_num_families_and_members_by_camp()[camp_id]["num_members"]
			max_capacity = accessible_active_camps[camp_id]["max_capacity"]
			remaining_spaces = max(max_capacity - camp_total_num_members, 0)

			current_family_num_members = accessible_refugees[refugee_id]["number_of_members"]

			print(f"Note:\
				\n -> Remaining space(s) in {camp_id}: {remaining_spaces} (excluding current family members)\
				\n -> Current number of members in the family: {current_family_num_members}")

			value = int(input_until_valid(
			input_message=f"Enter the new number of members in the refugee family (1-{remaining_spaces + current_family_num_members} inclusive):",
			is_valid=lambda user_input: user_input.isdigit() and int(user_input) >= 1 and int(user_input) <= remaining_spaces + current_family_num_members,
			validation_message=f"Number of family members must be a positive integer (1-{remaining_spaces + current_family_num_members} inclusive). Please re-enter."
		))
		elif field == "camp_id":
			
			camp_id = accessible_refugees[refugee_id]["camp_id"]
			refugee_count_dict = get_num_families_and_members_by_camp()
			
			current_refugee_num_members = load_active_refugees()[refugee_id]["number_of_members"]
			camps_with_space = []
			spaces_stats_df = pd.DataFrame(columns=['Max Capacity', 'Current Total Members', 'Extra Spaces'])
			
			for alt_camp_id in accessible_active_camps_ids:	
				alt_camp_total_num_members = refugee_count_dict[alt_camp_id]["num_members"]
				alt_camp_max_capacity = accessible_active_camps[alt_camp_id]["max_capacity"]
				row_name = alt_camp_id if alt_camp_id != camp_id else alt_camp_id+" (current)"
				spaces_stats_df.loc[row_name] = [alt_camp_max_capacity, alt_camp_total_num_members, alt_camp_max_capacity - alt_camp_total_num_members]
				alt_camp_remaining_spaces = max(alt_camp_max_capacity - alt_camp_total_num_members, 0)
				if alt_camp_remaining_spaces >= current_refugee_num_members or alt_camp_id == camp_id:
					camps_with_space.append(alt_camp_id)
			
			print("\nRefugee statistics of camp(s) under active plan(s) accessible by you:")
			print(spaces_stats_df)
			print(f"(Recall that the current refugee has {current_refugee_num_members} members)")

			camps_without_space = list(set(accessible_active_camps_ids).difference(set(camps_with_space)))

			value = input_until_valid(
				input_message=f"\nNote:\
					\n(1) Camp(s) under active plan(s) accessible by you AND with spaces for refugees: \n  {', '.join(camps_with_space) if camps_with_space else 'None found'}\
					\n(2) Camp(s) under active plan(s) accessible by you, but WITHOUT spaces for refugees: \n  {', '.join(camps_without_space) if camps_without_space else 'None found'}\
					\nEnter new camp ID from list (1) for this refugee, or leave empty to abort:",
				is_valid=lambda user_input: user_input == "" or user_input in camps_with_space,
				validation_message="Camp ID not found. Please choose camp IDs from list (1), or leave empty to abort."
			)
			if value == "":
				print("Refugee modification aborted.")
				return
			
		elif field == "medical_condition":
			value = input_until_valid(
				input_message="Enter medical condition:",
				is_valid=lambda user_input: user_input.strip() != "",
				validation_message="Medical condition cannot be empty. Please enter a valid medical condition."
			)

		confirm = input_until_valid(
			input_message=f"Please confirm details of the refugee modification (y/n):\
				\n->Refugee: {accessible_refugees[refugee_id]["fullname"]} (ID: {refugee_id})\
				\n->Field: {field}\
				\n->Previous Value: {accessible_refugees[refugee_id][field] if field != "refugee_id" else {refugee_id}}\
				\n->New Value: {value}\
				\n[y] Yes\
				\n[n] No (abort)",
			is_valid=lambda user_input: user_input == "y" or user_input == "n",
			validation_message="Unrecognized input. Please confirm details of the refugee modification (y/n):\n[y] Yes\n[n] No (abort)"
		)
		
		if confirm == "n":
			print("Refugee modification aborted.")
			return
	
		recorded_refugees = load_active_refugees()			
		refugee_obj = recorded_refugees[refugee_id]
		refugee_obj[field] = value  # update refugee object's field to new value
		recorded_refugees[refugee_id] = refugee_obj

		with open("refugees.json", "w") as json_file:
			json.dump(recorded_refugees, json_file, indent=2)
		print(f"Refugee {accessible_refugees[refugee_id]["fullname"]} ({refugee_id}) has been added successfully.")
		print("Successfully modified refugee.")
			
	
	@staticmethod
	def print_refugee_values(refugee_id, refugee_obj):
		print("\nCurrent values of the selected refugee:")
		print(f"-> id: {refugee_id} (not modifiable)")
		for key, val in refugee_obj.items():
			print(f"-> {key}: {val}")		
	

	def prompt_delete_refugee(self):
		accessible_refugees = get_accessible_refugees(self.current_user.username)
		self.succint_print_all_refugees_user_has_access_to()
		
		refugee_id = input_until_valid(
			input_message="Enter the refugee ID of the refugee to modify or leave empty to abort:",
			is_valid = lambda user_input: user_input in accessible_refugees or user_input == "",
			validation_message="Refugee ID not found. Please enter an existing refugee ID or leave empty to abort."
		)
		if refugee_id == "":
			print("Aborted refugee profile edit.")
			return
	
		refugee_fullname = accessible_refugees[refugee_id]["fullname"]

		
		data = load_active_refugees()
		del data[refugee_id]
		with open("refugees.json", "w") as json_file:
			json.dump(data, json_file, indent=2)

		print(f"Successfully deleted refugee {refugee_fullname} ({refugee_id})")