#interface volunteer option.py
#resources.py
from resource_modified import CampResources
#handle user input
from interface_helper import input_until_valid
from users import Users
from camp_modified import Camp
from refugees import load_ALL_refugees, load_active_refugees, get_num_families_and_members_by_camp
from collections import defaultdict
import pandas as pd
class InterfaceManageResource:
	def __init__(self,current_user):
		self.current_user = current_user
		
	def prompt_admin_options(self):
		option = input_until_valid(
				input_message = f"\n<homepage/manage-resources>\nPlease choose a resource management option below:\
					\n[1] CANCEL\
					\n[2] List all resource profiles under all camps (*)\
					\n[3] List all resource profiles under a specific camp (*)\
					\n[4] Update (overwrite) resources of a specific camp (*)\
					\n[5] Add resources to a specific camp (*)\
					\n[6] Limited resources warning (*)\
					\nPlease note: options annotated with (*) are only for entities under active plans",
				is_valid=lambda user_input: user_input.isdigit() and int(user_input) > 0 and int(user_input) <= 6,
				validation_message="Unrecognized input. Please choose from the above list.")
		
		if option == "1":
			return
		if option == "2":
			self.prompt_display_all_camps()
		if option == "3":
			self.prompt_display_specific_camp()
		if option == "4":
			self.prompt_change_resources('update')
		if option == "5":
			self.prompt_change_resources('add')
		if option == "6":
			self.prompt_resource_warning()

	# @staticmethod
	# def validate_input_camp(camp_id,current_user): 
	# 	users = Users.load_users()
	# 	camp_data = Camp.loadCampData()
	# 	is_admin = users[current_user]["is_admin"]
	# 	if camp_id in camp_data:
	# 		if current_user in camp_data[camp_id]["volunteers_in_charge"]:
	# 			return True
	# 		elif is_admin:
	# 			return True
	# 		else:
	# 			return False
	# 	return False
		
	def prompt_volunteer_options(self):
		option = input_until_valid(
				input_message = f"\n<homepage/manage-resources>\nPlease choose a resource management option below:\
					\n[1] CANCEL\
					\n[2] List all resource profiles under a specific camp (under an active plan) (*)\
					\n[3] Update (overwrite) resources of a specific camp (under an active plan) (*)\
					\n[4] Add resources to a specific camp (under an active plan) (*)\
					\nPlease note: options annotated with (*) are only for entities under active plans",
				is_valid=lambda user_input: user_input.isdigit() and int(user_input) > 0 and int(user_input) <= 4,
				validation_message="Unrecognized input. Please choose from the above list.")
		
		if option == "1":
			return
		if option == "2":
			self.prompt_display_specific_camp()
		if option == "3":
			self.prompt_update_resources()
		if option == "4":
			self.prompt_change_resources("add")
	
	def prompt_display_all_camps(self):
		print('Resources for all camp(s) under active plan(s):')
		df = pd.DataFrame(CampResources.load_active_resources())
		df_tranpose = df.to_string()  # to_string: prevent table truncation
		print(df_tranpose)
		print("----------------------------------End of resources table-------------------------------------")
		input("Press Enter to continue...")

	@staticmethod
	def count_occupancy(camp_id): #scan the refugee json file
		count = 0
		refugees = load_ALL_refugees()
		for refugee in refugees:
			if refugees[refugee]["camp_id"] == camp_id:
				count+=1
		return count


	def print_exist_camp(self):
		df = pd.DataFrame(CampResources.load_active_resources())
		df_tranpose = df.transpose()
		column_names = df.columns.tolist()
		df_camp = pd.DataFrame({'camp name': column_names})
		print(df_camp)

	def prompt_display_specific_camp(self):
		users = Users.load_users()
		is_admin = users[self.current_user.username]["is_admin"]

		filtered_camps = Camp.load_active_camps_user_has_access_to(self.current_user.username)
		message_key = "\nExisting camp(s) under active plan(s):" if is_admin else "Camp(s) you have access rights to (under active plans):"
		message_value = ", ".join(list(filtered_camps.keys())) if filtered_camps else "None found"
		print(f"{message_key} {message_value}")

		if is_admin:
			camp_id = input_until_valid(
				input_message = "Enter the camp name, or leave empty to abort: ", 
				is_valid = lambda user_input: (user_input == "") or (user_input in CampResources.load_active_resources()), 
				validation_message = "Unrecognized camp. Please enter a new one, or leave empty to abort: ")
			
			if camp_id == "":
				print("Aborted displaying resources.")
				return

			resource_sepecific_camp = CampResources()
			resource_sepecific_camp.display_active_resources(camp_id)
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
			resource_sepecific_camp.display_active_resources(camp_id)
			print("-------End of resource details--------")
			input("Press Enter to continue...")
		

	def prompt_change_resources(self, method='update'):
		users = Users.load_users()
		is_admin =  users[self.current_user.username]["is_admin"]

		filtered_ALL_camps = Camp.load_active_camps_user_has_access_to(self.current_user.username)
		message_key = "\nExisting camp(s) under active plan(s):" if is_admin else "Camp(s) you have access rights to (under active plans):"
		message_value = ", ".join(list(filtered_ALL_camps.keys())) if filtered_ALL_camps else "None found"
		print(f"{message_key} {message_value}")

		if is_admin:
			validation_message = "Unrecognized camp. Please enter a new one or leave empty to abort: "
		else:
			validation_message = "Unrecognized camp or you do not have access rights. Please enter a new one or leave empty to abort: "

		camp_id = input_until_valid(input_message="Enter the camp name or leave empty to abort: ", 
						is_valid=lambda user_input:(user_input == "") or user_input in filtered_ALL_camps, 
						validation_message=validation_message)
		
		if camp_id =="":
			print("Aborted resource amount modification.")
			return

		if InterfaceManageResource.Test_underthreshold(camp_id):
			InterfaceManageResource.helper_print_warning(camp_id)

		camp_population = get_num_families_and_members_by_camp()
		num_family = camp_population[camp_id]['num_families']
		num_members = camp_population[camp_id]['num_members']
		
		#todo: present the population of the camp.
		df = pd.DataFrame(CampResources.load_active_resources()).transpose()
		print("detailed information of this camp:")
		print(df.loc[camp_id])
		not_exit = True
		while not_exit:
			resource_to_edit = input_until_valid(input_message="Enter the resource to edit: food_packets/medical_packets/water_packets/shelter_packets/clothing_packets/first_aid_packets/baby_packet/sanitation_packets), or leave empty to abort:",
												is_valid=lambda user_input: user_input in CampResources.load_active_resources()[camp_id] or user_input == "",
												validation_message="Unrecognized input. Please enter again.")
			if resource_to_edit == "":
				print("Aborted resource amount modification.")
				return
			
			# new_amount = input_until_valid(input_message= f"Enter the new amount for {resource_to_edit} or leave empty to abort: ",
			# 										is_valid=lambda user_input: user_input.isdigit() or user_input == "",
			# 										validation_message="Unrecognized input. Please enter again.")
			# 	if new_amount == "":
			# 		print("Aborted resource amount modification.")
			# 		return
			
			
			amount_edit = input_until_valid(input_message= f"Enter the new amount for {resource_to_edit} or press enter to return: ",
												is_valid=lambda user_input: user_input.isdigit() or user_input == "",
												validation_message="Unrecognized type, please enter again.")
			# if amount_edit == "":
			# 	print("edition aborted.")
			# 	return
			
			# confirm = input_until_valid(input_message="Please confirm your edition for change "+resource_to_edit+ "to amount"+ amount_edit+" \n[y] Yes\n[n] No (abort)",
			# 							is_valid = lambda user_input: user_input == "y" or user_input == "n",
			# 							validation_message="Unrecognized input. Please confirm (y/n):\n[y] Yes\n[n] No (abort)")
			
			# if confirm == "n":
			# 	print(f"Camp information modification aborted.")
			# 	return
			# resource = CampResources()
			# test = resource.update_resources(camp_id,resource_to_edit,int(amount_edit))


			if method == 'update':
				confirm = input_until_valid(input_message=f"Please confirm your edition for change {resource_to_edit} to amount {amount_edit} \n[y] Yes\n[n] No (abort)",
										is_valid = lambda user_input: user_input == "y" or user_input == "n",
										validation_message="Unrecognized input. Please confirm (y/n):\n[y] Yes\n[n] No (abort)")
				if confirm == "n":
					print(f"Camp information modification aborted.")
					return          
				resource = CampResources()
				test = resource.update_resources(camp_id,resource_to_edit,int(amount_edit))
			else:  # method == 'add'
				confirm = input_until_valid(input_message=f"Please confirm your edition for adding {amount_edit} to {resource_to_edit} \n[y] Yes\n[n] No (abort)",
										is_valid = lambda user_input: user_input == "y" or user_input == "n",
										validation_message="Unrecognized input. Please confirm (y/n):\n[y] Yes\n[n] No (abort)")
				if confirm == "n":
					print(f"Camp information modification aborted.")
					return
				resource = CampResources()
				test = resource.adjust_resources(camp_id,resource_to_edit,int(amount_edit))
			



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

		


		


		


	@staticmethod 
	def calculate_threshold(resource_name,camp_id):
		resources = CampResources()
		refugee_count_dict = get_num_families_and_members_by_camp()
		num_refugees= refugee_count_dict[camp_id]["num_members"]
		factor = resources.resource_factor()
		threshold = num_refugees*factor[resource_name]*resources.warning_days
		return threshold
	
	@staticmethod
	def Test_underthreshold(camp_id):
		"""helper method for determine which camp to warning

		return boolean value: true if underthreshold"""
		resources = CampResources.load_ALL_resources()
		test = False
		for resource in resources[camp_id]:
			if resources[camp_id][resource]<InterfaceManageResource.calculate_threshold(resource,camp_id):
				test = True
		return test
	
	@staticmethod
	def helper_print_warning(camp_id):
		"""helper method for print warning camp details"""
		resources = CampResources.load_ALL_resources()
		print("-"*25+"warning"+"-"*25)
		print(f'warning: {camp_id} may face risk of resource shortage.\n  The resource in shortage is:')
		for resource in resources[camp_id]:
			amount = resources[camp_id][resource]
			warning_amount = InterfaceManageResource.calculate_threshold(resource,camp_id)
			if amount<warning_amount:
				print(f' |{resource}: current amount {amount}. warning level: {warning_amount}')
		print("-"*25+"warning"+"-"*25+'\n')

				


	@staticmethod
	def print_warning_level_helper():
		resources = CampResources()
		factor = resources.resource_factor()
		print('-'*29+'warning level'+'-'*29)
		width = 20
		border_char = "||"
		padding_char = " "
		for resource in factor.keys():
			amount = factor[resource]
			text = f'The warning level for {resource} is {amount} per person per day.'
			left_aligned = text.ljust(width)
			left_border = border_char + left_aligned + padding_char*(70-len(text)) +border_char
			print(left_border)
		print('||'+' '*14+'the warning level of day time is '+str(resources.warning_days)+'.'+' '*16+'||')
		print('-'*29+'warning level'+'-'*29)


	def prompt_resource_warning(self):
		print('warning for camps facing risk of shortage:\n')
		for camp_id in CampResources.load_active_resources():
			if InterfaceManageResource.Test_underthreshold(camp_id):
				InterfaceManageResource.helper_print_warning(camp_id)

		InterfaceManageResource.print_warning_level_helper()
		change = input_until_valid(input_message="Do you want to current warning factors? (Press 'enter' to return) \n[y] Yes\n[n] No (abort)",
										is_valid = lambda user_input: user_input == "y" or user_input == "n",
										validation_message="Unrecognized input. Please confirm (y/n):\n[y] Yes\n[n] No (abort)")
		
		if change == "":
			return

		print("reset factors (Press 'Enter to go retrieve')")
		resource_reset = CampResources()
		factor_reset_amounts = {}
		for resource in resource_reset.resource_factor().keys():
			reset = input_until_valid(input_message= resource +": ", is_valid=lambda user_input: user_input.isdigit() and int(user_input)>=0 or user_input == "",
									   validation_message="Please input Non-negative intergers.or press enter to exit directly ")
			if reset == "":
				return
			factor_reset_amounts[resource] = int(reset)
		reset = input_until_valid(input_message= "warning days: ", is_valid=lambda user_input: user_input.isdigit() and int(user_input)>=0 or user_input == "",
									   validation_message="Please input possitive intergers.or press enter to exit directly ")
		if reset == "":
			return
		factor_reset_amounts["warning_days"] = int(reset)
	   
		print(factor_reset_amounts)
		confirm = input_until_valid(input_message="Please confirm your reset warning factors. \n" +" \n[y] Yes\n[n] No (abort)",
										is_valid = lambda user_input: user_input == "y" or user_input == "n",
										validation_message="Unrecognized input. Please confirm (y/n):\n[y] Yes\n[n] No (abort)")
		if confirm == "n":
			print(f"Edition aborted.")
			return
		
		test = CampResources.reset_factor(factor_reset_amounts)

		if test:
			print(f"You've changed the warning factors successfully!")
		else:
			print(f'Failed to change.')
		
		
	
# resource = InterfaceManageResource('admin')
# resource.prompt_resource_warning()
		



