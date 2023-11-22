class CurrentUser:
	def __init__(self, username, password, is_admin = False):
		self.username = username
	
	def set_username(self, new_username):
		self.username = new_username
	