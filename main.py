from interface import Interface

# dummy data - - - -  - - - -  - - - -  - - - - 
import json
dummyUsers = {
    "admin": {
        "password": "111",
        "isAdmin": True,
        "isActivated": True,
    },
    "volunteer1": {
        "password": "111",
        "isAdmin": False,
        "isActivated": True,
    },
    "volunteer2": {
        "password": "111",
        "isAdmin": False,
        "isActivated": True,
    },
    "volunteer3": {
        "password": "111",
        "isAdmin": False,
        "isActivated": False,
    },
}
with open("users.json", "w") as jsonFile:
    json.dump(dummyUsers, jsonFile)
# dummy data - - - -  - - - -  - - - -  - - - - 

    
interface = Interface()
interface.start()