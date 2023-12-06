#interface volunteer option.py
#resources.py
from resource_modified import CampResources
#handle user input
from interface_helper import input_until_valid
from users import Users
from camp_modified import Camp
import pandas as pd


class InterfaceManageResource:
	def __init__(self,current_user):
		self.current_user = current_user
		self.resources = CampResources().resources
		
	def prompt_admin_options(self):
		option = input_until_valid(
				input_message = f"\n<homepage/manage-resources>\nPlease choose a resource management option below:\
					\n[1] CANCEL\
					\n[2] List all resource profiles under all camps\
					\n[3] List all resource profiles under a specific camp\
					\n[4] Allocate resources to a specific camp",
				is_valid=lambda user_input: user_input.isdigit() and int(user_input) > 0 and int(user_input) <= 4,
				validation_message="Unrecognized input. Please choose from the above list.")
		
		if option == "1":
			return
		if option == "2":
			self.prompt_display_all_camps()
		if option == "3":
			self.prompt_display_specific_camp()
		if option == "4":
			self.prompt_update_resources()

	# @staticmethod
	# def validate_input_camp(camp_id,current_user): 
	# 	users = Users.load_users()
	# 	camp_data = Camp.loadCampData()
	# 	is_admin = users[current_user]["is_admin"]
	# 	if camp_id in camp_data:
	# 		if is_admin or current_user in camp_data[camp_id]["volunteers_in_charge"]:
	# 			return True
	# 	return False
		
	def prompt_volunteer_options(self):
		option = input_until_valid(
				input_message = f"\n<homepage/manage-resources>\nPlease choose a resource management option below:\
					\n[1] CANCEL\
					\n[2] List all resource profiles under a specific camp\
					\n[3] Allocate resources to a specific camp",
				is_valid=lambda user_input: user_input.isdigit() and int(user_input) > 0 and int(user_input) <= 3,
				validation_message="Unrecognized input. Please choose from the above list.")
		
		if option == "1":
			return
		if option == "2":
			self.prompt_display_specific_camp()
		if option == "3":
			self.prompt_update_resources()
	
	def prompt_display_all_camps(self):
		print('Resources for all camps:')
		df = pd.DataFrame(self.resources)
		df_tranpose = df.to_string()  # to_string: prevent table truncation
		print(df_tranpose)
		print("----------------------------------End of resources table-------------------------------------")
		input("Press Enter to continue...")

	# removed functionality
	# def print_exist_camp(self):
	#     df = pd.DataFrame(self.resources)
	#     df_tranpose = df.transpose()
	#     column_names = df.columns.tolist()
	#     df_camp = pd.DataFrame({'camp name': column_names})
	#     print(df_camp)

	def prompt_display_specific_camp(self):
		users = Users.load_users()
		is_admin = users[self.current_user.username]["is_admin"]

		filtered_camps = Camp.load_camps_user_has_access_to(self.current_user.username)
		message_key = "\nExisting camp(s):" if is_admin else "Camp(s) you have access rights to:"
		message_value = ", ".join(list(filtered_camps.keys())) if filtered_camps else "None found"
		print(f"{message_key} {message_value}")

		if is_admin:
			camp_id = input_until_valid(
				input_message = "Enter the camp name, or leave empty to abort: ", 
				is_valid = lambda user_input: (user_input == "") or (user_input in self.resources), 
				validation_message = "Unrecognized camp. Please enter a new one, or leave empty to abort: ")
			
			if camp_id == "":
				print("Aborted displaying resources.")
				return

			resource_sepecific_camp = CampResources()
			resource_sepecific_camp.display_resources(camp_id)
			print("-------End of resource details--------")
			input("Press Enter to continue...")
		else:
			camp_id = input_until_valid(
				input_message = "Enter the camp name, or leave empty to abort: ", 
				is_valid = lambda user_input: (user_input == "") or (user_input in filtered_camps), 
				validation_message = "Unrecognized camp or camp not accessible. Please enter a new one or leave empty to abort: ")
			
			if camp_id == "":
				print("Aborted displaying resources.")
				return

			resource_sepecific_camp = CampResources()
			resource_sepecific_camp.display_resources(camp_id)
			print("-------End of resource details--------")
			input("Press Enter to continue...")
		

	def prompt_update_resources(self):

		users = Users.load_users()
		is_admin =  users[self.current_user.username]["is_admin"]

		filtered_camps = Camp.load_camps_user_has_access_to(self.current_user.username)
		message_key = "\nExisting camp(s):" if is_admin else "Camp(s) you have access rights to:"
		message_value = ", ".join(list(filtered_camps.keys())) if filtered_camps else "None found"
		print(f"{message_key} {message_value}")

		camp_id = input_until_valid(input_message="Enter the camp name or press Enter to abort: ", 
						is_valid=lambda user_input:(user_input == "") or user_input in filtered_camps, 
						validation_message="Unrecognized camp or camp not accessible. Please enter a new one or leave empty to abort: ")
		
		if camp_id =="":
			print("Aborted resource amount modification.")
			return
		
		# TODO: present the population of the camp.
		df = pd.DataFrame(self.resources).transpose()
		print(f"Resources allocated to this {camp_id}:")
		print(df.loc[camp_id].to_string())
		not_exit = True
		while not_exit:
			resource_to_edit = input_until_valid(input_message="Enter the resource to edit: food_packets/medical_packets/water_packets/shelter_packets/clothing_packets/first_aid_packets/baby_packet/sanitation_packets), or leave empty to abort:",
												is_valid=lambda user_input: user_input in self.resources[camp_id] or user_input == "",
												validation_message="Unrecognized input. Please enter again.")
			if resource_to_edit == "":
				print("Aborted resource amount modification.")
				return
			
			new_amount = input_until_valid(input_message= f"Enter the new amount for {resource_to_edit} or press Enter to abort: ",
												is_valid=lambda user_input: user_input.isdigit() or user_input == "",
												validation_message="Unrecognized input. Please enter again.")
			if new_amount == "":
				print("Aborted resource amount modification.")
				return
			
			confirm = input_until_valid(input_message=f"Please confirm your modification:\
							   \n-> Resource: {resource_to_edit}\
							   \n-> Old amount: {df.loc[camp_id, resource_to_edit]}\
							   \n-> New amount: {new_amount}\
							   \n[y] Yes\
							   \n[n] No (abort)",
										is_valid = lambda user_input: user_input == "y" or user_input == "n",
										validation_message="Unrecognized input. Please confirm (y/n):\n[y] Yes\n[n] No (abort)")
			
			if confirm == "n":
				print("Aborted resource amount modification.")
				return
			resource = CampResources()
			test = resource.update_resources(camp_id,resource_to_edit,int(new_amount))

			if test:
				print(f"You've changed the {resource_to_edit} successfully!")
			else:
				print(f'Failed to change {resource_to_edit}')

			exit_confirm = input_until_valid(input_message="Do you want to edit other resource amounts?\n[y] Yes\n[n] No (abort)",
										is_valid = lambda user_input: user_input == "y" or user_input == "n",
										validation_message="Unrecognized input. Please confirm (y/n):\n[y] Yes\n[n] No (abort)")
			
			if exit_confirm == 'y':
				not_exit = True
			else:
				not_exit = False

		


		


		


	

