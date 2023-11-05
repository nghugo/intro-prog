class User:
	def __init__(self, name, password, isAdmin = False):
		self.name = name
		self.password = password
		self.isAdmin = isAdmin