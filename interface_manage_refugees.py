import json
import uuid

from interface_helper import input_until_valid, input_until_valid_name
from users import Users

class InterfaceManageRefugees:
	def __init__(self, current_user):
		self.current_user = current_user

	def prompt_volunteer_options(self):
		option = input_until_valid(
			
			input_message = f"\n<homepage/manage-refugees>\nPlease choose a refugee management option below:\
				\n[1] CANCEL\
				\n[2] List all refugee profiles TODO\
				\n[3] Add a refugee profile\
				\n[4] Edit a refugee profile TODO\
				\n[5] Delete a refugee profile TODO\
				\n[6] TODO\
				\n[7] TODO",
			is_valid=lambda user_input: user_input.isdigit() and int(user_input) > 0 and int(user_input) <= 7,
			validation_message="Unrecognized input. Please choose from the above list."
		)
		if option == "1":
			return  # option 1 is cancel, so just return
		if option == "2":
			pass
		if option == "3":
			self.prompt_add_refugee()
		if option == "4":
			pass
		if option == "5":
			pass
		if option == "6":
			pass
		if option == "7":
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
		camp_identification = input_until_valid(
			input_message="Enter camp identification for this refugee:",
			is_valid=lambda user_input: user_input.strip() != "",
			validation_message="Camp identification cannot be empty. Please enter a valid camp identification."
		)
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
				\n->Camp identification: {camp_identification}\
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
				"camp_identification": camp_identification,
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
	
	def list_all_refugees_with_access_rights(self):
		pass



	# TODO: method: remove refugee from camp
	# TODO: method: print all refugees of a camp