import json 

from interface_helper import input_until_valid, is_valid_date
from interface_modify_users import InterfaceModifyUsers
from plans import Plans

class InterfaceAdminOptions:
    def __init__(self, users, current_user):
        self.users = users
        self.current_user = current_user
        self.interface_modify_users = InterfaceModifyUsers(self.users, self.current_user)

    def execute_option(self, option):
        # option 1 is log out, which is handled at interface_main.py
        if option == "2":
            self.prompt_manage_users_options()
        if option == "3":
            self.prompt_create_plan()
        if option == "4":
            pass  # PLACEHOLDER
        if option == "5":
            self.prompt_generate_reports_options()
         

    # START of user options - - - - - - - - - - - - - - - - - - - - -

    def prompt_manage_users_options(self):
        option = input_until_valid(
			# when extending this list, make sure the input message matches the is_valid validation function and the options in interface_admin_options.py
			input_message = f"\nPlease choose a user management option below:\
				\n[1] CANCEL, return to home page\
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
            self.back()
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



    
    # END of user options - - - - - - - - - - - - - - - - - - - - -

    
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
 

    # START of generate report options - - - - - - - - - - - - - - - - - - - - -

    def prompt_generate_reports_options(self):
        option = input_until_valid(
			# when extending this list, make sure the input message matches the is_valid validation function and the options in interface_admin_options.py
            #                 
			input_message = f"\nPlease choose a report to generate below:\
				\n[1] CANCEL, return to home page\
                \n[2] Specific plan (not yet implemented)\
                \n[3] All plans (not yet implemented)\
                \n[4] Specific camp\
                \n[5] All camps",
			is_valid=lambda user_input: user_input.isdigit() and int(user_input) > 0 and int(user_input) <= 5,
			validation_message="Unrecognized input. Please choose from the above list."
		)
        if option == "1":
            self.back()
        if option == "2":
            pass # TODO
        if option == "3":
            pass # TODO
        if option == "4":
            self.generate_camp_report()
        if option == "5":
            self.generate_overall_report()


    def generate_camp_report(self):
            camp_name = input("Enter the name of the camp to generate the report for: ")
            with open('camps.json', 'r') as file:
                camps_data = json.load(file)
            camp_data = camps_data.get(camp_name, {})
            
            if camp_data:
                report = f"Report for {camp_name}:\n"
                report += f"Location: {camp_data.get('location', 'N/A')}\n"
                report += f"Capacity: {camp_data.get('capacity', 'N/A')}\n"
                report += f"Occupancy: {camp_data.get('occupancy', 'N/A')}\n"
                report += f"Humanitarian Plan: {camp_data.get('humanitarian_plan_in', 'N/A')}\n"
                volunteerString = ', '.join(camp_data.get('volunteer_in_charge', []))
                report += f"Volunteer in Charge: {volunteerString if volunteerString != "" else "Currently none"}\n"
                print(report)
            else:
                print(f"No data available for {camp_name}")
            input("Press Enter to continue...")
        
    def generate_overall_report(self):
            with open('camps.json', 'r') as file:
                camps_data = json.load(file)
            report = "Overall report for all plans:\n"

            for camp_name, camp_data in camps_data.items():
                report += f"Camp Name: {camp_name}\n"
                report += f"Location: {camp_data.get('location', 'N/A')}\n"
                report += f"Capacity: {camp_data.get('capacity', 'N/A')}\n"
                report += f"Occupancy: {camp_data.get('occupancy', 'N/A')}\n"
                report += f"Humanitarian Plan: {camp_data.get('humanitarian_plan_in', 'N/A')}\n"
                volunteerString = ', '.join(camp_data.get('volunteer_in_charge', []))
                report += f"Volunteer in Charge: {volunteerString if volunteerString != "" else "Currently none"}\n\n"
            print(report)
            input("Press Enter to continue...")

    # END of plan options - - - - - - - - - - - - - - - - - - - - -

    def back(self):  # TODO: refactor later
        pass
            