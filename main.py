from interface import Interface

# overwrite users.json with dummy data - - - -  - - - -  - - - -  - - - - 
from dummy import dummy_users, overwrite_users_json
overwrite_users_json(dummy_users)

# dummy data - - - -  - - - -  - - - -  - - - - 

    
interface = Interface()
interface.start()