import json

from interface_helper import input_until_valid

class InterfaceGenerateReports:

	def prompt_admin_options(self):
		option = input_until_valid(
			
			#                 
			input_message = f"\n<homepage/report>\nPlease choose a report to generate below:\
				\n[1] CANCEL\
				\n[2] TODO: Specific plan (not yet implemented)\
				\n[3] TODO: All plans (not yet implemented)\
				\n[4] Specific camp\
				\n[5] All camps",
			is_valid=lambda user_input: user_input.isdigit() and int(user_input) > 0 and int(user_input) <= 5,
			validation_message="Unrecognized input. Please choose from the above list."
		)
		if option == "1":
			return  # option 1 is cancel, so just return
		if option == "2":
			pass
		if option == "3":
			pass
		if option == "4":
			self.generate_camp_report()
		if option == "5":
			self.generate_overall_report()
	
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
				report += f"Volunteer in Charge: {volunteerString if volunteerString != "" else "Currently none"}"
			print(report)
			print("--- End of report for all plans ---\n")
			input("Press Enter to continue...")