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
		self.resources = CampResources().resources
		
	def prompt_admin_options(self):
		option = input_until_valid(
				input_message = f"\n<homepage/manage-resources>\nPlease choose a resource management option below:\
					\n[1] CANCEL\
					\n[2] List all resource profiles under all camps (*)\
					\n[3] List all resource profiles under a specific camp (*)\
					\n[4] Set (overwrite) resource amounts in a specific camp (*)\
					\n[5] Increment resource amounts in a specific camp (*)\
					\n[6] Display camps with insufficient resources/ Change resource warning thresholds (*)\
					\nPlease note: Options annotated with (*) are only for entities under active plans.",
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
			self.prompt_resource_warning(is_admin = True)
		
	def prompt_volunteer_options(self):
		option = input_until_valid(
				input_message = f"\n<homepage/manage-resources>\
					\nPlease choose a resource management option below:\
					\n[1] CANCEL\
					\n[2] List all resource profiles under a specific camp\
					\n[3] Set (overwrite) resource amounts in a specific camp\
					\n[4] Increment resource amounts in a specific camp\
					\n[5] Display camps with insufficient resources/ View resource warning thresholds",
				is_valid=lambda user_input: user_input.isdigit() and int(user_input) > 0 and int(user_input) <= 5,
				validation_message="Unrecognized input. Please choose from the above list.")
		
		if option == "1":
			return
		if option == "2":
			self.prompt_display_specific_camp()
		if option == "3":
			self.prompt_change_resources('update')
		if option == "4":
			self.prompt_change_resources("add")
		if option == "5":
			self.prompt_resource_warning(is_admin = False)
	
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
		
		camp_population = get_num_families_and_members_by_camp()
		num_family = camp_population[camp_id]['num_families']
		num_members = camp_population[camp_id]['num_members']

		if InterfaceManageResource.Test_underthreshold(camp_id):
			InterfaceManageResource.helper_print_warning(camp_id, num_members)

		
		#todo: present the population of the camp.
		df = pd.DataFrame(CampResources.load_active_resources()).transpose()
		print("detailed information of this camp:")
		print(df.loc[camp_id])
		not_exit = True
		
		while not_exit:
			resource_to_edit = input_until_valid(input_message="Enter the resource to edit: food_packets/medical_packets/water_packets/shelter_packets/clothing_packets/sanitation_packets), or leave empty to abort:",
												is_valid=lambda user_input: user_input in CampResources.load_active_resources()[camp_id] or user_input == "",
												validation_message="Unrecognized input. Please enter again.")
			if resource_to_edit == "":
				print("Aborted resource amount modification.")
				return
			
			if method == 'update':
				input_msg = f"Enter the new amount for {resource_to_edit} or leave empty to abort: "
			else:
				input_msg = f"Enter the increment amount for {resource_to_edit} or leave empty to abort: "
			
			amount_edit = input_until_valid(input_message= input_msg,
												is_valid=lambda user_input: user_input.isdigit() or user_input == "",
												validation_message="Unrecognized input. Please enter again.")
			if amount_edit == "":
				print("Aborted resource amount modification.")
				return


			if method == 'update':
				confirm = input_until_valid(input_message=f"Please confirm that you want to set the amount of {resource_to_edit} to {amount_edit} \n[y] Yes\n[n] No (abort)",
										is_valid = lambda user_input: user_input == "y" or user_input == "n",
										validation_message="Unrecognized input. Please confirm (y/n):\n[y] Yes\n[n] No (abort)")
				if confirm == "n":
					print(f"Camp information modification aborted.")
					return          
				resource = CampResources()
				test = resource.overwrite_resources_amount(camp_id,resource_to_edit,int(amount_edit))
			else:  # method == 'add'
				
				current_resource_amount = int(CampResources.load_ALL_resources()[camp_id][resource_to_edit])

				confirm = input_until_valid(input_message=f"Please confirm that you want to add {amount_edit} units of {resource_to_edit} (result: {int(amount_edit) + current_resource_amount}) \n[y] Yes\n[n] No (abort)",
										is_valid = lambda user_input: user_input == "y" or user_input == "n",
										validation_message="Unrecognized input. Please confirm (y/n):\n[y] Yes\n[n] No (abort)")
				if confirm == "n":
					print(f"Camp information modification aborted.")
					return
				resource = CampResources()
				test = resource.increment_resources_amount(camp_id,resource_to_edit,int(amount_edit))
			

			if test:
				print(f"You've changed the {resource_to_edit} amount successfully!")
			else:
				print(f'Failed to change {resource_to_edit} amount')

			if method == 'update':
				exit_msg = f"Do you want to update (overwrite) other resource amounts?\n[y] Yes\n[n] No (leave)"
			else:
				exit_msg = f"Do you want to increment other resource amounts?\n[y] Yes\n[n] No (leave)"

			exit_confirm = input_until_valid(input_message=exit_msg,
										is_valid = lambda user_input: user_input == "y" or user_input == "n",
										validation_message="Unrecognized input. Please confirm (y/n):\n[y] Yes\n[n] No (leave)")
			
			if exit_confirm == 'y':
				not_exit = True
			else:
				not_exit = False
	@staticmethod 
	def calculate_threshold(resource_name,camp_id):
		"""calculate the set resource threshold
		with algorithm: threshold = population*resource_factors*warning_days
		----------------------------
		return threshold(int)
		"""
		resources = CampResources()
		refugee_count_dict = get_num_families_and_members_by_camp()
		num_refugees= refugee_count_dict[camp_id]["num_members"]
		factor = resources.resource_factor()
		factor_day = resources.factors
		threshold = num_refugees*factor[resource_name]
		return threshold
	@staticmethod
	def Test_underthreshold(camp_id):
		"""helper method for determine which camp to warning
		-------------------------------
		return boolean value: true if underthreshold"""
		resources = CampResources.load_active_resources()
		test = False
		for resource in resources[camp_id]:
			if resources[camp_id][resource] < InterfaceManageResource.calculate_threshold(resource,camp_id):
				test = True
		return test
	
	@staticmethod
	def helper_print_warning(camp_id, num_refugees):
		"""helper method for print warning camp details"""
		resources = CampResources.load_active_resources()
		print("-"*29+"Warning"+"-"*29)
		print(f'Warning: {camp_id} with {num_refugees} refugee(s) may face resource shortage\nResources with amount lower than threshold are:')
		for resource in resources[camp_id]:
			amount = resources[camp_id][resource]
			warning_amount = InterfaceManageResource.calculate_threshold(resource,camp_id)
			if amount<warning_amount:
				print(f'-> {resource :20} current amount: {str(amount):6} min threshold: {warning_amount}')
		print("-"*65+'\n')
	@staticmethod
	def print_warning_level_helper():
		resources = CampResources()
		factor = resources.resource_factor()
		print('-'*26+'Current thresholds'+'-'*26)
		width = 20
		border_char = "||"
		padding_char = " "
		for resource in factor:
			amount = factor[resource]
			text = f'The min threshold for {resource+":":21} {amount} per refugee'
			left_aligned = text.ljust(width)
			left_border = border_char + " "*4 + left_aligned + padding_char*(60-len(text)) +border_char
			print(left_border)
		print('-'*70+'\n')
	
	def prompt_resource_warning(self, is_admin):
			
			if is_admin:
				print('Camps facing risk of shortage:\n')
			else:
				print('Camps accessible by you facing risk of shortage:\n')
			active_accessible_camps = Camp.load_active_camps_user_has_access_to(self.current_user.username)
			
			camp_lower_than_threshold_found = False

			for camp_id in active_accessible_camps:
				refugee_count_dict = get_num_families_and_members_by_camp()
				if InterfaceManageResource.Test_underthreshold(camp_id):
					num_refugees= refugee_count_dict[camp_id]["num_members"]
					InterfaceManageResource.helper_print_warning(camp_id, num_refugees)
					camp_lower_than_threshold_found = True
			
			if not camp_lower_than_threshold_found:
				if is_admin:
					print("None found. No camps face risk of shortage.\n")
				else:
					print("None found. No camps accessible by you face risk of shortage.\n")
				
			InterfaceManageResource.print_warning_level_helper()

			if not is_admin:
				input("Press Enter to continue...")
				return

			
			confirm = input_until_valid(input_message="Do you want to edit the thresholds? \n[y] Yes \n[n] No ",
											is_valid = lambda user_input: user_input == "y" or user_input == "n",
											validation_message="Unrecognized input.")
			
			if confirm == "n":
				return
		
			resource_reset = CampResources()
			factor_reset_amounts = {}
			for resource in resource_reset.resource_factor().keys():
				reset = input_until_valid(input_message= f"Please enter the new threshold for {resource}:", 
							is_valid=lambda user_input: user_input.isdigit() and int(user_input)>=0,
							validation_message="Threshold must be a non-negative integer. Please re-enter.")
				factor_reset_amounts[resource+"_factor"] = int(reset)
			
			print("Your inputted thresholds:")
			print(pd.DataFrame.from_dict(factor_reset_amounts,orient="index",columns=["factor"]))
			confirm = input_until_valid(input_message="Please confirm the new thresholds. \n" +" \n[y] Yes\n[n] No (abort)",
											is_valid = lambda user_input: user_input == "y" or user_input == "n",
											validation_message="Unrecognized input. Please confirm the new thresholds (y/n):\n[y] Yes\n[n] No (abort)")
			if confirm == "n":
				print(f"Resource threshold modification aborted.")
				return
			
			test= CampResources.reset_factor(factor_reset_amounts)

			if test:
				print(f"You've changed the resource thresholds successfully!")
			else:  
				print(f'Failed to change.')