import sys

req_version = (3,12)
cur_version = sys.version_info

if cur_version < req_version:
	print ("\n*** This application requires Python version >= 3.12.0. Please consider upgrading  ***")

else:
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