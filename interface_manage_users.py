import pandas as pd
import hashlib
import secrets

from users import Users
from interface_helper import input_until_valid, input_until_valid_email, input_until_valid_name

class InterfaceManageUsers:
	def __init__(self, current_user):
		self.current_user = current_user

	def prompt_admin_options(self):
		option = input_until_valid(
			input_message = f"\n<homepage/manage-users>\nPlease choose a user management option below:\
				\n[1] CANCEL\
				\n[2] List all users\
				\n[3] Add user\
				\n[4] Edit user\
				\n[5] Delete user\
				\n[6] Activate user\
				\n[7] Deactivate user",
			is_valid=lambda user_input: user_input.isdigit() and int(user_input) > 0 and int(user_input) <= 7,
			validation_message="Unrecognized input. Please choose from the above list."
		)
		if option == "1":
			return  # option 1 is cancel, so just return
		if option == "2":
			self.list_users()
		if option == "3":
			self.prompt_add_user()
		if option == "4":
			self.prompt_modify_user()
		if option == "5":
			self.prompt_delete_user()
		if option == "6":
			self.prompt_activate_user()
		if option == "7":
			self.prompt_deactivate_user()

	def prompt_add_user(self):
		users = Users.load_users()
		self.print_all_users()
		username = input_until_valid(
			input_message="Enter the username for the new user, or leave empty to abort:",
			is_valid=lambda user_input: user_input == "" or user_input not in users,
			validation_message="Username is already taken. Please enter a different username for the new user. Leave empty to abort:"
		)
		if username == "":
			print("User creation aborted.")
			return  # early termination

		plain_text_password = input_until_valid(
			input_message=f"Please enter the password for the new user (5+ digits)",
			is_valid=lambda user_input: len(user_input) >= 5,
			validation_message=f"Unrecognized input. Please specify the password for the new user (5+ digits or leave empty)"
		)
		
		salt = secrets.token_hex(16)
		hashed_password = hashlib.sha256((plain_text_password + salt).encode('utf-8')).hexdigest()

		fullname = input_until_valid_name(
			input_message="Enter the full name of the new user:",
			validation_message="User's full name can only contain letters and spaces. Please re-enter."
		)

		email=input_until_valid_email("Enter the email for the new user (format: xxx@yyy.zzz with no spaces):")
		
		phone_number = input_until_valid(
			input_message=f"Enter the new phone number (5+ digits or leave empty):",
			is_valid=lambda user_input: (user_input == "") or (
				user_input.isdigit() and len(user_input) >= 5),
			validation_message=f"Unrecognized input. Please enter the new phone number (5+ digits or leave empty)"
		)
		is_admin = input_until_valid(
			input_message="Specify if the new user is an admin (t/f):\n[t] True\n[f] False",
			is_valid=lambda user_input: user_input == "t" or user_input == "f",
			validation_message="Unrecognized input. Please specify if the new user is an admin (t/f):\n[t] True\n[f] False"
		)
		is_activated = input_until_valid(
			input_message="Specify if the new user is activated (t/f):\n[t] True\n[f] False",
			is_valid=lambda user_input: user_input == "t" or user_input == "f",
			validation_message="Unrecognized input. Please specify if the new user is activated (t/f):\n[t] True\n[f] False"
		)


		confirm = input_until_valid(
			input_message=f"Please confirm details of the new user (y/n):\
				\n->Username: {username}\
				\n->Password: {plain_text_password}\
				\n->Full Name: {fullname}\
				\n->Email: {email}\
				\n->phone_number: {phone_number}\
				\n->Is Admin: {"yes" if is_admin == "t" else "no"}\
				\n->Is Activated: {"yes" if is_activated == "t" else "no"}\
				\n[y] Yes\n[n] No (abort)",
			is_valid=lambda user_input: user_input == "y" or user_input == "n",
			validation_message="Unrecognized input. Please confirm details of the new user (y/n):\n[y] Yes\n[n] No (abort)"
		)
		if confirm == "y":
			success = Users.add_user(
				username=username, 
				salt=salt,
				password=hashed_password, 
				fullname=fullname, 
				email=email,phone_number=phone_number, 
				is_admin=is_admin == "t", 
				is_activated=is_activated == "f")
			if success:
				print(f"Successfully added user {username}")
			else:
				print(f"Failed to add user {username}")
		else:
			print(f"Aborted user addition.")

	def prompt_activate_user(self):
		self.print_all_users()
		users = Users.load_users()
		username = input_until_valid(
			input_message="Enter the username of the user to activate or leave empty to abort:",
			is_valid=lambda user_input: user_input in users or user_input == "",
			validation_message="Username not found. Please enter an existing username or leave empty to abort."
		)
		if username == "":
			print("User activation aborted.")
		else:
			Users.modify_user(username, "is_activated", True)
			print(f"User {username} has been activated.")

	def prompt_deactivate_user(self):
		self.print_all_users()
		users = Users.load_users()
		username = input_until_valid(
			input_message="Enter the username of the user to deactivate or leave empty to abort:",
			is_valid=lambda user_input: user_input in users or user_input == "",
			validation_message="Username not found. Please enter an existing username or leave empty to abort."
		)
		if username == "":
			print("User deactivation aborted.")
		elif username == self.current_user.username:
			print(
				"You are not allowed to deactivate your own account. User deactivation aborted.")
		else:
			Users.modify_user(username, "is_activated", False)
			print(f"User {username} has been deactivated.")

	def prompt_modify_user(self):
		users = Users.load_users()
		self.print_all_users()
		username = input_until_valid(
			input_message="Enter the username of the user to modify or leave empty to abort:",
			is_valid=lambda user_input: user_input in users or user_input == "",
			validation_message="Username not found. Please enter an existing username or leave empty to abort."
		)
		
		if username == "":
			print("User modification aborted.")
			return  # early termination
		
		Users.print_current_user_values(username)

		field = input_until_valid(
			input_message="Enter the field (username/password/fullname/email/phone_number/is_admin/is_activated) to modify, or leave empty to abort:",
			is_valid=lambda user_input: user_input in {
				"", "username", "password", "fullname", "email", "phone_number", "is_admin", "is_activated"},
			validation_message="Unrecognized input. Please enter a valid field (username/password/email/phone_number/is_admin/is_activated)."
		)
		if field == "":
			print("User modification aborted.")
			return
		if field in {"is_admin", "is_activated"}:
			if username == self.current_user.username:
				# do not allow deactivation or admin disabling of own account
				print(f"You are not allowed to modify the {
					  field} field of your own account. Modification aborted.")
				return
			value = input_until_valid(
				input_message=f"Specify the new value for the {field} field (t/f):\n[t] True\n[f] False",
				is_valid=lambda user_input: user_input == "t" or user_input == "f",
				validation_message=f"Unrecognized input. Please specify the new value for the {field} field (t/f):\n[t] True\n[f] False"
			)
			value = True if value == "t" else False
		elif field == "username":
			value = input_until_valid(
				input_message=f"Enter the new username",
				is_valid=lambda user_input: user_input not in users,
				validation_message=f"Username already taken. Please enter a different username."
			)
		elif field == "fullname":
			value = input_until_valid_name(
				input_message = "Please enter the new full name",
				validation_message = "Your full name can only contain letters and spaces. Please re-enter."
				)
		elif field == "email":
			value=input_until_valid_email("Enter the new email (format: xxx@yyy.zzz with no spaces):")
		elif field == "phone_number":
			value = input_until_valid(
				input_message=f"Please enter the new phone number (5+ digits or leave empty)",
				is_valid=lambda user_input: (user_input == "") or (
					user_input.isdigit() and len(user_input) >= 5),
				validation_message=f"Unrecognized input. Please specify the new phone number (5+ digits or leave empty)"
			)
		elif field == "password":
			plain_text_password = input_until_valid(
				input_message=f"Please enter the new password (5+ characters)",
				is_valid=lambda user_input: len(user_input) >= 5,
				validation_message=f"Unrecognized input. Please specify the new password (5+ characters)"
			)
			salt = users[username]["salt"]
			hashed_password = hashlib.sha256((plain_text_password + salt).encode('utf-8')).hexdigest()
			value = hashed_password
		else:
			value = input_until_valid(f"Please enter the new value for the {field} field:")

		if field == "username":
			prev_value = username
		elif field == "password":
			prev_value = "[HIDDEN]"
		else:
			prev_value = users[username][field]

		confirm = input_until_valid(
			input_message=f"Please confirm details of the user modification (y/n):\
				\n->Username: {username}\
				\n->Field: {field}\
				\n->Previous Value: {prev_value}\
				\n->New Value: {value if field != "password" else plain_text_password}\
				\n[y] Yes\
				\n[n] No (abort)",
			is_valid=lambda user_input: user_input == "y" or user_input == "n",
			validation_message="Unrecognized input. Please confirm details of the user modification (y/n):\n[y] Yes\n[n] No (abort)"
		)
		if confirm == "y":
			# modify persistent store and reload current_user if username matches
			Users.modify_user(username, field, value)
			if field == "username" and self.current_user.username == username:
				self.current_user.set_username(value)

			print("Successfully modified user.")
		else:
			print("User modification aborted.")

	def prompt_delete_user(self):
		users = Users.load_users()
		self.print_all_users()
		username = input_until_valid(
			input_message="\nEnter the username of the user to delete or leave empty to abort:",
			is_valid=lambda user_input: user_input in users or user_input == "",
			validation_message="Username not found. Please enter an existing username or leave empty to abort."
		)
		if username == "":
			print("User deletion aborted.")
		elif username == self.current_user.username:
			print(
				"You are not allowed to delete your own account. User deletion aborted.")
		else:
			Users.delete_user(username)
			print(f"User {username} has been deleted.")

	@staticmethod
	def list_users():
		users = Users.load_users()
		print("--- Users are as follows ---")
		# use pandas for pretty print
		users_df = pd.DataFrame.from_dict(users).transpose()

		users_df = users_df.loc[:, ~users_df.columns.isin(["salt"])]
		users_df["password"] = "[HIDDEN]"

		print(users_df)
		print("--- End of users list ---")
		input("Press Enter to continue...")
	
	@staticmethod
	def print_all_users():
		users = Users.load_users()
		print(f"\nExisting username(s): {", ".join(users.keys()) if users else 'None found'}")