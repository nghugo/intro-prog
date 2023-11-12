from interface import Interface
from auth import Auth

# overwrite users.json with dummy data - - - -  - - - -  - - - -  - - - - 
from dummy import dummy_users, overwrite_users_json
overwrite_users_json(dummy_users)

# dummy data - - - -  - - - -  - - - -  - - - - 

auth = Auth()
interface = Interface(auth)
interface.start()