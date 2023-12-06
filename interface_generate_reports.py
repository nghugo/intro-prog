import json

from interface_helper import input_until_valid

class InterfaceGenerateReports:

	def prompt_admin_options(self):
		option = input_until_valid(
			
			#                 
			input_message = f"\n<homepage/report>\nPlease choose a report to generate below:\
				\n[1] CANCEL\
				\n[2] Specific plan\
				\n[3] All plans \
				\n[4] All camps in specific plan\
				\n[5] Specific camp\
				\n[6] All camps",
			is_valid=lambda user_input: user_input.isdigit() and int(user_input) > 0 and int(user_input) <= 5,
			validation_message="Unrecognized input. Please choose from the above list."
		)
		if option == "1":
			return  # option 1 is cancel, so just return
		if option == "2":
			self.generate_specific_plan_report()
		if option == "3":
			self.generate_all_plans_report()
		if option == "4":
			self.generate_camps_in_specific_plan_report()
		if option == "5":
			self.generate_camp_report()
		if option == "6":
			self.generate_overall_report()
	#2nd option 
	@staticmethod
	def generate_specific_plan_report():
		plan_name = input("\nEnter the name of the plan to generate the report for: ").strip()
		with open('plans.json', 'r') as file:
			plans_data = json.load(file)

		plan_data = plans_data.get(plan_name)

		print(f"\n--- Report for {plan_name} Plan ---")
		if plan_data:
			report = f"Description: {plan_data.get('description', 'N/A')}\n"
			report += f"Location: {plan_data.get('location', 'N/A')}\n"
			report += f"Start Date: {plan_data.get('start_date', 'N/A')}\n"
			print(report)
		else:
			print(f"No data available for the plan: {plan_name}")

		input("Press Enter to continue...")


	#3 ''
	@staticmethod
	def generate_all_plans_report():
		"""this gives a report of all the plans """
		with open('plans.json', 'r') as file:
			plans_data = json.load(file)
		print("\n--- Report for All Plans ---")
		for plan_name, plan_data in plans_data.items():
			report = f"\nPlan Name: {plan_name}\n"
			report += f"Description: {plan_data.get('description', 'N/A')}\n"
			report += f"Location: {plan_data.get('location', 'N/A')}\n"
			report += f"Start Date: {plan_data.get('start_date', 'N/A')}\n"
			print(report)
		print("--- End of Report for All Plans ---\n")
		input("Press Enter to continue...")

	#4 ''
	@staticmethod
	def generate_camps_in_specific_plan_report():
		plan_name = input("\nEnter the name of the plan to generate the report for camps: ")
		with open('camps.json', 'r') as file:
			camps_data = json.load(file)

		print(f"\n--- Camps in Plan: {plan_name} ---")
		found_camps = False
		for camp_name, camp_data in camps_data.items():
			
			if camp_data.get('humanitarian_plan_in') == plan_name:
				found_camps = True
				report = f"\nCamp Name: {camp_name}\n"
				report += f"Location: {camp_data.get('location', 'N/A')}\n"
				report += f"Max capacity: {camp_data.get('max_capacity', 'N/A')}\n"
				report += f"Occupancy: {camp_data.get('occupancy', 'N/A')}\n"
				volunteerString = ', '.join(camp_data.get('volunteers_in_charge', []))
				report += f"Volunteer in Charge: {volunteerString if volunteerString else 'Currently none'}"
				print(report)

		if not found_camps:
			print(f"\nNo camps found for plan: {plan_name}")

		print("--- End of report for camps in Plan: {plan_name} ---\n")
		input("Press Enter to continue...")
		
	#5 ''
	@staticmethod
	def generate_camp_report():
			camp_name = input("\nEnter the name of the camp to generate the report for: ")
			with open('camps.json', 'r') as file:
				camps_data = json.load(file)
			camp_data = camps_data.get(camp_name, {})
			
			print(f"\n--- Report for {camp_name} ---")
			if camp_data:
				report = ""
				report += f"Location: {camp_data.get('location', 'N/A')}\n"
				report += f"Max capacity: {camp_data.get('max_capacity', 'N/A')}\n"
				report += f"Occupancy: {camp_data.get('occupancy', 'N/A')}\n"
				report += f"Humanitarian Plan: {camp_data.get('humanitarian_plan_in', 'N/A')}\n"
				volunteerString = ', '.join(camp_data.get('volunteers_in_charge', []))
				report += f"Volunteer in Charge: {volunteerString if volunteerString != "" else "Currently none"}"
				print(report)
				print(f"--- End of report for {camp_name} ---\n")
			else:
				print(f"\nNo data available for {camp_name}")
			input("Press Enter to continue...")
	
	#6 '' 
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
				"added new line so report isnt jam packed"
				report += "\n"

			print(report)
			print("--- End of report for all plans ---\n")
			input("Press Enter to continue...")