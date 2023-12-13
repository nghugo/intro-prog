import json
import os 
import datetime 

from plans import Plans
from interface_helper import input_until_valid
from refugees import get_num_families_and_members_by_camp, load_ALL_refugees
from resource_modified import CampResources

class InterfaceGenerateReports:
    plan_key_to_text = {
        "description": "Description",
        "country": "Country",
        "start_date": "Start Date",
        "end_date": "End Date",
        "status": "Status",
    }

    camp_key_to_text = {
        "location": "Location",
        "max_capacity": "Max capacity",
        "volunteers_in_charge": "Volunteers in Charge",
        "status": "Status",
    }

    def prompt_admin_options(self):
        option = input_until_valid(
                          
            input_message = f"\n<homepage/report>\nPlease choose a report to generate below:\
                \n[1] CANCEL\
                \n[2] All plans\
                \n[3] Specific plan and its nested camps\
                \n[4] All camps\
                \n[5] Specific camp and its nested resources + refugees\
                \n[6] All resources in ended plans",
            is_valid=lambda user_input: user_input.isdigit() and int(user_input) > 0 and int(user_input) <= 6,
            validation_message="Unrecognized input. Please choose from the above list."
        )
        if option == "1":
            return  # option 1 is cancel, so just return
        if option == "2":
            self.generate_all_plans_report()
        if option == "3":
            self.generate_specific_plan_report()
        if option == "4":
            self.generate_all_camps_report()
        if option == "5":
            self.generate_specific_camp_report()
        if option == "6":
            self.display_remaining_resources_in_ended_plans()


    @classmethod
    def generate_specific_plan_report(cls):
        with open('plans.json', 'r') as file:
            plans_data = json.load(file)
            
            print("\nAvailable plans: " + ", ".join(plans_data.keys()))            
            
            plan_name = input_until_valid(
				input_message= "\nEnter the name of the plan to generate the report for (leave empty to abort): ",
				is_valid = lambda user_input: user_input == "" or user_input in plans_data,
				validation_message = "Plan not found. Please enter an existing plan name or leave empty to abort."
			).strip()

            if plan_name == "":
                print("Operation aborted.")
                return
            
            plan_data = plans_data[plan_name]
            report = f"\n--- Report for {plan_name} Plan ---\n"
            for key, val in plan_data.items():
                report += f"{cls.plan_key_to_text[key]+":":16} {val}\n"

            with open('camps.json', 'r') as file:
                camps_data = json.load(file)
                camps_under_plan = {k: v for k, v in camps_data.items() if v["humanitarian_plan_in"] == plan_name}

            report += f"\nCamps in {plan_name}:\n"
            if not camps_data:
                report += f"No camps found under plan: {plan_name}. Please try a different plan name.\n"
            else:
                for camp_name, camp_data in camps_under_plan.items():
                    report += f"\n  {camp_name}\n"
                    for attr, val in camp_data.items():
                        if attr == "humanitarian_plan_in":
                            continue
                        report += f"  -> {attr}: {val}\n"

            report += f"\n--- End of Report for {plan_name} Plan ---\n"
            
            # timestamp
            current_time = datetime.datetime.now()
            timestamp = current_time.strftime("%Y%m%d_%H%M%S")
            save_report = input_until_valid(
                input_message = "Do you want to save this report as a text file? (y/n):",
                is_valid = lambda user_input: user_input == "y" or user_input == "n",
                validation_message = "Unrecognized input. Please confirm if you want to sasve this report as a text file (y/n):\n[y] Yes\n[n] No (abort)"
            ).lower()
            
            if save_report == 'y': 
                directory = "reports_timestamp"  
                if not os.path.exists(directory):
                    os.makedirs(directory)  
                
                file_name = f"{directory}/{plan_name}_{timestamp}.txt"
                with open(file_name, 'w') as file:
                    file.write(report)
                print(f"Report for {plan_name} has been saved to {file_name}")
            
            print(report)  
            input("Press Enter to continue...")



            


    @staticmethod
    def generate_all_plans_report():
        """this gives a report of all the plans """
        with open('plans.json', 'r') as file:
            plans_data = json.load(file)
        print("\n--- Report for All Plans ---")
        for plan_name, plan_data in plans_data.items():
            report = f"\nPlan Name: {plan_name}\n"
            report += f"Description: {plan_data.get('description', 'N/A')}\n"
            report += f"Country: {plan_data.get('country', 'N/A')}\n"
            report += f"Start Date: {plan_data.get('start_date', 'N/A')}\n"
            report += f"End Date: {plan_data.get('end_date', 'N/A')}\n"
            report += f"Status: {plan_data.get('status', 'N/A')}"
            print(report)
        print("--- End of Report for All Plans ---\n")
    
        save_report = input_until_valid(
        input_message = "Do you want to save this report as a text file? (y/n):",
        is_valid = lambda user_input: user_input == "y" or user_input == "n",
        validation_message = "Unrecognized input. Please confirm if you want to sasve this report as a text file (y/n):\n[y] Yes\n[n] No (abort)"
    ).lower()
        if save_report == 'y':
            directory = "reports_timestamp"
            if not os.path.exists(directory):
                os.makedirs(directory)

            file_name = f"{directory}/all_plans_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(file_name, 'w') as file:
                file.write(report)

            print(f"Report saved to {file_name}")
        input("Press Enter to continue...")


    @classmethod
    def generate_specific_camp_report(cls):
        with open('camps.json', 'r') as file:
            camps_data = json.load(file)

        report = "\nAvailable camps: " + ", ".join(camps_data.keys()) + "\n"
        print(report)

        camp_name = input_until_valid(
            input_message= "Enter the name of the camp to generate the report for (leave empty to abort):",
            is_valid = lambda user_input: user_input == "" or user_input in camps_data,
            validation_message = "Camp not found. Please enter an existing camp name or leave empty to abort."
        ).strip()
        
        if camp_name == "":
            print("Operation aborted.")
            return

        camp_data = camps_data[camp_name]
        report += f"\n--- Report for {camp_name} ---\n"
        report += f"Location: {camp_data.get('location', 'N/A')}\n"
        report += f"Max capacity: {camp_data.get('max_capacity', 'N/A')}\n"

        # Assuming these functions exist in your code
        refugee_stats = get_num_families_and_members_by_camp()
        camp_refugee_data = refugee_stats.get(camp_name, {"num_families": 0, "num_members": 0})
        report += f"Number of Families: {camp_refugee_data['num_families']}\n"
        report += f"Total Number of Members: {camp_refugee_data['num_members']}\n"

        plans = Plans.load_all_plans()
        humanitarian_plan_in = camp_data.get('humanitarian_plan_in', 'N/A')
        report += f"Humanitarian Plan: {humanitarian_plan_in} ({plans[humanitarian_plan_in]['status']})\n"

        volunteerString = ', '.join(camp_data.get('volunteers_in_charge', []))
        report += f"Volunteers in Charge: {volunteerString if volunteerString else 'Currently none'}\n\n"

        resources_obj = CampResources()
        if not resources_obj.display_ALL_resources(camp_name):
            report += f"Resources for {camp_name}: None available\n"

        refugees = load_ALL_refugees()
        if not refugees:
            report += f"\nRefugees for {camp_name}: None available\n"
        else:
            report += f"\nRefugees for {camp_name}:\n"
            for refugee_id, refugee_values in refugees.items():
                report += f"-> {refugee_values['fullname']} ({refugee_id})\n"
                report += f"     Number of members: {refugee_values['number_of_members']}\n"
                report += f"     Medical condition: {refugee_values['medical_condition']}\n"

        report += f"\n--- End of report for {camp_name} ---\n"
        print(report)  # Print the complete report

        save_report = input_until_valid(
        input_message = "Do you want to save this report as a text file? (y/n):",
        is_valid = lambda user_input: user_input == "y" or user_input == "n",
        validation_message = "Unrecognized input. Please confirm if you want to sasve this report as a text file (y/n):\n[y] Yes\n[n] No (abort)"
    ).lower()
        if save_report == 'y':
            directory = "reports_timestamp"
            if not os.path.exists(directory):
                os.makedirs(directory)

            file_name = f"{directory}/{camp_name}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(file_name, 'w') as file:
                file.write(report)

            print(f"Report saved to {file_name}")

        input("Press Enter to continue...")
    
    # @staticmethod
    # def generate_camps_in_specific_plan_report():
    # 	with open('plans.json', 'r') as file:
    # 		plans_data = json.load(file)
        
    # 	print("\nAvailable plans: " + ", ".join(plans_data.keys()))
        
    # 	while True:
    # 		plan_name = input("\nEnter the name of the plan to generate the report for camps (leave empty to abort): ").strip()
            
    # 		if plan_name == "":
    # 			print("Operation aborted.")
    # 			break

    # 		if plan_name not in plans_data:
    # 			print(f"Plan '{plan_name}' not found. Please enter an existing plan name or leave empty to abort.")
    # 			continue 

    # 		with open('camps.json', 'r') as file:
    # 			camps_data = json.load(file)

    # 		print(f"\n--- Camps in Plan: {plan_name} ---")
    # 		found_camps = False
    # 		for camp_name, camp_data in camps_data.items():
    # 			if camp_data.get('humanitarian_plan_in') == plan_name:
    # 				found_camps = True
    # 				report = f"\nCamp Name: {camp_name}\n"
    # 				report += f"Location: {camp_data.get('location', 'N/A')}\n"
    # 				report += f"Max capacity: {camp_data.get('max_capacity', 'N/A')}\n"
    # 				volunteerString = ', '.join(camp_data.get('volunteers_in_charge', []))
    # 				report += f"Volunteers in Charge: {volunteerString if volunteerString else 'Currently none'}"
    # 				print(report)

    # 		if not found_camps:
    # 			print(f"No camps found under plan: {plan_name}. Please try a different plan name.")
    # 			continue

    # 		print(f"--- End of report for camps in Plan: {plan_name} ---\n")
    # 		input("Press Enter to continue...")
    # 		break

    
    @staticmethod
    def generate_all_camps_report():
            with open('camps.json', 'r') as file:
                camps_data = json.load(file)
            print("\n--- Report for all plans ---")
            report = ""

            plans = Plans.load_all_plans()			

            for camp_name, camp_data in camps_data.items():
                humanitarian_plan_in = camp_data.get('humanitarian_plan_in', 'N/A')
                report += f"Camp Name: {camp_name}\n"
                report += f"Location: {camp_data.get('location', 'N/A')}\n"
                report += f"Max capacity: {camp_data.get('max_capacity', 'N/A')}\n"
                report += f"Humanitarian Plan: {humanitarian_plan_in} ({plans[humanitarian_plan_in]["status"]})\n"
                volunteerString = ', '.join(camp_data.get('volunteers_in_charge', []))
                report += f"Volunteer in Charge: {volunteerString if volunteerString != "" else "Currently none"}\n"
                report += "\n"  # newline for spacing

            print(report)
            print("--- End of report for all plans ---\n")

            save_report = input_until_valid(
        input_message = "Do you want to save this report as a text file? (y/n):",
        is_valid = lambda user_input: user_input == "y" or user_input == "n",
        validation_message = "Unrecognized input. Please confirm if you want to sasve this report as a text file (y/n):\n[y] Yes\n[n] No (abort)"
    ).lower()
            if save_report == 'y':
                directory = "reports_timestamp"
                if not os.path.exists(directory):
                    os.makedirs(directory)

                file_name = f"{directory}/all_camps_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                with open(file_name, 'w') as file:
                    file.write(report)

                print(f"Report saved to {file_name}")

            input("Press Enter to continue...")



    
    @staticmethod
    def display_remaining_resources_in_ended_plans():
        
        with open('plans.json', 'r') as file:
            plans_data = json.load(file)
        
        with open('camps.json', 'r') as file:
            camps_data = json.load(file)
        
        with open('camp_resources.json', 'r') as file:
            camp_resources_data = json.load(file)
        
        ended_plans = [plan_name for plan_name, plan_data in plans_data.items() if plan_data.get('status') == 'Ended']

    
        report = "\n--- Resources in Ended Plans ---\n"
        for plan_name in ended_plans:
            report += f"\nResources for Plan: {plan_name}\n"
            for camp_name, camp_data in camps_data.items():
                if camp_data['humanitarian_plan_in'] == plan_name:
                    resources = camp_resources_data.get(camp_name, {})
                    report += f"Resources for camp {camp_name}:\n"
                    for resource, quantity in resources.items():
                        report += f"-> {resource}: {quantity}\n"
                    report += "\n"

        report += f"--- Report generated on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---\n"
        print(report)

        
        save_report = input_until_valid(
        input_message = "Do you want to save this report as a text file? (y/n):",
        is_valid = lambda user_input: user_input == "y" or user_input == "n",
        validation_message = "Unrecognized input. Please confirm if you want to save this report as a text file (y/n):\n[y] Yes\n[n] No (abort)"
        ).lower()
        if save_report == 'y':
            directory = "reports_timestamp"
            if not os.path.exists(directory):
                os.makedirs(directory)

            file_name = f"{directory}/ended_plans_resources_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(file_name, 'w') as file:
                file.write(report)

            print(f"Report saved to {file_name}")

        input("Press Enter to continue...")