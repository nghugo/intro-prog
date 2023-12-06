from users import Users

from interface_manage_users import InterfaceManageUsers
from interface_plan import InterfacePlan
from interface_camp import InterfaceCamp
from interface_manage_refugees import InterfaceManageRefugees
from interface_generate_reports import InterfaceGenerateReports
from interface_volunteer_user_details import InterfaceVolunteerUserDetails
from interface_manage_resource import InterfaceManageResource

from interface_helper import input_until_valid


class InterfaceAdminOptions:
	def __init__(self, current_user, main_self):
		self.current_user = current_user
		self.main_self = main_self
		self.interface_manage_users = InterfaceManageUsers(self.current_user)
		self.interface_plan = InterfacePlan(self.current_user)
		self.interface_camp = InterfaceCamp(self.current_user)
		self.interface_manage_refugees = InterfaceManageRefugees(self.current_user)
		self.interface_generate_reports = InterfaceGenerateReports()
		self.interface_volunteer_user_details = InterfaceVolunteerUserDetails(self.current_user)
		self.interface_manage_resources = InterfaceManageResource(self.current_user)
	
	def prompt_admin_options(self):
		users = Users.load_users()
		option = input_until_valid(
			
			input_message = f"\n<homepage>\nPlease choose an option: (logged in as {users[self.current_user.username]['fullname']} ({self.current_user.username}) - {'admin' if users[self.current_user.username]['is_admin'] else 'volunteer'})\
				\n[1] Log out\
				\n[2] Manage my user account\
				\n[3] Manage users (volunteers, admins)\
				\n[4] Manage humanitarian plans\
				\n[5] Manage camps and volunteers\
				\n[6] Manage refugee profiles\
				\n[7] Manage resources\
				\n[8] Generate a report (plans, camps)",
			is_valid=lambda user_input: user_input.isdigit() and int(user_input) > 0 and int(user_input) <= 8,
			validation_message="Unrecognized input. Please choose from the above list."
		)
		if option == "1":
			self.main_self.prompt_logout()
		if option == "2":
			# this is intended to be a volunteer option, but is included for the sake of completeness (admin has all volunteer options)
			# to edit own user details, InterfaceVolunteerUserDetails is more convenient, though admin can also do so via InterfaceManageUsers
			self.interface_volunteer_user_details.prompt_manage_my_details_options()
		if option == "3":
			self.interface_manage_users.prompt_admin_options()
		if option == "4":
			self.interface_plan.prompt_admin_options()
		if option == "5":
			self.interface_camp.prompt_admin_options()
		if option == "6":
			self.interface_manage_refugees.prompt_admin_options()
		if option == "7":
			self.interface_manage_resources.prompt_admin_options()
		if option == "8":
			self.interface_generate_reports.prompt_admin_options()