from interface import Interface
from auth import Auth

# [START] dummy data - - - - - - - - - - - - - - - - - - - -
from dummy import dummy_users, overwrite_users_json
overwrite_users_json(dummy_users)  # overwrite users.json
# [END] dummy data - - - - - - - - - - - - - - - - - - - - -

auth = Auth()
interface = Interface(auth)
interface.start()