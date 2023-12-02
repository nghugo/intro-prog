import json
import uuid


from interface_helper import input_until_valid, input_until_valid_name
from refugees import load_refugees, get_accessible_refugees, get_accessible_refugees_sep_by_camp
from camp_modified import Camp
from users import Users



class InterfaceManageRefugees:
	def __init__(self, current_user):
		self.current_user = current_user
	

	def prompt_admin_options(self):
		option = input_until_valid(
			
			input_message = f"\n<homepage/manage-refugees>\nPlease choose a refugee management option below:\
				\n[1] CANCEL\
				\n[2] List all refugee profiles under each camp\
				\n[3] Add a refugee profile\
				\n[4] Edit a refugee profile\
				\n[5] Delete a refugee profile",
			is_valid=lambda user_input: user_input.isdigit() and int(user_input) > 0 and int(user_input) <= 5,
			validation_message="Unrecognized input. Please choose from the above list."
		)
		if option == "1":
			return  # option 1 is cancel, so just return
		if option == "2":
			self.verbose_print_all_refugees_user_has_access_to()
		if option == "3":
			self.prompt_add_refugee()
		if option == "4":
			self.prompt_modify_refugee()
		if option == "5":
			self.prompt_delete_refugee()


	def prompt_volunteer_options(self):
		option = input_until_valid(
			
			input_message = f"\n<homepage/manage-refugees>\nPlease choose a refugee management option below:\
				\n[1] CANCEL\
				\n[2] List all refugee profiles under camps you have access rights to\
				\n[3] Add a refugee profile\
				\n[4] Edit a refugee profile\
				\n[5] Delete a refugee profile",
			is_valid=lambda user_input: user_input.isdigit() and int(user_input) > 0 and int(user_input) <= 5,
			validation_message="Unrecognized input. Please choose from the above list."
		)
		if option == "1":
			return  # option 1 is cancel, so just return
		if option == "2":
			self.verbose_print_all_refugees_user_has_access_to()
		if option == "3":
			self.prompt_add_refugee()
		if option == "4":
			self.prompt_modify_refugee()
		if option == "5":
			self.prompt_delete_refugee()
	

	def prompt_add_refugee(self):
		existing_ids = load_refugees().keys()
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
		number_of_members = int(input_until_valid(
			input_message="Enter the number of members in the refugee family:",
			is_valid=lambda user_input: user_input.isdigit() and int(user_input) >= 1 and int(user_input) <= 100,
			validation_message="Number of family members must be a positive integer (1-100 inclusive). Please re-enter."
		))
		
		# Done: make sure a volunteer is only able to add refugees to the camps that they have access rights to

		filtered_camps = Camp.load_camps_user_has_access_to(self.current_user.username)
		filtered_camps_ids = filtered_camps.keys()

		camp_id = input_until_valid(
			input_message=f"Enter camp ID for this refugee, or leave empty to abort:\
				\n(Note: Camps accessible by you are: {", ".join(filtered_camps_ids) if filtered_camps_ids else "None found"})",
			is_valid=lambda user_input: user_input == "" or user_input in filtered_camps_ids,
			validation_message="Camp ID not found. Please choose from the above list of camp IDs, or leave empty to abort."
		)
		if camp_id == "":
			print("Refugee creation aborted.")
			return
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
			recorded_refugees = load_refugees()
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
			print("\n--- List of refugees under camps you have access rights to ---")
		if not accessible_refugees_sep_by_camp:
			print("None found")
		else:
			for camp, refugee_id_values in accessible_refugees_sep_by_camp.items():
				print(f"\n{{{camp}}}")
				for refugee_id, refugee_values in refugee_id_values:
					print(f"\n{refugee_values["fullname"]} (ID: {refugee_id})")
					for attr, val in refugee_values.items():
						if attr != "fullname":
							print(f"-> {attr}: {val}")
		print("\n--- End of refugee list ---")
		input("Press Enter to continue...")


	def succint_print_all_refugees_user_has_access_to(self):
		accessible_refugees_sep_by_camp = get_accessible_refugees_sep_by_camp(username = self.current_user.username)
		users = Users.load_users()

		if users[self.current_user.username]["is_admin"]:
			print("\nExisting refugees:")
		else:
			print("\nExisting refugees under camps that have access rights to:")
		
		for camp, refugee_id_values in accessible_refugees_sep_by_camp.items():
			print(f"{camp}:")
			ref_list_in_camp = []
			for refugee_id, refugee_values in refugee_id_values:
				ref_list_in_camp.append(f"{refugee_values["fullname"]} (ID: {refugee_id})")
			print("-> " + ", ".join(ref_list_in_camp))


	def prompt_modify_refugee(self):
		accessible_refugees = get_accessible_refugees(self.current_user.username)
		self.succint_print_all_refugees_user_has_access_to()
		
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
			value = int(input_until_valid(
			input_message="Enter the number of members in the refugee family:",
			is_valid=lambda user_input: user_input.isdigit() and int(user_input) >= 1 and int(user_input) <= 100,
			validation_message="Number of family members must be a positive integer (1-100 inclusive). Please re-enter."
		))
		elif field == "camp_id":
			filtered_camps = Camp.load_camps_user_has_access_to(self.current_user.username)
			filtered_camps_ids = filtered_camps.keys()

			value = input_until_valid(
				input_message=f"Enter camp ID for this refugee, or leave empty to abort:\
					\n(Note: Camps accessible by you are: {", ".join(filtered_camps_ids) if filtered_camps_ids else "None found"})",
				is_valid=lambda user_input: user_input == "" or user_input in filtered_camps_ids,
				validation_message="Camp ID not found. Please choose from the above list of camp IDs, or leave empty to abort."
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
	
		recorded_refugees = load_refugees()			
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

		with open("refugees.json", "r") as json_file:
			data = json.load(json_file)
		del data[refugee_id]
		with open("refugees.json", "w") as json_file:
			json.dump(data, json_file, indent=2)

		print(f"Successfully deleted refugee {refugee_fullname} ({refugee_id})")