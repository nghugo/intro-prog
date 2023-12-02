import json
import uuid
from collections import defaultdict

from interface_helper import input_until_valid, input_until_valid_name
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
				\n[4] Edit a refugee profile TODO\
				\n[5] Delete a refugee profile TODO",
			is_valid=lambda user_input: user_input.isdigit() and int(user_input) > 0 and int(user_input) <= 5,
			validation_message="Unrecognized input. Please choose from the above list."
		)
		if option == "1":
			return  # option 1 is cancel, so just return
		if option == "2":
			self.print_all_refugees_user_has_access_to()
		if option == "3":
			self.prompt_add_refugee()
		if option == "4":
			pass  # NOTE: make sure a volunteer is only able to edit refugees in the camps that they have access rights to
		if option == "5":
			pass  # NOTE: make sure a volunteer is only able to delete refugees from the camps that they have access rights to

	def prompt_volunteer_options(self):
		option = input_until_valid(
			
			input_message = f"\n<homepage/manage-refugees>\nPlease choose a refugee management option below:\
				\n[1] CANCEL\
				\n[2] List all refugee profiles under camps you have access rights to\
				\n[3] Add a refugee profile\
				\n[4] Edit a refugee profile TODO\
				\n[5] Delete a refugee profile TODO",
			is_valid=lambda user_input: user_input.isdigit() and int(user_input) > 0 and int(user_input) <= 5,
			validation_message="Unrecognized input. Please choose from the above list."
		)
		if option == "1":
			return  # option 1 is cancel, so just return
		if option == "2":
			self.print_all_refugees_user_has_access_to()
		if option == "3":
			self.prompt_add_refugee()
		if option == "4":
			pass
		if option == "5":
			pass
	
	def prompt_add_refugee(self):
		existing_ids = self.load_refugees().keys()
		refugee_id = input_until_valid(
			input_message="Enter a unique id to identify this refugee, or leave empty to auto-generate:",
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
			recorded_refugees = self.load_refugees()
			recorded_refugees[refugee_id] = refugee_infomation
			with open("refugees.json", "w") as json_file:
				json.dump(recorded_refugees, json_file, indent=2)
			print(f"Refugee {fullname} ({refugee_id}) has been added successfully.")
		else:
			print(f"Aborted refugee addition.")
	
	@staticmethod
	def load_refugees():
		try:
			with open("refugees.json", "r") as json_file:
				json_load = json.load(json_file)
				return json_load
		except FileNotFoundError:
			return {}
	
	def print_all_refugees_user_has_access_to(self):
		
		accessible_refugees_sep_by_camp = self.get_accessible_refugeeids_sep_by_camp(username = self.current_user.username)
		
		users = Users.load_users()
		if users[self.current_user.username]["is_admin"]:
			print("\n--- List of refugees ---")
		else:
			print("\n--- List of refugees under camps you have access rights to ---")

		if not accessible_refugees_sep_by_camp:
			print("None found")
		else:
			for camp, refugee_id_fullname in accessible_refugees_sep_by_camp.items():
				print(f"{camp}:")
				for refugee_id, refugee_fullname in refugee_id_fullname:
					print(f"-> {refugee_fullname} ({refugee_id})")
		print("--- End of refugee list ---")
		input("Press Enter to continue...")
	

	def get_accessible_refugeeids_sep_by_camp(self, username) -> dict:
		accessible_refugees = self.get_accessible_refugees(username)
		accessible_refugees_sep_by_camp =  defaultdict(list)
		for refugee_id, refugee_values in accessible_refugees.items():
			accessible_refugees_sep_by_camp[refugee_values["camp_id"]].append((refugee_id, refugee_values["fullname"]))
		return accessible_refugees_sep_by_camp

	def get_accessible_refugees(self, username):
		all_refugees = self.load_refugees()
		accessible_refugees = {refugee_id: refugee_values for refugee_id, refugee_values in all_refugees.items() 
						 if Camp.user_has_access(camp_id = refugee_values["camp_id"], username = username)}
		return accessible_refugees


	def prompt_modify_refugee(self,):
		pass
	

	def prompt_delete_refugee(self):
		pass