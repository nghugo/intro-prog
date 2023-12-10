import json
import os 
import datetime 
from interface_helper import input_until_valid
from refugees import get_num_families_and_members_by_camp
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
				\n[5] Specific camp and its nested resources + refugees",
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
			self.generate_overall_report()
		if option == "5":
			self.generate_camp_report()
		
		# DELETED (merged into generate_specific_plan_report)
		# if option == ???:
		# 	self.generate_camps_in_specific_plan_report()
	
	
	@classmethod
	def generate_specific_plan_report(cls):
			with open('plans.json', 'r') as file:
				plans_data = json.load(file)
			
			print("\nAvailable plans: " + ", ".join(plans_data.keys()))
			plan_name = input("\nEnter the name of the plan to generate the report for (leave empty to abort): ").strip()
			
			if plan_name == "":
				print("Operation aborted.")
				return

			if plan_name not in plans_data:
				print(f"Plan '{plan_name}' not found, Please enter an existing plan name or leave empty to abort.")
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
#timestamp
			current_time = datetime.datetime.now()
			timestamp = current_time.strftime("%Y%m%d_%H%M%S")
			save_report = input("Do you want to save this report as a text file? (y/n): ").lower()
			
			if save_report == 'y': 
				directory = "reports"  
				if not os.path.exists(directory):
					os.makedirs(directory)  
					
					file_name = f"{directory}/report_{plan_name}_{timestamp}.txt"
					with open(file_name, 'w') as file:
							file.write(report)
					print(f"Report for {plan_name} has been saved to {file_name}")
			else:
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
		input("Press Enter to continue...")

	@classmethod
	def generate_camp_report(cls):		

		with open('camps.json', 'r') as file:
			camps_data = json.load(file)
		resources_obj = CampResources()  # Initialise with CampResources

		print("\nAvailable camps: " + ", ".join(camps_data.keys()))
		camp_name = input_until_valid(
			input_message = f"Enter the name of the camp to generate the report for (leave empty to abort)",
			is_valid = lambda user_input: user_input == "" or user_input in camps_data,
			validation_message = f"No data available for the specified camp. Please enter an existing camp name or leave empty to abort."
		)
		if camp_name == "":
			print("Operation aborted.")
			return

		camp_data = camps_data.get(camp_name, None)  # Get camp data

		print(f"--- Report for {camp_name} ---\n")

		print(f"Location: {camp_data.get('location', 'N/A')}")
		print(f"Max capacity: {camp_data.get('max_capacity', 'N/A')}")

		# refugee info
		refugee_stats = get_num_families_and_members_by_camp()
		camp_refugee_data = refugee_stats.get(camp_name, {"num_families": 0, "num_members": 0})
		print(f"Number of Families: {camp_refugee_data['num_families']}")
		print(f"Total Number of Members: {camp_refugee_data['num_members']}")
		
		print(f"Humanitarian Plan: {camp_data.get('humanitarian_plan_in', 'N/A')}")
		volunteerString = ', '.join(camp_data.get('volunteers_in_charge', []))
		print(f"Volunteers in Charge: {volunteerString if volunteerString else 'Currently none'}")
		
		print()  # newline
		
		# Displaying resources in stock
		if not resources_obj.display_resources(camp_name):
			print("Resources: None available")

		print(f"\n--- End of report for {camp_name} ---\n")
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
	# 				report += f"Occupancy: {camp_data.get('occupancy', 'N/A')}\n"
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
	def generate_overall_report():
			with open('camps.json', 'r') as file:
				camps_data = json.load(file)
			print("\n--- Report for all plans ---")
			report = ""

			for camp_name, camp_data in camps_data.items():
				report += f"Camp Name: {camp_name}\n"
				report += f"Location: {camp_data.get('location', 'N/A')}\n"
				report += f"Max capacity: {camp_data.get('max_capacity', 'N/A')}\n"
				report += f"Occupancy: {camp_data.get('occupancy', 'N/A')}\n"
				report += f"Humanitarian Plan: {camp_data.get('humanitarian_plan_in', 'N/A')}\n"
				volunteerString = ', '.join(camp_data.get('volunteers_in_charge', []))
				report += f"Volunteer in Charge: {volunteerString if volunteerString != "" else "Currently none"}\n"
				report += "\n"  # newline for spacing

			print(report)
			print("--- End of report for all plans ---\n")
			input("Press Enter to continue...")