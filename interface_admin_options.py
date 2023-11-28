import json #why is this not working not a solid black colour 

import pandas as pd

from interface_helper import input_until_valid, is_valid_date
from plans import Plans

class InterfaceAdminOptions:
    def __init__(self, users, current_user):
        self.users = users
        self.current_user = current_user
        # initialise self.plans
        self.plans = Plans()

    def generate_camp_report(self):
        camp_name = input("Enter the name of the camp to generate the report for: ")
        # Replace 'camps.json' with the actual filename where camp data is stored
        with open('camps.json', 'r') as file:
            camps_data = json.load(file)
        camp_data = camps_data.get(camp_name, {})
        if not camp_data:
            print(f"No data available for {camp_name}")
            return
        report = f"Report for {camp_name}:\n"
        report += f"Refugee Count: {len(camp_data.get('refugees', []))}\n"
        report += f"Resources: {camp_data.get('resources', 'N/A')}\n"
        report += f"Volunteers: {len(camp_data.get('volunteers', []))}\n"
        print(report)

    def generate_overall_report(self):
         # Replace 'camps.json' with the actual filename where camp data is stored
        with open('camps.json', 'r') as file:
            camps_data = json.load(file)
        report = "Overall Report:\n"
        for camp_name, camp_data in camps_data.items():
            report += f"Camp Name: {camp_name}\n"
            report += f"Refugee Count: {len(camp_data.get('refugees', []))}\n"
            report += f"Resources: {camp_data.get('resources', 'N/A')}\n"
            report += f"Volunteers: {len(camp_data.get('volunteers', []))}\n\n"
        print(report)


    def execute_option(self, user_option):

        if user_option == "2":
            self.prompt_add_user()
        if user_option == "3":
            self.prompt_delete_user()
        if user_option == "4":
            self.prompt_activate_user()
        if user_option == "5":
            self.prompt_deactivate_user()
        if user_option == "6":
            self.prompt_modify_user()
        if user_option == "7":
            self.list_users()
        if user_option == "8":
            self.prompt_create_plan()
        if user_option == "9":
            self.generate_camp_report()
        if user_option == "10":
            self.generate_overall_report()

    def prompt_add_user(self):
        username = input_until_valid(
            input_message="\nEnter the username for the new user:",
            is_valid=lambda user_input: user_input != "" and user_input not in self.users.users,
            validation_message="Username cannot be empty or is already taken. Please enter a different username for the new user"
        )
        password = input_until_valid("Enter the password for the new user:")
        phone_number = input_until_valid(
            input_message=f"Enter the new phone number (5+ digits or leave empty)",
            is_valid=lambda user_input: (user_input == "") or (
                user_input.isnumeric() and len(user_input) >= 5),
            validation_message=f"Unrecognized input. Please enter the new phone number (5+ digits or leave empty)"
        )
        is_admin = input_until_valid(
            input_message="Specify if the new user is an admin (t/f):\n[t] True\n[f] False",
            is_valid=lambda user_input: user_input == "t" or user_input == "f",
            validation_message="Unrecognized input. Please specify if the new user is an admin (t/f):\n[t] True\n[f] False"
        )
        is_activated = input_until_valid(
            input_message="Specify if the new user is activated (t/f):\n[t] True\n[f] False",
            is_valid=lambda user_input: user_input == "t" or user_input == "f",
            validation_message="Unrecognized input. Please specify if the new user is activated (t/f):\n[t] True\n[f] False"
        )
        confirm = input_until_valid(
            input_message=f"Please confirm details of the new user (y/n):\n->Username: {username}\n->Password: {password}\n->Is Admin: {
                "yes" if is_admin else "no"}\n->phone_number: {phone_number}\n->Is Activated: {"yes" if is_activated else "no"}\n[y] Yes\n[n] No (abort)",
            is_valid=lambda user_input: user_input == "y" or user_input == "n",
            validation_message="Unrecognized input. Please confirm details of the new user (y/n):\n[y] Yes\n[n] No (abort)"
        )
        if confirm == "y":
            success = self.users.add_user(
                username=username, password=password, phone_number=phone_number, is_admin=is_admin == "y", is_activated=is_activated == "y")
            if success:
                print(f"Successfully added user {username}")
            else:
                print(f"Failed to add user {username}")
        else:
            print(f"Aborted user addition.")

    def prompt_activate_user(self):
        username = input_until_valid(
            input_message="\nEnter the username of the user to activate or leave empty to abort:",
            is_valid=lambda user_input: user_input in self.users.users or user_input == "",
            validation_message="Username not found. Please enter an existing username or leave empty to abort."
        )
        if username == "":
            print("User activation aborted.")
        else:
            self.users.modify_user(username, "is_activated", True)
            print(f"User {username} has been activated.")

    def prompt_deactivate_user(self):
        username = input_until_valid(
            input_message="\nEnter the username of the user to deactivate or leave empty to abort:",
            is_valid=lambda user_input: user_input in self.users.users or user_input == "",
            validation_message="Username not found. Please enter an existing username or leave empty to abort."
        )
        if username == "":
            print("User deactivation aborted.")
        elif username == self.current_user.username:
            print(
                "You are not allowed to deactivate your own account. User deactivation aborted.")
        else:
            self.users.modify_user(username, "is_activated", False)
            print(f"User {username} has been deactivated.")

    def prompt_modify_user(self):
        username = input_until_valid(
            input_message="\nEnter the username of the user to modify or leave empty to abort:",
            is_valid=lambda user_input: user_input in self.users.users or user_input == "",
            validation_message="Username not found. Please enter an existing username or leave empty to abort."
        )

        if username == "":
            print("User modification aborted.")
            return  # early termination

        field = input_until_valid(
            input_message="Enter the field (username/password/phone_number/is_admin/is_activated) to modify:",
            is_valid=lambda user_input: user_input in {
                "username", "password", "phone_number", "is_admin", "is_activated"},
            validation_message="Unrecognized input. Please enter a valid field (username/password/phone_number/is_admin/is_activated)."
        )
        if field in {"is_admin", "is_activated"}:
            if username == self.current_user.username:
                # do not allow deactivation or admin disabling of own account
                print(f"You are not allowed to modify the {
                      field} field of your own account. Modification aborted.")
                return

            value = input_until_valid(
                input_message=f"Specify the new value for the {field} field (t/f):\n[t] True\n[f] False",
                is_valid=lambda user_input: user_input == "t" or user_input == "f",
                validation_message=f"Unrecognized input. Please specify the new value for the {field} field (t/f):\n[t] True\n[f] False"
            )
            value = True if value == "t" else False
        elif field == "phone_number":
            value = input_until_valid(
                input_message=f"Specify the new phone number (5+ digits or leave empty)",
                is_valid=lambda user_input: (user_input == "") or (
                    user_input.isnumeric() and len(user_input) >= 5),
                validation_message=f"Unrecognized input. Please specify the new phone number (5+ digits or leave empty)"
            )
        else:
            value = input_until_valid(f"Enter the new value for the {field} field:")

        confirm = input_until_valid(
            input_message=f"Please confirm details of the user modification (y/n):\n->Username: {username}\n->Field: {field}\n->Previous Value: {
                self.users.users[username][field] if field != "username" else username}\n->New Value: {value}\n[y] Yes\n[n] No (abort)",
            is_valid=lambda user_input: user_input == "y" or user_input == "n",
            validation_message="Unrecognized input. Please confirm details of the user modification (y/n):\n[y] Yes\n[n] No (abort)"
        )
        if confirm == "y":
            # modify persistent store and reload current_user if username matches
            self.users.modify_user(username, field, value)
            if username == self.current_user.username:
                if field == "username":
                    self.current_user.set_username(value)
                elif field == "password":
                    self.current_user.set_password(value)

            print("Successfully modified user.")
        else:
            print("User modification aborted.")

    def prompt_delete_user(self):

        username = input_until_valid(
            input_message="\nEnter the username of the user to delete or leave empty to abort:",
            is_valid=lambda user_input: user_input in self.users.users or user_input == "",
            validation_message="Username not found. Please enter an existing username or leave empty to abort."
        )
        if username == "":
            print("User deletion aborted.")
        elif username == self.current_user.username:
            print(
                "You are not allowed to delete your own account. User deletion aborted.")
        else:
            self.users.delete_user(username)
            print(f"User {username} has been deleted.")

    def list_users(self):
        print("--- Users are as follows ---")
        # using pandas just for pretty print
        users_df = pd.DataFrame.from_dict(self.users.users).transpose()
        print(users_df)
        print("--- End of users list ---")

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
            success = self.plans.add_plan(
                plan_name=plan_name, description=description, location=location, start_date=start_date)
            if success:
                print(f"Plan for {plan_name} successfully added.")
            else:
                print(f"Failed to add plan for {plan_name}")
        else:
            print(f"Aborted plan creation.")
