from interface_main import InterfaceMain

# [START] dummy data - - - - - - - - - - - - - - - - - - - -
from dummy import dummy_users, overwrite_users_json
overwrite_users_json(dummy_users)  # overwrite users.json
# [END] dummy data - - - - - - - - - - - - - - - - - - - - -

interface = InterfaceMain(current_user = None)
interface.start()