import pandas as pd
import json

from interface_helper import input_until_valid


class InterfaceVolunteerOptions:
    def __init__(self, users, current_user):
        self.users = users
        self.current_user = current_user

    def execute_option(self, user_option):
        if user_option == "2":
            self.prompt_modify_my_details()
        if user_option == "3":
            self.list_my_details()
        if user_option == "4":
            pass  # TODO
        if user_option == "5":
            self.add_refugee()
        if user_option == "6":
            pass  # TODO

    def prompt_modify_my_details(self):
        field = input_until_valid(
            input_message="Enter the field (username/password/phone_number) to modify:",
            is_valid=lambda user_input: user_input in {
                "username", "password", "phone_number"},
            validation_message="Unrecognized input. Please enter a valid field (username/password/phone_number)."
        )
        if field == "username":
            value = input_until_valid(
                input_message="\nEnter the new username:",
                is_valid=lambda user_input: user_input != "" and user_input not in self.users.users,
                validation_message="Username cannot be empty or is already taken. Please enter a different username"
            )
        elif field == "phone_number":
            value = input_until_valid(
                input_message=f"Enter the new phone number (5+ digits or leave empty)",
                is_valid=lambda user_input: (user_input == "") or (
                    user_input.isnumeric() and len(user_input) >= 5),
                validation_message=f"Unrecognized input. Please enter the new phone number (5+ digits or leave empty)"
            )
        else:  # field == "password"
            value = input_until_valid(f"Enter the new value for the {field} field:")

        confirm = input_until_valid(
            input_message=f"Please confirm details of your user detail modification (y/n):\n->Field: {field}\n->Previous Value: {self.users.users[self.current_user.username][field] if field != "username" else self.current_user.username}\n->New Value: {value}\n[y] Yes\n[n] No (abort)",
            is_valid=lambda user_input: user_input == "y" or user_input == "n",
            validation_message="Unrecognized input. Please confirm details of the user modification (y/n):\n[y] Yes\n[n] No (abort)"
        )
        if confirm == "y":
            # modify persistent store and reload current_user if username matches
            self.users.modify_user(self.current_user.username, field, value)
            if field == "username":
                self.current_user.set_username(value)
            elif field == "password":
                self.current_user.set_password(value)

            print("Successfully modified user.")
        else:
            print("User modification aborted.")

    def list_my_details(self):
        print("--- Your details are follows ---")
        print(f'{"username":16}{self.current_user.username}')
        for field, value in self.users.users[self.current_user.username].items():
            # print(field, ":", value)
            print(f'{field:16}{value}')
        print("--- End of your details ---")


    def add_refugee(self):
        name = input_until_valid(
            input_message="Enter the name of the refugee:",
            is_valid=lambda user_input: user_input.strip() != "",
            validation_message="Name cannot be empty. Please enter a valid name."
        )

        camp_identification = input_until_valid(
            input_message="Enter camp identification:",
            is_valid=lambda user_input: user_input.strip() != "",
            validation_message="Camp identification cannot be empty. Please enter a valid camp identification."
        )

        medical_condition = input_until_valid(
            input_message="Enter medical condition:",
            is_valid=lambda user_input: user_input.strip() != "",
            validation_message="Medical condition cannot be empty. Please enter a valid medical condition."
        )

        recorded_refugees = self.load_refugees()

        
        refugee_infomation = {
            "name": name,
            "camp_identification": camp_identification,
            "medical_condition": medical_condition,
        }


        recorded_refugees[name] = refugee_infomation

        confirm = input_until_valid(
            input_message=f"Please confirm details of the new user (y/n):\n->Name: {name}\n->Camp Identification: {camp_identification}\n->Medical condition: {medical_condition}\n[y] Yes\n[n] No (abort)",
            is_valid=lambda user_input: user_input == "y" or user_input == "n",
            validation_message="Unrecognized input. Please confirm details of the new user (y/n):\n[y] Yes\n[n] No (abort)"
        )
        if confirm == "y":
            with open("refugees.json", "w") as json_file:
                json.dump(recorded_refugees, json_file, indent=2)

            print(f"Refugee {name} is added successfully.")
            
        else:
            print(f"Aborted refugee addition.")
    
    def load_refugees(self):
        try:
            with open("refugees.json", "r") as json_file:
                json_load = json.load(json_file)
                return json_load
        except FileNotFoundError:
            return {}