#interface volunteer option.py
#resources.py
from resource_modified import CampResources
#handle user input
from interface_helper import input_until_valid
from users import Users
from camp_modified import Camp
import pandas as pd
class InterfaceManageResource:
    def __init__(self,current_user):
        self.current_user = current_user
        self.resources = CampResources().resources
        
    def  prompt_admin_options(self):
        option = input_until_valid(
                input_message = f"\n<homepage/manage-resources>\nPlease choose a resource management option below:\
                    \n[1] CANCEL\
                    \n[2] List all resource profiles under all camps\
                    \n[3] List all resource profiles under a specific camp\
                    \n[4] allocate resources of a specific camp",
                is_valid=lambda user_input: user_input.isdigit() and int(user_input) > 0 and int(user_input) <= 4,
                validation_message="Unrecognized input. Please choose from the above list.")
        
        if option == "1":
            return
        if option == "2":
            self.prompt_display_all_camps()
        if option == "3":
            self.prompt_display_specific_camp()
        if option == "4":
            self.prompt_update_resources()

    @staticmethod
    def validate_input_camp(camp_id,current_user): 
        users = Users.load_users()
        camp_data = Camp.loadCampData()
        is_admin = users[current_user]["is_admin"]
        if camp_id in camp_data:
           if current_user in camp_data[camp_id]["volunteers_in_charge"]:
               return True
           elif is_admin:
               return True
           else:
               return False
        else:
            return False
        
    def prompt_volunteer_options(self):
        option = input_until_valid(
                input_message = f"\n<homepage/manage-resources>\nPlease choose a resource management option below:\
                    \n[1] CANCEL\
                    \n[2] List all resource profiles under a specific camp\
                    \n[3] allocate resources of a specific camp",
                is_valid=lambda user_input: user_input.isdigit() and int(user_input) > 0 and int(user_input) <= 3,
                validation_message="Unrecognized input. Please choose from the above list.")
        
        if option == "1":
            return
        if option == "2":
            self.prompt_display_specific_camp()
        if option == "3":
            self.prompt_update_resources()
    
    def prompt_display_all_camps(self):
        print('the information of resources of all camps is display as below:')
        df = pd.DataFrame(self.resources)
        df_tranpose = df.transpose()
        print(df_tranpose)
        print("----------------------------------end table-------------------------------------")
        enter = input_until_valid("Press Enter to go back: ",is_valid=lambda user_input:user_input=="",
                                  validation_message="Please press enter to go back")
        if enter == "":
            return

    def print_exist_camp(self):
        df = pd.DataFrame(self.resources)
        df_tranpose = df.transpose()
        column_names = df.columns.tolist()
        df_camp = pd.DataFrame({'camp name': column_names})
        print(df_camp)

    def prompt_display_specific_camp(self):
        users = Users.load_users()
        is_admin = users[self.current_user.username]["is_admin"]
        if is_admin:
            camp_id = input_until_valid(input_message="Enter the camp name: ", is_valid=lambda user_input: (user_input == "") or (user_input in self.resources), 
                            validation_message="unrecognized camp. Please enter a new one: ")
            
            if camp_id == "":
                print("display viewing aborted.")
                return

            resource_sepecific_camp = CampResources()
            resource_sepecific_camp.display_resources(camp_id)
            print("-------end of resource details--------")
            input("Press Enter to return to the previous window...")
        else:
            camp_data = Camp.loadCampData()
            camp_id = input_until_valid(input_message="Enter the camp name: ", 
                            is_valid=lambda user_input: (user_input == "") or (self.validate_input_camp(user_input,self.current_user.username)), 
                            validation_message="unrecognized camp or camp not accessible. Please enter a new one: ")
            
            if camp_id == "":
                print("display viewing aborted.")
                return

            resource_sepecific_camp = CampResources()
            resource_sepecific_camp.display_resources(camp_id)
            print("-------end of resource details--------")
            input("Press Enter to return to the previous window...")
        

    def prompt_update_resources(self):
        #todo:if required to display the campid volunteer incharge first:
        #find how many camps a volunteer is in charge and print them down.
        #This is so strange! time cosumming if there exists a lot of data
        print("current exist camps:")
        self.print_exist_camp()
        camp_id = input_until_valid(input_message="Enter the camp name or press enter to return to the former page: ", 
                        is_valid=lambda user_input:(user_input == "") or (self.validate_input_camp(user_input,self.current_user.username)), 
                        validation_message="unrecognized camp or camp not accessible. Please enter a new one: ")
        
        if camp_id =="":
            print("edition aborted.")
            return
        #todo: present the population of the camp.
        df = pd.DataFrame(self.resources).transpose()
        print("detailed information of this camp:")
        print(df.loc[camp_id])
        not_exit = True
        while(not_exit == True):
            edition_resource = input_until_valid(input_message="Enter one resource type to edit: food_packets/medical_packets/water_packets/shelter_packets/clothing_packets/first_aid_packets/baby_packet/sanitation_packets)/n Or press Enter to return: ",
                                                is_valid=lambda user_input: user_input in self.resources[camp_id] or user_input == "",
                                                validation_message="unrecognized type, please enter again.")
            if edition_resource == "":
                print("edition aborted.")
                return
            
            amount_edit = input_until_valid(input_message="enter the new amount for"+edition_resource+"or press enter to return: ",
                                                is_valid=lambda user_input: user_input.isdigit() or user_input == "",
                                                validation_message="unrecognized type, please enter again.")
            if amount_edit == "":
                print("edition aborted.")
                return
            
            confirm = input_until_valid(input_message="please confirm your edition for change "+edition_resource+ "to amount"+ amount_edit+" \n[y] Yes\n[n] No (abort)",
                                        is_valid = lambda user_input: user_input == "y" or user_input == "n",
                                        validation_message="Unrecognized input. Please confirm (y/n):\n[y] Yes\n[n] No (abort)")
            
            if confirm == "n":
                print(f"Camp information modification aborted.")
                return
            resource = CampResources()
            test = resource.update_resources(camp_id,edition_resource,int(amount_edit))

            if test:
                print(f"You've changed the {edition_resource} successfully!")
            else:
                print(f'Failed to change {edition_resource}')

            exit_confirm = input_until_valid(input_message="do you want to edit other resource information?\n[y] Yes\n[n] No (abort)",
                                        is_valid = lambda user_input: user_input == "y" or user_input == "n",
                                        validation_message="Unrecognized input. Please confirm (y/n):\n[y] Yes\n[n] No (abort)")
            
            if exit_confirm == 'y':
                not_exit = True
            else:
                not_exit = False

        


        


        


    

