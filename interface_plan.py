import pandas as pd
from datetime import datetime

from interface_helper import input_until_valid, is_valid_date
from plans import Plans
from data_validator import DataValidator

class InterfacePlan:
	def __init__(self, current_user):
		self.current_user = current_user
	
	def prompt_admin_options(self):		
		option = input_until_valid(
			
			input_message = f"\n<homepage/manage-plans>\nPlease choose a plan management option below:\
				\n[1] CANCEL\
				\n[2] List plans (active/ended/all)\
				\n[3] Create new humanitarian plan\
				\n[4] Modify a humanitarian plan\
				\n[5] Immediately end a humanitarian plan\
				\n[6] Reactivate a humanitarian plan\
				\n[7] Delete a humanitarian plan",
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
			self.prompt_modify_plan()
		if option == "5":
			self.prompt_immediate_end_plan()
		if option == "6":
			self.prompt_reactivate_plan()

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
			input_message = "\nEnter location of the emergency (This should be a country name e.g. Belgium):",
			is_valid = lambda location: DataValidator.validate_country(location) is True,
			validation_message = "Location must be a valid country. Please re-enter the location of the emergency."
		)
		start_date = input_until_valid(
			input_message = "\nEnter the plan start date in the format dd/mm/yyyy:",
			is_valid = lambda start_date: is_valid_date(start_date),
			validation_message = "Invalid date format. Please re-enter the date in the format dd/mm/yyyy."
		)
		end_date = input_until_valid(
			input_message = "\nEnter the plan end date in the format dd/mm/yyyy: \nNote:\nFor active plans please enter a future date. \nIf this is an old plan, you can archive it by adding its end date.",
			is_valid = lambda end_date: is_valid_date(end_date),
			validation_message = "Invalid date format. Please re-enter the date in the format dd/mm/yyyy."
		)

		confirm = input_until_valid(
			input_message = f"Please confirm details of the new plan (y/n):\
				\nPlan name: {plan_name}\
				\nPlan Description: {description}\
				\nPlan Location: {location}\
				\nPlan Start Date: {start_date}\
				\nPlan End Date: {end_date}",
			is_valid=lambda user_input: user_input == "y" or user_input == "n",
			validation_message="Unrecognized input. Please confirm details of the new user (y/n):\n[y] Yes\n[n] No (abort)"
			)
		if confirm == "y":
			plans = Plans()
			success = plans.add_plan(
				plan_name=plan_name, description=description, location=location, start_date=start_date, end_date=end_date)
			if success:
				print(f"Plan for {plan_name} successfully added.")
			else:
				print(f"Failed to add plan for {plan_name}")
		else:
			print(f"Aborted plan creation.")

	def prompt_list_plans(self):
		option = input_until_valid(
			
			input_message = f"\n<homepage/manage-plans/list-plans>\nPlease choose an option below:\
				\n[1] CANCEL\
				\n[2] List active plans\
				\n[3] List ended plans\
				\n[4] List all plans",
			is_valid=lambda user_input: user_input.isdigit() and int(user_input) > 0 and int(user_input) <= 4,
			validation_message="Unrecognized input. Please choose from the above list."
		)
		if option == "1":
			return  # option 1 is cancel, so just return
		if option == "2":
			self.prompt_list_active_plans()
		if option == "3":
			self.prompt_list_ended_plans()
		if option == "4":
			self.prompt_list_all_plans()
	
	def prompt_list_active_plans(self):
		plans = Plans.load_plans()
		active_plans = {key: value for key, value in plans.items() if value.get("status") == "Active"}
		if active_plans:
			print("--- Active plans are as follows ---")
			active_plans_df = pd.DataFrame.from_dict(active_plans).transpose()
			print(active_plans_df)
			print("--- End of plans list ---")
		else:
			print("--- No active plans logged on system ---")
		input("Press Enter to continue...")

	def prompt_list_ended_plans(self):
		plans = Plans.load_plans()
		ended_plans = {key: value for key, value in plans.items() if value.get("status") == "Ended"}
		if ended_plans:
			print("--- Ended plans are as follows ---")
			ended_plans_df = pd.DataFrame.from_dict(ended_plans).transpose()
			print(ended_plans_df)
			print("--- End of plans list ---")
		else:
			print("--- No ended plans logged on system ---")
		input("Press Enter to continue...")
		
	def prompt_list_all_plans(self):
		# create pandas dataframe from dictionary
		plans = Plans.load_plans()
		if plans:
			print("--- All plans are as follows ---")
			plans_df = pd.DataFrame.from_dict(plans).transpose()
			print(plans_df)
			print("--- End of plans list ---")
		else:
			print("--- No plans logged on system. Please add a plan ---")
		input("Press Enter to continue...")
	
	def prompt_modify_plan(self):
		self.prompt_list_all_plans()
		plan_keys = Plans.load_plans().keys()
		# Promps input from user
		plan_name = input_until_valid(
			input_message="Enter the plan you want to modify or leave empty to abort:",
			is_valid = lambda user_input: user_input == "" or user_input in plan_keys,
			validation_message= "This plan does not exist. Please re-enter plan name from the list above, create a new plan with this name, or leave empty to abort."
		)
		
		if plan_name == "":
			print("User modification aborted.")
			return  # returns from method to abort current method
		
		print("\nCurrent values of the selected plan:")
		print(f"-> plan_name: {plan_name}")
		selected_plan = Plans.load_plans()[plan_name]
		for field, val in selected_plan.items():
			print(f"-> {field}: {val}")
		
		attribute = input_until_valid(
			input_message = "Enter the attribute (plan_name/description/location/start_date/end_date) to modify:",
			is_valid = lambda user_input: user_input in {"plan_name", "description", "location", "start_date", "end_date"},
			validation_message = "Unrecognized input. Please enter a valid field (plan_name/description/location/start_date/end_date)."
			)

			# TODO: also add the code for updating camp that plan is under (update their plan_name from previous value to newer value)
		if attribute == "plan_name":
			new_value = input_until_valid(
			input_message = "\nEnter new plan name. This should be the name of the emergency occuring (E.g. Ukraine War) and must be different from existing plans. Leave empty to abort:",
			is_valid = lambda plan_name: plan_name == "" or plan_name not in plan_keys,
			validation_message = "Plan name already exists. Please enter a different plan name."
		)
		elif plan_name == "":
			print("Plan creation aborted.")
			return

		elif attribute == "description":
			new_value = input_until_valid(
			input_message = "\nEnter new plan description:",
			is_valid = lambda description: description != "",
			validation_message = "Plan description cannot be empty. Please enter a plan description."
		)
		
		elif attribute == "location":
			new_value = input_until_valid(
			input_message = "\nEnter the new location of the emergency (This should be a country name e.g. Belgium):",
			is_valid = lambda location: DataValidator.validate_country(location) is True,
			validation_message = "Location must be a valid country. Please re-enter the location of the emergency."
		)
		
		elif attribute == "start_date":
			new_value = input_until_valid(
			input_message = "\nEnter the plan's new start date in the format dd/mm/yyyy:",
			is_valid = lambda start_date: is_valid_date(start_date),
			validation_message = "Invalid date format. Please re-enter the date in the format dd/mm/yyyy."
		)

		elif attribute == "end_date":
			new_value = input_until_valid(
			input_message = "\nEnter the plan's new end date in the format dd/mm/yyyy:",
			is_valid = lambda end_date: is_valid_date(end_date),
			validation_message = "Invalid date format. Please re-enter the date in the format dd/mm/yyyy."
		)

		else:  
			# TODO: location -> implement country checks from hashset
			print(f"\nCurrent {attribute} value: {self.prompt_list_plans()[plan_name][attribute]}")
			new_value = input_until_valid(f"Enter the new value for the {attribute}:")

		confirm = input_until_valid(
			input_message = f"Please confirm you want to change {attribute} from previous value to new value:\n |{plan_name if attribute == "plan_name" else Plans.load_plans()[plan_name][attribute]}| --> |{new_value}| \n[y] Yes\n[n] No (abort)",
			is_valid = lambda user_input: user_input == "y" or user_input == "n",
			validation_message = "Unrecognized input. Please confirm (y/n):\n[y] Yes\n[n] No (abort)"
		)

		if confirm == "n":
			print(f"Plan information modification aborted.")
			return

		if attribute == "plan_name":
			test = Plans.modify_plan_name(plan_name = plan_name, new_name = new_value)
		else:
			test = Plans.modify_plan(plan_name = plan_name, field = attribute, new_value = new_value)
		
		if test:
			print(f"You've changed the {attribute} successfully! Your changes can now be seen:")
			print(f"-> plan_name: {plan_name}")
			selected_plan = Plans.load_plans()[plan_name]
			for field, val in selected_plan.items():
				print(f"-> {field}: {val}")
		else:
			print(f'Failed to change {attribute}')

	def prompt_immediate_end_plan(self):
		self.prompt_list_active_plans()
		plans = Plans.load_plans()
		active_plans = {key: value for key, value in plans.items() if value.get("status") == "Active"}
		active_plan_keys = active_plans.keys()
		# Promps input from user
		plan_name = input_until_valid(
			input_message="Enter the plan you want to immediately end or leave empty to abort:",
			is_valid = lambda user_input: user_input == "" or user_input in active_plan_keys,
			validation_message= "This plan has already ended or does not exist. Please re-enter a plan name from the active plans listed above, or leave empty to abort."
		)
		
		if plan_name == "":
			print("User modification aborted.")
			return  # returns from method to abort current method
		
		print("\nCurrent values of the plan you are ending:")
		print(f"-> plan_name: {plan_name}")
		selected_plan = Plans.load_plans()[plan_name]
		for field, val in selected_plan.items():
			if field != "end_date" and field != "status":
				print(f"-> {field}: {val}")
		for field, val in selected_plan.items():
			if field == "end_date":
				print(f"-> original end date: {val}")
		
		confirm = input_until_valid(
			input_message = f"Please confirm you want to end {plan_name}\n[y] Yes\n[n] No (abort)",
			is_valid = lambda user_input: user_input == "y" or user_input == "n",
			validation_message = "Unrecognized input. Please confirm (y/n):\n[y] Yes\n[n] No (abort)"
		)

		if confirm == "n":
			print(f"Plan termination aborted.")
			return
		
		now = datetime.now()
		test = Plans.modify_plan(plan_name = plan_name, field = "end_date", new_value = now.strftime('%d/%m/%Y'))
		
		if test:
			print(f"You've successfully ended the following plan: {plan_name}\
				\nHere is a list of your ended plans:")
			self.prompt_list_ended_plans()
		else:
			print(f'Failed to end {plan_name}')


		
	