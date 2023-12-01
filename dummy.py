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
    "a": {
        "password": "a",
        "phone_number" : "11111",
        "email":"a@a.a",
        "is_admin": True,
        "is_activated": True,
    },  # for quick testing
    "v": {
        "password": "v",
        "phone_number" : "11111",
        "email":"v@v.v",
        "is_admin": False,
        "is_activated": True,
    },  # for quick testing
}

dummy_camps = {
  "camp1": {
    "location": "China",
    "capacity": 20,
    "humanitarian_plan_in": "planA",
    "volunteer_in_charge": ["volunteer1", "v"]
  },
  "camp2": {
    "location": "Ukraine",
    "capacity": 224,
    "humanitarian_plan_in": "planB",
    "volunteer_in_charge": ["volunteer1", "volunteer2", "v"]
  }
}

dummy_plans = {
  "Ukraine war": {
    "plan_name": "Ukraine war",
    "description": "description",
    "location": "kyiv",
    "start_date": "24/12/2022"
  },
  "planA": {
    "plan_name": "planA",
    "description": "description for planA",
    "location": "ucl",
    "start_date": "25/09/2023"
  },
  "planB": {
    "plan_name": "planB",
    "description": "description for planA",
    "location": "london",
    "start_date": "05/01/2023"
  }
}

dummy_refugees = {
  "refugee1": {
    "name": "John Doe",
    "number_of_members": 1,
    "camp_identification": "camp1",
    "medical_condition": "food starved"
  },
  "refugee2": {
    "name": "Jane Smith",
    "number_of_members": 3,
    "camp_identification": "camp1",
    "medical_condition": "healthy"
  },
  "refugee3": {
    "name": "Saul Goodman",
    "number_of_members": 3,
    "camp_identification": "camp2",
    "medical_condition": "broken bones"
  },
  "f2db20d5525c49c2adaca68b15795f36": {
    "name": "Hugo",
    "number_of_members": 2,
    "camp_identification": "camp1",
    "medical_condition": "hungry"
  }
}



def overwrite_json(object, file): 
    with open(file, "w") as json_file:
        json.dump(object, json_file, indent=2)

# overwrite_json(dummy_users)