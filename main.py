from interface import Interface
from users import Users

# [START] dummy data - - - - - - - - - - - - - - - - - - - -
# from dummy import dummy_users, overwrite_users_json
# overwrite_users_json(dummy_users)  # overwrite users.json
# [END] dummy data - - - - - - - - - - - - - - - - - - - - -

users = Users()
interface = Interface(users = users, current_user = None)
interface.start()