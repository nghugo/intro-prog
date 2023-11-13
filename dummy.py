import json

dummy_users = {
    "admin": {
        "password": "111",
        "is_admin": True,
        "is_activated": True,
    },
    "volunteer1": {
        "password": "111",
        "is_admin": False,
        "is_activated": True,
    },
    "volunteer2": {
        "password": "111",
        "is_admin": False,
        "is_activated": True,
    },
    "volunteer3": {
        "password": "111",
        "is_admin": False,
        "is_activated": False,
    },
}

def overwrite_users_json(dummyUsers):
    with open("users.json", "w") as json_file:
        json.dump(dummyUsers, json_file)