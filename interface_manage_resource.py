#interface volunteer option.py
#resources.py
from resource_modified import CampResources
#handle user input
from interface_helper import input_until_valid
from users import Users
from camp_modified import Camp
from refugees import load_refugees,get_num_families_and_members_by_camp
from collections import defaultdict
import pandas as pd


class InterfaceManageResource:
    """class used for manage option related to manage resource.
    """
    def __init__(self,current_user):
        self.current_user = current_user
        self.resources = CampResources().resources
        
    def  prompt_admin_options(self):
        option = input_until_valid(
                input_message = f"\n<homepage/manage-resources>\nPlease choose a resource management option below:\
                    \n[1] CANCEL\
                    \n[2] List all resource profiles under all camps\
                    \n[3] List all resource profiles under a specific camp\
                    \n[4] Update resources of a specific camp\
                    \n[5] Add resources to a specific camp\
                    \n[6] Limited resources warnning",
                is_valid=lambda user_input: user_input.isdigit() and int(user_input) > 0 and int(user_input) <= 6,
                validation_message="Unrecognized input. Please choose from the above list.")
        
        if option == "1":
            return
        if option == "2":
            self.prompt_display_all_camps()
        if option == "3":
            self.prompt_display_specific_camp()
        if option == "4":
            self.prompt_change_resources('update')
        if option == "5":
            self.prompt_change_resources('add')
        if option == "6":
            self.prompt_resource_warning()


        
    def prompt_volunteer_options(self):
        option = input_until_valid(
                input_message = f"\n<homepage/manage-resources>\nPlease choose a resource management option below:\
                    \n[1] CANCEL\
                    \n[2] List all resource profiles under a specific camp\
                    \n[3] update resources of a specific camp\
                    \n[4] add resources to a specific camp",
                is_valid=lambda user_input: user_input.isdigit() and int(user_input) > 0 and int(user_input) <= 4,
                validation_message="Unrecognized input. Please choose from the above list.")
        
        if option == "1":
            return
        if option == "2":
            self.prompt_display_specific_camp()
        if option == "3":
            self.prompt_change_resources("update")
        if option == "4":
            self.prompt_change_resources("add")

    
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
    #it may remain some problems as I can not use the method in interface_camp  
    #   
    @staticmethod
    def print_accessible_camp(current_user):
        users = Users.load_users()
        camp_data = Camp.loadCampData()
        is_admin = users[current_user]["is_admin"]
        camp_list = []
        for camp in camp_data:
            if InterfaceManageResource.validate_input_camp(camp,current_user):
                camp_list.append(camp)
        access_camp = {'camp_ID':camp_list}
        df = pd.DataFrame(access_camp)
        print(df)




        
    @staticmethod
    def count_occupancy(camp_id): #scan the refugee json file
        count = 0
        refugees = load_refugees()
        for refugee in refugees:
            if refugees[refugee]["camp_id"] == camp_id:
                count+=1
        return count
        

    def print_exist_camp(self):
        """helper method for display all existing camps"""
        df = pd.DataFrame(self.resources)
        df_tranpose = df.transpose()
        column_names = df.columns.tolist()
        df_camp = pd.DataFrame({'camp name': column_names})
        print(df_camp)
        
    def prompt_display_specific_camp(self):
        users = Users.load_users()
        is_admin = users[self.current_user.username]["is_admin"]
        filtered_camps = Camp.load_camps_user_has_access_to(self.current_user.username)
        message_key = "\nExisting camp(s):" if is_admin else "Camp(s) you have access rights to:"
        message_value = ", ".join(list(filtered_camps.keys())) if filtered_camps else "None found"
        print(f"{message_key} {message_value}")

        if is_admin:
            camp_id = input_until_valid(
				input_message = "Enter the camp name, or leave empty to abort: ", 
				is_valid = lambda user_input: (user_input == "") or (user_input in self.resources), 
				validation_message = "Unrecognized camp. Please enter a new one, or leave empty to abort: ")
			
            if camp_id == "":
                print("Aborted displaying resources.")
                return

            resource_sepecific_camp = CampResources()
            resource_sepecific_camp.display_resources(camp_id)
            print("-------End of resource details--------")
            input("Press Enter to continue...")
        else:
            camp_id = input_until_valid(
				input_message = "Enter the camp name, or leave empty to abort: ", 
				is_valid = lambda user_input: (user_input == "") or (user_input in filtered_camps), 
				validation_message = "Unrecognized camp or camp not accessible. Please enter a new one or leave empty to abort: ")
			
            if camp_id == "":
                print("Aborted displaying resources.")
                return
            
            resource_sepecific_camp = CampResources()
            resource_sepecific_camp.display_resources(camp_id)
            print("-------End of resource details--------")
            input("Press Enter to continue...")
    
    def prompt_change_resources(self,method='update'):
        #todo:if required to display the campid volunteer incharge first:
        #find how many camps a  volunteer is in charge and print them down.
        #This is so strange! time cosumming if there exists a lot of data
        print("current exist camps:")
        self.print_accessible_camp(self.current_user.username)
        camp_id = input_until_valid(input_message="Enter the camp name or press enter to return to the former page: ", 
                        is_valid=lambda user_input:(user_input == "") or (self.validate_input_camp(user_input,self.current_user.username)), 
                        validation_message="unrecognized camp or camp not accessible. Please enter a new one: ")
        
        if camp_id == "":
            print("edition aborted.")
            return
        if InterfaceManageResource.Test_underthreshold(camp_id):
            InterfaceManageResource.helper_print_warnning(camp_id)

        camp_population = get_num_families_and_members_by_camp()
        num_family = camp_population[camp_id]['num_families']
        num_members = camp_population[camp_id]['num_members']
        df = pd.DataFrame(self.resources).transpose()
        print("detailed information of "+camp_id+": \nCurrent populatiom: " + str(num_members) +"   Current family numbers: "+str(num_family)+"\n"+"-"*18+"end population details"+"-"*19+"\nCurrent resource details:")
        print(df.loc[camp_id])
        not_exit = True
        while(not_exit == True):
            edition_resource = input_until_valid(input_message="Enter one resource type to edit: food_packets/medical_packets/water_packets/shelter_packets/clothing_packets/sanitation_packets)/n Or press Enter to return: ",
                                                is_valid=lambda user_input: user_input in self.resources[camp_id] or user_input == "",
                                                validation_message="unrecognized type, please enter again.")
            if edition_resource == "":
                print("edition aborted.")
                return
            
            amount_edit = input_until_valid(input_message="enter the new amount for"if method=="update" else "enter the new amount add to "+edition_resource+"or press enter to return: ",
                                                is_valid=lambda user_input: user_input.isdigit() or user_input == "",
                                                validation_message="unrecognized type, please enter again.")
            
            if amount_edit == "":
                print("edition aborted.")
                return
            if method == 'update':
                confirm = input_until_valid(input_message="please confirm your edition for change "+edition_resource+ "to amount"+ amount_edit +" \n[y] Yes\n[n] No (abort)",
                                        is_valid = lambda user_input: user_input == "y" or user_input == "n",
                                        validation_message="Unrecognized input. Please confirm (y/n):\n[y] Yes\n[n] No (abort)")
                if confirm == "n":
                    print(f"Camp information modification aborted.")
                    return          
                resource = CampResources()
                test = resource.update_resources(camp_id,edition_resource,int(amount_edit))
            elif method == 'add':
                confirm = input_until_valid(input_message="please confirm your edition for adding "+amount_edit+ " to "+ edition_resource +" \n[y] Yes\n[n] No (abort)",
                                        is_valid = lambda user_input: user_input == "y" or user_input == "n",
                                        validation_message="Unrecognized input. Please confirm (y/n):\n[y] Yes\n[n] No (abort)")
                if confirm == "n":
                    print(f"Camp information modification aborted.")
                    return
                resource = CampResources()
                test = resource.adjust_resources(camp_id,edition_resource,int(amount_edit))
            
            
            if test:
                print(f"You've changed the {edition_resource} successfully!")
            else:
                print(f'Failed to change {edition_resource}')

            exit_confirm = input_until_valid(input_message="Do you want to edit other resource amounts?\n[y] Yes\n[n] No (abort)",
										is_valid = lambda user_input: user_input == "y" or user_input == "n",
										validation_message="Unrecognized input. Please confirm (y/n):\n[y] Yes\n[n] No (abort)")
			
            if exit_confirm == 'y':
                not_exit = True
            else:
                not_exit = False

    @staticmethod 
    def calculate_threshold(resource_name,camp_id):
        resources = CampResources()
        refugee_count_dict = get_num_families_and_members_by_camp()
        num_refugees= refugee_count_dict[camp_id]["num_members"]
        factor = resources.resource_factor()
        threshold = num_refugees*factor[resource_name]*resources.warnning_days
        return threshold
    
    @staticmethod
    def Test_underthreshold(camp_id):
        """helper method for determine which camp to warnning

        return boolean value: true if underthreshold"""
        resources = CampResources.load_resources()
        test = False
        for resource in resources[camp_id]:
            if resources[camp_id][resource]<InterfaceManageResource.calculate_threshold(resource,camp_id):
                test = True
        return test
    
    @staticmethod
    def helper_print_warnning(camp_id):
        """helper method for print warnning camp details"""
        resources = CampResources.load_resources()
        print("-"*25+"Warnning"+"-"*25)
        print(f'Warnning: {camp_id} may face risk of resource shortage.\n  The resource in shortage is:')
        for resource in resources[camp_id]:
            amount = resources[camp_id][resource]
            warnning_amount = InterfaceManageResource.calculate_threshold(resource,camp_id)
            if amount<warnning_amount:
                print(f' |{resource}: current amount {amount}. warnning level: {warnning_amount}')
        print("-"*25+"Warnning"+"-"*25+'\n')

        

                


    @staticmethod
    def print_warnning_level_helper():
        resources = CampResources()
        factor = resources.resource_factor()
        print('-'*29+'warnning level'+'-'*29)
        width = 20
        border_char = "||"
        padding_char = " "
        for resource in factor.keys():
            amount = factor[resource]
            text = f'The warnning level for {resource} is {amount} per person per day.'
            left_aligned = text.ljust(width)
            left_border = border_char + left_aligned + padding_char*(70-len(text)) +border_char
            print(left_border)
        print('||'+' '*17+'the warnning level of day time is '+str(resources.warnning_days)+'.'+' '*17+'||')
        print('-'*29+'warnning level'+'-'*29)


    def prompt_resource_warning(self):
        print('warnning for camps facing risk of shortage:\n')
        for camp_id in self.resources:
            if InterfaceManageResource.Test_underthreshold(camp_id):
                InterfaceManageResource.helper_print_warnning(camp_id)
            
        InterfaceManageResource.print_warnning_level_helper()

        
        confirm = input_until_valid(input_message="Please press 'enter' to return to former page. ",
                                        is_valid = lambda user_input: user_input == "",
                                        validation_message="Unrecognized input. Please press 'enter' to return to former page.")
        
        if confirm == "":
            return
    

