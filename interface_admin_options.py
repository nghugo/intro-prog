import pandas as pd

from interface_helper import input_until_valid, is_valid_date
from plans import Plans
from users import Users
from interface_camp_options import InterfaceCampOptions
from interface_modify_users import InterfaceModifyUsers
from interface_generate_reports import InterfaceGenerateReports
from plans import Plans

class InterfaceAdminOptions:
	def __init__(self, users, current_user):
		self.users = users
		self.current_user = current_user
		self.interface_modify_users = InterfaceModifyUsers(self.users, self.current_user)
		self.interface_generate_reports = InterfaceGenerateReports()
		# initialise self.plans
		self.plans = Plans()

	def execute_option(self, option):
		# option 1 is log out, which is handled at interface_main.py
		if option == "2":
			self.execute_manage_users_options()
		if option == "3":
			self.prompt_create_plan()
		if option == "4":
			self.prompt_list_plans()
		if option == "5":
			self.execute_generate_reports_options()
		if option == "6":
			self.execute_camp_options()
			
	def execute_manage_users_options(self):
		option = input_until_valid(
			# when extending this list, make sure the input message matches the is_valid validation function and the options in interface_admin_options.py
			input_message = f"\n<homepage/manage-users>\nPlease choose a user management option below:\
				\n[1] CANCEL (return to homepage)\
				\n[2] Add user\
				\n[3] Delete user\
				\n[4] Activate user\
				\n[5] Deactivate user\
				\n[6] Modify user\
				\n[7] List all users",
			is_valid=lambda user_input: user_input.isdigit() and int(user_input) > 0 and int(user_input) <= 7,
			validation_message="Unrecognized input. Please choose from the above list."
		)
		if option == "1":
			return  # option 1 is cancel, so just return
		if option == "2":
			self.interface_modify_users.prompt_add_user()
		if option == "3":
			self.interface_modify_users.prompt_delete_user()
		if option == "4":
			self.interface_modify_users.prompt_activate_user()
		if option == "5":
			self.interface_modify_users.prompt_deactivate_user()
		if option == "6":
			self.interface_modify_users.prompt_modify_user()
		if option == "7":
			self.interface_modify_users.list_users()

	
	def prompt_create_plan(self):
		plan_name = input_until_valid(
			input_message = "\nEnter plan name. This should be the name of the emergency occuring (E.g. Ukraine War):",
			is_valid = lambda plan_name: plan_name != "",
			validation_message = "plan name cannot be empty. Please enter an plan name."
		)
		description = input_until_valid(
			input_message = "\nEnter plan description:",
			is_valid = lambda description: description != "",
			validation_message = "Plan description cannot be empty. Please enter a plan description."
		)
		location = input_until_valid(
			input_message = "\nEnter location of the emergency:",
			is_valid = lambda location: location != "",
			validation_message = "Location cannot be empty. Please enter the location of the emergency."
		)
		start_date = input_until_valid(
			input_message = "\nEnter the plan start date in the format dd/mm/yyyy:",
			is_valid = lambda start_date: is_valid_date(start_date),
			validation_message = "Invalid date format. Please re-enter the date in the format dd/mm/yyyy."
		)
		confirm = input_until_valid(
			input_message = f"""Please confirm details of the new plan (y/n):\n
			Plan name: {plan_name}\n
			Plan Description: {description}\n
			Plan Location: {location}\n
			Plan Start Date: {start_date}""",
			is_valid=lambda user_input: user_input == "y" or user_input == "n",
			validation_message="Unrecognized input. Please confirm details of the new user (y/n):\n[y] Yes\n[n] No (abort)"
			)
		if confirm == "y":
			plans = Plans()
			success = plans.add_plan(
				plan_name=plan_name, description=description, location=location, start_date=start_date)
			if success:
				print(f"Plan for {plan_name} successfully added.")
			else:
				print(f"Failed to add plan for {plan_name}")
		else:
			print(f"Aborted plan creation.")

	def execute_camp_options(self):
		"""bring up a menu for camp functions """
		users = Users()
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
		
		interface_camp_options = InterfaceCampOptions(users, self.current_user)
		interface_camp_options.execute_option(option)
	def prompt_list_plans(self):
		print("--- Plans are as follows ---")
		# create pandas dataframe from dictionary (self.plans.plans dict in .json file)
		plans_df = pd.DataFrame.from_dict(self.plans.plans).transpose()
		print(plans_df)
		print("--- End of plans list ---")
		input("Press Enter to continue...")
	
	def execute_generate_reports_options(self):
		option = input_until_valid(
			# when extending this list, make sure the input message matches the is_valid validation function and the options in interface_admin_options.py
			#                 
			input_message = f"\n<homepage/report>\nPlease choose a report to generate below:\
				\n[1] CANCEL (return to homepage)\
				\n[2] Specific plan (not yet implemented)\
				\n[3] All plans (not yet implemented)\
				\n[4] Specific camp\
				\n[5] All camps",
			is_valid=lambda user_input: user_input.isdigit() and int(user_input) > 0 and int(user_input) <= 5,
			validation_message="Unrecognized input. Please choose from the above list."
		)
		if option == "1":
			return  # option 1 is cancel, so just return
		if option == "2":
			pass # TODO
		if option == "3":
			pass # TODO
		if option == "4":
			self.interface_generate_reports.generate_camp_report()
		if option == "5":
			self.interface_generate_reports.generate_overall_report()

			
