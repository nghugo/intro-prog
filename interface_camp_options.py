import pandas as pd
from camp_modified import Camp
from interface_helper import input_until_valid
from current_user import CurrentUser
import json
from users import Users
class InterfaceCampOptions:
    def __init__(self, users, current_user):
        self.users = users
        self.current_user = current_user


    def excute_option (self, user_option):
        if user_option == "1":
            self.add_camp()
        if user_option == "2":
            self.delete_camp()
        if user_option == "3":
            self.Edit_camp_information()
        if user_option == "4":
            self.Edit_volunteer()
        if user_option == "5":
            self.Get_volunteer_list()
    
    def add_camp(self):
        camp_identification = input_until_valid(
        input_message = "Please enter the new CampID",
        is_valid = lambda user_input: user_input != "" and Camp.validateId != None,
        validation_message = "CampID cannot be empty or this campID already exists."
    )
    
        Location = input_until_valid(
            input_message = "Enter the country this camp locates in",
            is_valid = lambda user_input: user_input != "" and type(user_input) == str,
            validation_message = "This cannot be empty. Please enter the camp location"
        )

        capacity = input_until_valid(
            input_message = "Enter the camp capacity",
            is_valid=lambda user_input: user_input != "" and type(user_input) == str,
            validation_message="This cannot be empty! Please enter the integer as camp capacity!"
        )
        
        humanitarian_plan_in = input_until_valid(
            input_message= "Please enter the humanitarian plan this camp belongs to",
            is_valid = lambda user_input: user_input != "" and type(user_input) == str,
            validation_message="This cannot be empty. Please enter the name of the humanitarian plan"
        )

        volunteer_in_charge = input_until_valid(
            input_message="Enter the volunteer name who charges this camp",
            is_valid=lambda user_input: user_input!="",
            validation_message="volunteer does not exist or volunteer is in other camps! Please retry."
        )
        # TODO: refer volunteerlist to add more deciding criteria in is_valid
        
        confirm = input_until_valid(
            input_message=f"Please confirm details of the new camp (y/n):\n->CampID: {camp_identification}\n->location: {Location}\n->capacity: {capacity}\n->in {humanitarian_plan_in} humanitarian plan\n->volunteer_in_charge: {volunteer_in_charge}\n[y] Yes\n[n] No (abort)",
			is_valid=lambda user_input: user_input == "y" or user_input == "n",
			validation_message="Unrecognized input. Please confirm details of the new camp (y/n):\n[y] Yes\n[n] No (abort)"
        )
        if confirm == "y":
            success = Camp(
				camp_identification, Location , capacity, humanitarian_plan_in, volunteer_in_charge)
            if success:
                print(f"Successfully added {camp_identification}")
            else:
                print(f"Failed to add {camp_identification}")
        else:
            print(f"Aborted user addition.")


    def delete_camp(self):
        with open("users.json", "r") as json_file:
            data = json.load(json_file)

        username = self.current_user.username
        if data[username]['is_admin']:
            user = "admin"
        else:
            user != "admin"
    
        camp_identification = input_until_valid(
            input_message= "Please enter the campID you would like to delete",
            is_valid=lambda user_input: user_input !="",
            validation_message="CampID cannot be empty."
        )
        if camp_identification == "":
            print("Camp deletion aborted.")

        else:
            confirm = input_until_valid(
            input_message=f"Please confirm you want to delete this camp (y/n):\n->CampID: {camp_identification}\n[y] Yes\n[n] No (abort)",
			is_valid=lambda user_input: user_input == "y" or user_input == "n",
			validation_message="Unrecognized input. Please confirm details of the camp (y/n):\n[y] Yes\n[n] No (abort)"
        )
            if confirm == "y":
                test = Camp.delete_camp(camp_identification, user)
                if test: 
                    print("Successfully delete {camp_identification}")
                else: 
                    print(f'Failed to delete {camp_identification} as {camp_identification} not in camp list')
            else:
                print(f"Aborted delete this camp.")


    def Edit_camp_information(self):

        camp_data = Camp.loadCampData()
        # print(type(camp_data))  #TODO: remove
        # print(camp_data)  #TODO: remove
        # print(camp_data.keys())  #TODO: remove

        camp_identification = input_until_valid(
                input_message="Please enter the campID you would like to change camp details, or leave empty to abort",
                is_valid = lambda user_input: user_input == "" or user_input in camp_data,
                validation_message= "The campID does not exist."
            )   
        
        if camp_identification == "":
            print("Camp modification aborted.")
        
        else:
            if self.users.users[self.current_user.username]["is_admin"] or self.current_user.username == camp_data[camp_identification]["volunteer_in_charge"]:
                attribute = input_until_valid(
			    input_message="Enter the field (camp_identification/location/capacity/humanitarian_plan_in/volunteer_in_charge) to modify:",
			    is_valid=lambda user_input: user_input in {
			    "camp_identification", "location", "capacity", "humanitarian_plan_in", "volunteer_in_charge"},
			    validation_message="Unrecognized input. Please enter a valid field (camp_identification/location/capacity/humanitarian_plan_in/volunteer_in_charge)."
            )
                if attribute == "camp_identification":
                    new_value = input_until_valid(
                    input_message = f"Please enter the new value for {attribute}",
                    is_valid=lambda user_input: user_input != camp_data[camp_identification],
                    validation_message="Please enter the new campID different from current one."
                )
                
                else:
                    new_value = input_until_valid(
                    input_message=f"Enter the new value for the {attribute}:",
                    is_valid=lambda user_input: user_input != camp_data[camp_identification][attribute],
                    validation_message=f"Please enter the different value of {attribute} from current one."
                )

                confirm = input_until_valid(
                    input_message=f"Please confirm you want to change {attribute} from previous value:\n {camp_identification if attribute == "camp_identification" else camp_data[camp_identification][attribute]} to {new_value} \n[y] Yes\n[n] No (abort)",
                    is_valid=lambda user_input: user_input == "y" or user_input == "n",
                    validation_message="Unrecognized input. Please confirm the new campID (y/n):\n[y] Yes\n[n] No (abort)"
                )

                # TODO: implement actual modification on persistent data (camps.json)
                
            else:
                print("You are not allowed to edit camp information")
            
       
               
            
        # if confirm == "y":
        #     # test = Camp.edit_camp_information_id(camp_identification, new_identification, self.current_user)
        #     test = Camp.edit_camp_information(camp_identification = camp_identification, attribute = attribute, new_value = new_value, user = self.current_user) 
        #     if test:
        #         print(f"change the {attribute} successfully!")
        #     else:
        #         print(f"Camp information modification aborted.")

# testing error1 -- data saving:
# login as admin: 
# [9] edit humanitarian plan 
# [1] add camp: if we creat camp1, showing 'already exist' and 'sucessfully created a new camp' at the same time; while creating other campID such as 'camp2' or 'camp3' is fine.
# besides, if we create another new camp after creating one, the new one will overwrite the existing one. And in each run, previous data in camp.json will be lost. There might be some problem in saving our camp data into camp.json.

# testing erro2 -- accessing camp data:
# login as admin:
# [9] edit humanitarian plan 
# [3] edit camp info: need to access camp_data from camp.json to set restriction for user_input in input_until_validation check. But there is something wrong accessing the camp_data[camp_identification] in line 113: is_valid = lambda user_input: user_input == "" or user_input in camp_data[camp_identification]


        
    
    
    







