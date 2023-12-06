from users import Users

from interface_manage_refugees import InterfaceManageRefugees
from interface_volunteer_user_details import InterfaceVolunteerUserDetails
from interface_manage_resource import InterfaceManageResource
from interface_camp import InterfaceCamp
from interface_helper import input_until_valid

class InterfaceVolunteerOptions:
	def __init__(self, current_user, main_self):
		self.current_user = current_user
		self.main_self = main_self
		self.interface_manage_refugees = InterfaceManageRefugees(self.current_user)
		self.interface_volunteer_user_details = InterfaceVolunteerUserDetails(self.current_user)
		self.interface_camp = InterfaceCamp(self.current_user)
		self.interface_manage_resource = InterfaceManageResource(self.current_user)

	def prompt_volunteer_options(self):  # TODO: implement handling for the other option values
		users = Users.load_users()
		option = input_until_valid(			
			input_message = f"\n<homepage>\nPlease choose an option: (logged in as {users[self.current_user.username]['fullname']} ({self.current_user.username}) - {'admin' if users[self.current_user.username]['is_admin'] else 'volunteer'})\
				\n[1] Log out\
				\n[2] Manage my user account\
				\n[3] Manage camps\
				\n[4] Manage refugee profiles\
				\n[5] Manage resources\
				\n[6] TODO placeholder",
			is_valid=lambda user_input: user_input.isdigit() and int(user_input) > 0 and int(user_input) <= 6,
			validation_message="Unrecognized input. Please choose from the above list."
		)
		if option == "1":
			self.main_self.prompt_logout()
		if option == "2":
			self.interface_volunteer_user_details.prompt_manage_my_details_options()
		if option == "3":
			self.interface_camp.prompt_volunteer_options()
		if option == "4":
			self.interface_manage_refugees.prompt_volunteer_options()
		if option == "5":
			self.interface_manage_resource.prompt_volunteer_options()
		if option == "6":
			pass
	