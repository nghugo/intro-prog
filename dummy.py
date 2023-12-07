import json
import secrets
import hashlib

initial_password = "111"

dummy_users = {
    "admin": {
        "fullname": "Homer Simpsons",
        "password": "111",
        "phone_number": "11111",
        "email": "admin@mail.com",
        "is_admin": True,
        "is_activated": True,
    },
    "volunteer1": {
        "fullname": "Lisa Simpsons",
        "password": "111",
        "phone_number": "5028382739",
        "email": "volunteer1@mail.com",
        "is_admin": False,
        "is_activated": True,
    },
    "volunteer2": {
        "fullname": "Peter Griffin",
        "password": "111",
        "phone_number": "9027346729",
        "email": "volunteer2@mail.com",
        "is_admin": False,
        "is_activated": True,
    },
    "volunteer3": {
        "fullname": "Brian Griffin",
        "password": "111",
        "phone_number": "11111",
        "email": "volunteer3@mail.com",
        "is_admin": False,
        "is_activated": False,
    },
    "a": {
        "fullname": "Gus Fring",
        "password": "a",
        "phone_number": "11111",
        "email": "a@a.a",
        "is_admin": True,
        "is_activated": True,
    },  # for quick testing
    "v": {
        "fullname": "Hank Schrader",
        "password": "v",
        "phone_number": "11111",
        "email": "v@v.v",
        "is_admin": False,
        "is_activated": True,
    },  # for quick testing
}

dummy_camps = {
    "camp1": {
        "location": "China",
        "max_capacity": 20,
        "humanitarian_plan_in": "planA",
        "volunteers_in_charge": ["volunteer1", "v"]
    },
    "camp2": {
        "location": "Ukraine",
        "max_capacity": 224,
        "humanitarian_plan_in": "planB",
        "volunteers_in_charge": ["volunteer1", "volunteer2", "v"]
    },
    "camp3": {
        "location": "UK",
        "max_capacity": 30,
        "humanitarian_plan_in": "planC",
        "volunteers_in_charge": ["v"]
    },
    "camp4": {
        "location": "China",
        "max_capacity": 10,
        "humanitarian_plan_in": "planA",
        "volunteers_in_charge": ["volunteer2"]
    },
    "camp5": {
        "location": "Ukraine",
        "max_capacity": 13,
        "humanitarian_plan_in": "planB",
        "volunteers_in_charge": ["volunteer1", "v"]
    }
}

dummy_plans = {
    "Ukraine war": {
        "description": "Helping victims of Ukraine war",
        "location": "kyiv",
        "start_date": "24/12/2022"
    },
    "planA": {
        "description": "UCL campaign for refugee education",
        "location": "ucl",
        "start_date": "25/09/2023"
    },
    "planB": {
        "description": "Helping Asylum Seekers and refugees in London since 2023",
        "location": "london",
        "start_date": "05/01/2023"
    }
}

dummy_refugees = {
    "refugee1": {
        "fullname": "John Doe",
        "number_of_members": 1,
        "camp_id": "camp1",
        "medical_condition": "food starved"
    },
    "refugee2": {
        "fullname": "Jane Smith",
        "number_of_members": 3,
        "camp_id": "camp1",
        "medical_condition": "healthy"
    },
    "refugee3": {
        "fullname": "Pepe the Frog",
        "number_of_members": 3,
        "camp_id": "camp3",
        "medical_condition": "dehydrated"
    },
    "refugee4": {
        "fullname": "Saul Goodman",
        "number_of_members": 3,
        "camp_id": "camp2",
        "medical_condition": "broken bones"
    },
    "f2db20d5525c49c2adaca68b15795f36": {
        "fullname": "Hugo",
        "number_of_members": 1,
        "camp_id": "camp3",
        "medical_condition": "hungry"
    }
}


def overwrite_json(object, file):
    with open(file, "w") as json_file:
        json.dump(object, json_file, indent=2)


for username, user_info in dummy_users.items():
    
    salt = secrets.token_hex(16)
    hashed_password = hashlib.sha256((initial_password + salt).encode('utf-8')).hexdigest()

    
    user_info["password"] = hashed_password
    user_info["salt"] = salt


overwrite_json(dummy_users, 'users.json')
