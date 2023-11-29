import json

import os

class InterfaceGenerateReports:

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
                report += f"Capacity: {camp_data.get('capacity', 'N/A')}\n"
                report += f"Occupancy: {camp_data.get('occupancy', 'N/A')}\n"
                report += f"Humanitarian Plan: {camp_data.get('humanitarian_plan_in', 'N/A')}\n"
                volunteerString = ', '.join(camp_data.get('volunteer_in_charge', []))
                report += f"Volunteer in Charge: {volunteerString if volunteerString != "" else "Currently none"}"
                print(report)
                print(f"--- End of report for {camp_name} ---\n")
                save_report = input("Do you want to save this overall report as a text file? (y/n): ").lower()
                if save_report == 'y':
                     file_name = "overall_camps_report.txt"
                     with open(file_name, 'w') as file:
                          file.write(report)
                     print(f"Report for {camp_name} has been saved to {file_name}")
                else:
                     print("Report not saved.")
            else:
                print(f"\nNo data available for {camp_name}")
                
            input("Press Enter to continue...")
    
    @staticmethod
    def generate_overall_report():
            with open('camps.json', 'r') as file:
                camps_data = json.load(file)
            print("\n--- Report for all camps in all plans ---")
            report = ""

            for camp_name, camp_data in camps_data.items():
                report += f"Camp Name: {camp_name}\n"
                report += f"Location: {camp_data.get('location', 'N/A')}\n"
                report += f"Capacity: {camp_data.get('capacity', 'N/A')}\n"
                report += f"Occupancy: {camp_data.get('occupancy', 'N/A')}\n"
                report += f"Humanitarian Plan: {camp_data.get('humanitarian_plan_in', 'N/A')}\n"
                volunteerString = ', '.join(camp_data.get('volunteer_in_charge', []))
                report += f"Volunteer in Charge: {volunteerString if volunteerString != "" else "Currently none"}"
            print(report)
            print("--- End of report all camps in all plans ---\n")
            input("Press Enter to continue...")
