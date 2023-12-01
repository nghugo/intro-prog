import pandas as pd

from interface_helper import input_until_valid, is_valid_date
from plans import Plans
from users import Users
from interface_camp_options import InterfaceCampOptions
from interface_manage_users import InterfaceManageUsers
from interface_generate_reports import InterfaceGenerateReports
from plans import Plans

class InterfaceAdminOptions:
	def __init__(self, users, current_user):
		self.users = users
		self.current_user = current_user
		self.interface_manage_users = InterfaceManageUsers(self.users, self.current_user)
		self.interface_generate_reports = InterfaceGenerateReports()
		self.interface_camp_options = InterfaceCampOptions(self.users, self.current_user)
		# initialise self.plans
		self.plans = Plans()


	def show_options(self, option):
		# option 1 is log out, which is handled at interface_main.py
		if option == "2":
			self.interface_manage_users.show_admin_options()
		if option == "3":
			self.prompt_create_plan()
		if option == "4":
			self.prompt_list_plans()
		if option == "5":
			self.interface_generate_reports.show_admin_options()
		if option == "6":
			self.interface_camp_options.show_camp_options(self.users, self.current_user)


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



	def prompt_list_plans(self):
		print("--- Plans are as follows ---")
		# create pandas dataframe from dictionary (self.plans.plans dict in .json file)
		plans_df = pd.DataFrame.from_dict(self.plans.plans).transpose()
		print(plans_df)
		print("--- End of plans list ---")
		input("Press Enter to continue...")
	
	

			
