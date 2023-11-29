import json

dummy_users = {
    "admin": {
        "password": "111",
        "phone_number" : "11111",
        "email":"admin@mail.com",
        "is_admin": True,
        "is_activated": True,
    },
    "volunteer1": {
        "password": "111",
        "phone_number" : "5028382739",
        "email":"volunteer1@mail.com",
        "is_admin": False,
        "is_activated": True,
    },
    "volunteer2": {
        "password": "111",
        "phone_number" : "9027346729",
        "email":"volunteer2@mail.com",
        "is_admin": False,
        "is_activated": True,
    },
    "volunteer3": {
        "password": "111",
        "phone_number" : "11111",
        "email":"volunteer3@mail.com",
        "is_admin": False,
        "is_activated": False,
    },
}

def overwrite_users_json(dummyUsers):
    with open("users.json", "w") as json_file:
        json.dump(dummyUsers, json_file)

# overwrite_users_json(dummy_users)