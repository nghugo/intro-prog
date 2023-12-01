from interface_helper import input_until_valid
from interface_camp import InterfaceCamp
from interface_manage_users import InterfaceManageUsers
from interface_generate_reports import InterfaceGenerateReports
from interface_plan import InterfacePlan


class InterfaceAdminOptions:
	def __init__(self, users, current_user):
		self.users = users
		self.current_user = current_user
		self.interface_manage_users = InterfaceManageUsers(self.users, self.current_user)
		self.interface_generate_reports = InterfaceGenerateReports()
		self.interface_camp = InterfaceCamp(self.users, self.current_user)
		self.interface_plan = InterfacePlan(self.users, self.current_user)
		# initialise self.plans
	
	def prompt_admin_options(self):  # TODO: implement handling for the other option values
		option = input_until_valid(
			# when extending this list, make sure the input message matches the is_valid validation function and the options in interface_admin_options.py
			input_message = f"\n<homepage>\nPlease choose an option: (logged in as {self.current_user.username} ({'admin' if self.users.users[self.current_user.username]['is_admin'] else 'volunteer'}))\
				\n[1] Log out\
				\n[2] Manage users (volunteers, admins)\
				\n[3] Manage humanitarian plans\
				\n[4] Manage camps\
				\n[5] Generate a report (plans, camps)",
			is_valid=lambda user_input: user_input.isdigit() and int(user_input) > 0 and int(user_input) <= 5,
			validation_message="Unrecognized input. Please choose from the above list."
		)
		if option == "1":
			self.prompt_logout()
		if option == "2":
			self.interface_manage_users.prompt_admin_options()
		if option == "3":
			self.interface_plan.prompt_admin_options()
		if option == "4":
			self.interface_camp.prompt_admin_options()
		if option == "5":
			self.interface_generate_reports.prompt_admin_options()
	

	def prompt_logout(self):
		print("\nAre you sure you want to log out?")
		user_input = input_until_valid(
			input_message="Please confirm your logout (y/n):\n[y] Yes\n[n] No",
			is_valid=lambda user_input: user_input == "y" or user_input == "n",
			validation_message="Unrecognized input. Please confirm your logout (y/n):\n[y] Yes\n[n] No"
		)
		if user_input == "y":
			print(f"Goodbye {self.current_user.username}! You are now logged out.")
			self.current_user = None