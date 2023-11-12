class User:
	def __init__(self, username, password, is_admin = False):
		self.username = username
		self.password = password
		self.is_admin = is_admin
	
	# TODO: Add to this class later to provide functionality for the current user