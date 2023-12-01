from interface_helper import input_until_valid, is_valid_date
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

	def show_options(self, option):
		# option 1 is log out, which is handled at interface_main.py
		if option == "2":
			self.interface_manage_users.show_admin_options()
		if option == "3":
			self.interface_plan.show_admin_options()
		if option == "5":
			self.interface_generate_reports.show_admin_options()
		if option == "6":
			self.interface_camp.show_admin_options()