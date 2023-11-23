import pandas as pd
from camp_modified import Camp
from interface_helper import input_until_valid


class InterfaceCampOptions:
    def __init__(self, users, current_user):
        self.users = users
        self.current_user = current_user
    
    def excute_option (self, user_option):
        if user_option == "1":
            self.add_camp()
        if user_option == "2":
            self.Delete_camp()
        if user_option == "3":
            self.Edit_camp_information_id()
        if user_option == "4":
            self.Edit_volunteer()
        if user_option == "5":
            self.Get_volunteer_list()
    
    def add_camp(self):
        field = input_until_valid(
            input_message = "Please enter: camp_identification/location/capacity/humanitarian_plan_in/volunteer_in_charge in order",
            is_valid=lambda user_input: user_input in
            ["camp_identification", "location", "capacity", "humanitarian_plan_in", "volunteer_in_charge"],
            validation_message = "Unrecognized input. Please enter a valid value"
        )
        camp_data = Camp.loadCampData()
        
        if field == "camp_identification":
            value = input_until_valid(
            input_message = "Please enter camp ID you want to add.", 
            is_valid=lambda user_input: user_input is str and user_input in camp_data,
            validation_message = "The camp number you entered exists"
        )
        if field == "location":
            value == input_until_valid(
                input_message = "Please "
            )

       
       
    def Delete_camp (self):
        Camp.delete_camp(identification, user)
        identification = input("Please enter the campID you want to delete")
        user = self.current_user
    
    def Edit_camp_information_id(self):
        Camp.edit_camp_information_id(camp_identification, attribute, new_value, user)
        camp_identification = input("Please enter the camp ID you want to edit the information")
        attribute = input("Please enter the camp camp attribute you want to edit: location/capacity")
        # new_value = input(f'Please enter the new value for {attribute} you would like to change')
        # input type string/int
        user = self.current_user
    
    def Edit_volunteer(self):
        edit_volunteer(camp_identification, volunteer, user, method)
        camp_identification = input("Please enter the campID you want to change its volunteer")
        user = self.current_user
        volunteer = input("Please enter the volunteer name")
        if volunteer in Camp.get_volunteer_list(camp_identification):
            method = "add"
        else:
            method = "remove"
    
    def Get_volunteer_list(self):
        get_volunteer_list(camp_identification)
        camp_identification = input("Please enter the camp ID")
        
    
    
    







