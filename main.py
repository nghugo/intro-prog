from interface_main import InterfaceMain

# [START] dummy data - - - - - - - - - - - - - - - - - - - -
# from dummy import overwrite_json, dummy_users, dummy_camps, dummy_plans, dummy_refugees
# overwrite_json(dummy_users, "users.json")
# overwrite_json(dummy_camps, "camps.json")
# overwrite_json(dummy_plans, "plans.json")
# overwrite_json(dummy_refugees, "refugees.json")
# [END] dummy data - - - - - - - - - - - - - - - - - - - - -

interface = InterfaceMain(current_user = None)
interface.start()