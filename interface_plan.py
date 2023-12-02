import pandas as pd

from interface_helper import input_until_valid, is_valid_date
from plans import Plans

class InterfacePlan:
	def __init__(self, current_user):
		self.current_user = current_user
	
	def prompt_admin_options(self):		
		option = input_until_valid(
			
			input_message = f"\n<homepage/manage-plans>\nPlease choose a plan management option below:\
				\n[1] CANCEL\
				\n[2] Display details of all plans\
				\n[3] Create new humanitarian plan\
				\n[4] TODO: Edit a humanitarian plan\
				\n[5] TODO: Remove a humanitarian plan\
				\n[6] TODO\
				\n[7] TODO",
			is_valid=lambda user_input: user_input.isdigit() and int(user_input) > 0 and int(user_input) <= 5,
			validation_message="Unrecognized input. Please choose from the above list."
		)
		if option == "1":
			return  # option 1 is cancel, so just return
		if option == "2":
			self.prompt_list_plans()
		if option == "3":
			self.prompt_create_plan()
		if option == "4":
			pass
		if option == "5":
			pass

	def prompt_create_plan(self):
		
		plan_keys = Plans.load_plans().keys()
		print(f"\nExisting plans(s): {", ".join(plan_keys) if plan_keys else 'None found'}")

		plan_name = input_until_valid(
			input_message = "\nEnter plan name. This should be the name of the emergency occuring (E.g. Ukraine War) and must be different from existing plans. Leave empty to abort:",
			is_valid = lambda plan_name: plan_name == "" or plan_name not in plan_keys,
			validation_message = "Plan name already exists. Please enter a different plan name."
		)
		if plan_name == "":
			print("Plan creation aborted.")
			return

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
			input_message = f"Please confirm details of the new plan (y/n):\
				\nPlan name: {plan_name}\
				\nPlan Description: {description}\
				\nPlan Location: {location}\
				\nPlan Start Date: {start_date}",
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
		# create pandas dataframe from dictionary
		plans = Plans.load_plans()
		plans_df = pd.DataFrame.from_dict(plans).transpose()
		print(plans_df)
		print("--- End of plans list ---")
		input("Press Enter to continue...")