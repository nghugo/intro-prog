class User:
	def __init__(self, username, password, isAdmin = False):
		self.username = username
		self.password = password
		self.isAdmin = isAdmin