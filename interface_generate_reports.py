import json

class InterfaceGenerateReports:

    @staticmethod
    def generate_camp_report():
            camp_name = input("Enter the name of the camp to generate the report for: ")
            with open('camps.json', 'r') as file:
                camps_data = json.load(file)
            camp_data = camps_data.get(camp_name, {})
            
            if camp_data:
                report = f"Report for {camp_name}:\n"
                report += f"Location: {camp_data.get('location', 'N/A')}\n"
                report += f"Capacity: {camp_data.get('capacity', 'N/A')}\n"
                report += f"Occupancy: {camp_data.get('occupancy', 'N/A')}\n"
                report += f"Humanitarian Plan: {camp_data.get('humanitarian_plan_in', 'N/A')}\n"
                volunteerString = ', '.join(camp_data.get('volunteer_in_charge', []))
                report += f"Volunteer in Charge: {volunteerString if volunteerString != "" else "Currently none"}\n"
                print(report)
            else:
                print(f"No data available for {camp_name}")
            input("Press Enter to continue...")
    
    @staticmethod
    def generate_overall_report():
            with open('camps.json', 'r') as file:
                camps_data = json.load(file)
            report = "Overall report for all plans:\n"

            for camp_name, camp_data in camps_data.items():
                report += f"Camp Name: {camp_name}\n"
                report += f"Location: {camp_data.get('location', 'N/A')}\n"
                report += f"Capacity: {camp_data.get('capacity', 'N/A')}\n"
                report += f"Occupancy: {camp_data.get('occupancy', 'N/A')}\n"
                report += f"Humanitarian Plan: {camp_data.get('humanitarian_plan_in', 'N/A')}\n"
                volunteerString = ', '.join(camp_data.get('volunteer_in_charge', []))
                report += f"Volunteer in Charge: {volunteerString if volunteerString != "" else "Currently none"}\n"
            print(report)
            input("Press Enter to continue...")