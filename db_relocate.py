import json

# cannot import from refugee.py, resources.py, or camp_modified.py
# otherwise circular import



def update_all_camp_values_in_refugees(from_camp, to_camp):
    """ Changes all camp_id == from_camp to to_camp for all refugees in refugees.json """
    try:
        with open("refugees.json", "r") as refugees_file:
            refugees = json.load(refugees_file)
            for refugee_values in refugees.values():
                if refugee_values["camp_id"] == from_camp:
                    refugee_values["camp_id"] = to_camp 
            with open('refugees.json','w') as file:
                json.dump(refugees, file, indent = 2)
    except:
        print("\nError relocating refugees to new camps\n")
    


def update_all_camp_values_in_camp_resources(from_camp, to_camp):
    """ Changes all camp_id == from_camp to to_camp for all resources in refugees.json """
    try:
        with open("camp_resources.json", "r") as camp_resources_file:
            camp_resources = json.load(camp_resources_file)
            camp_resources[to_camp] = camp_resources.pop(from_camp)
            with open('camp_resources.json','w') as file:
                json.dump(camp_resources, file, indent = 2)
    except:
        print("\nError relocating resources to new camps\n")
    


def update_all_plan_values_in_camps(from_plan, to_plan):
    try:
        with open("camps.json", "r") as camps_file:
            camps = json.load(camps_file)
            for camp_values in camps.values():
                if camp_values["humanitarian_plan_in"] == from_plan:
                    camp_values["humanitarian_plan_in"] = to_plan 
            with open('camps.json','w') as file:
                json.dump(camps, file, indent = 2)
    except:
        print("\nError relocating camps by plan\n")

