import json

# password for most users are 111
# exceptions: user a has password a, and user v has password v
dummy_users = {
  "admin": {
    "fullname": "Homer Simpsons",
    "password": "d2cdf18f2676375dc4f0f6bda15ad3198fc5ef67961ba4a15f45e5ec70726228",
    "phone_number": "11111",
    "email": "admin@mail.com",
    "is_admin": True,
    "is_activated": True,
    "salt": "80306a615dcab5952ea15e3369ed7196"
  },
  "volunteer1": {
    "fullname": "Lisa Simpsons",
    "password": "3c7ff0ad540f6971a970b1121626c91d787ab2a21fff82ce3fe116decfa8e453",
    "phone_number": "5028382739",
    "email": "volunteer1@mail.com",
    "is_admin": False,
    "is_activated": True,
    "salt": "1a51efcd45db38f7ab3814594e94a141"
  },
  "volunteer2": {
    "fullname": "Peter Griffin",
    "password": "acb5b70881ce130457ddf24c818a48b52f13e1f063c4845cee90f03a9c533706",
    "phone_number": "9027346729",
    "email": "volunteer2@mail.com",
    "is_admin": False,
    "is_activated": True,
    "salt": "00782b248ddee3ccc2fcc7975d2f0933"
  },
  "volunteer3": {
    "fullname": "Brian Griffin",
    "password": "3a5f51060a72e282117bb2551f00d134c2c429da7791e65e4301304c3ea3801c",
    "phone_number": "11111",
    "email": "volunteer3@mail.com",
    "is_admin": False,
    "is_activated": False,
    "salt": "05f7b58fc331c1743fcd0516e0aefd3e"
  },
  "a": {
    "fullname": "Gus Fring",
    "password": "234df68fd1d98e9642de27a17cd850a34ab1f8c48f5dba100751c624263ec675",
    "phone_number": "11111",
    "email": "a@a.a",
    "is_admin": True,
    "is_activated": True,
    "salt": "b13b214a2241462e9479b2704b99e65d"
  },
  "v": {
    "fullname": "Hank Schrader",
    "password": "f2f82dd7fd56621f0ad05249a32f9d3743ef915aae6e5bcd2b06486e03026353",
    "phone_number": "11111",
    "email": "v@v.v",
    "is_admin": False,
    "is_activated": True,
    "salt": "942e02e419c6fec198e4a9513d62cfab"
  },
  "test": {
    "password": "8094586435e1981fa0622edfd3401274804aa7b8685d31d323e66daf33c0532c",
    "fullname": "Test",
    "phone_number": "11111",
    "email": "test@f.com",
    "is_admin": False,
    "is_activated": True,
    "salt": "c72d035a6b87c81e15cfaf806dbca845"
  }
}

dummy_camps = {
  "camp1": {
    "location": "London",
    "max_capacity": 20,
    "humanitarian_plan_in": "planB",
    "volunteers_in_charge": [
      "volunteer1",
      "v"
    ]
  },
  "camp2": {
    "location": "UCL Engineering Building",
    "max_capacity": 224,
    "humanitarian_plan_in": "planA",
    "volunteers_in_charge": [
      "volunteer1",
      "volunteer2",
      "v"
    ]
  },
  "camp3": {
    "location": "JBS Haldane Student Hub",
    "max_capacity": 30,
    "humanitarian_plan_in": "planA",
    "volunteers_in_charge": [
      "v"
    ]
  },
  "camp4": {
    "location": "Birkbeck",
    "max_capacity": 10,
    "humanitarian_plan_in": "planA",
    "volunteers_in_charge": [
      "volunteer2"
    ]
  },
  "camp5": {
    "location": "Euston Station",
    "max_capacity": 13,
    "humanitarian_plan_in": "planB",
    "volunteers_in_charge": [
      "volunteer1",
      "v"
    ]
  },
  "camp6": {
    "location": "Kyiv",
    "max_capacity": 130,
    "humanitarian_plan_in": "Ukraine war",
    "volunteers_in_charge": [
      "volunteer1",
      "v"
    ]
  },
  "camp7": {
    "location": "Outside Kyiv",
    "max_capacity": 120,
    "humanitarian_plan_in": "Ukraine war",
    "volunteers_in_charge": [
      "volunteer2",
      "v"
    ]
  }
}

dummy_plans = {
  "Ukraine war": {
    "description": "Helping victims of Ukraine war",
    "country": "Ukraine",
    "start_date": "24/12/2022",
    "end_date": "12/01/2024",
    "status": "Active"
  },
  "planA": {
    "description": "UCL campaign for refugee education",
    "country": "United Kingdom",
    "start_date": "25/09/2023",
    "end_date": "12/01/2024",
    "status": "Active"
  },
  "planB": {
    "description": "Helping Asylum Seekers and refugees in London since 2023",
    "country": "United Kingdom",
    "start_date": "05/01/2023",
    "end_date": "12/01/2024",
    "status": "Active"
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

dummy_resources = {
  "camp1": {
    "food_packets": 10,
    "medical_packets": 10,
    "water_packets": 5,
    "shelter_packets": 5,
    "clothing_packets": 5,
    "first_aid_packets": 5,
    "baby_packets": 3,
    "sanitation_packets": 10
  },
  "camp2": {
    "food_packets": 2,
    "medical_packets": 3,
    "water_packets": 4,
    "shelter_packets": 5,
    "clothing_packets": 6,
    "first_aid_packets": 7,
    "baby_packets": 8,
    "sanitation_packets": 9
  },
  "camp3": {
    "food_packets": 0,
    "medical_packets": 0,
    "water_packets": 0,
    "shelter_packets": 0,
    "clothing_packets": 0,
    "first_aid_packets": 0,
    "baby_packets": 0,
    "sanitation_packets": 0
  },
  "camp4": {
    "food_packets": 0,
    "medical_packets": 0,
    "water_packets": 0,
    "shelter_packets": 0,
    "clothing_packets": 0,
    "first_aid_packets": 0,
    "baby_packets": 0,
    "sanitation_packets": 0
  },
  "camp5": {
    "food_packets": 0,
    "medical_packets": 0,
    "water_packets": 0,
    "shelter_packets": 0,
    "clothing_packets": 0,
    "first_aid_packets": 0,
    "baby_packets": 0,
    "sanitation_packets": 0
  }
}


def overwrite_json(object, file):
    with open(file, "w") as json_file:
        json.dump(object, json_file, indent=2)
