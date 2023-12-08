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
    


def update_all_camp_values_in_resources(from_camp, to_camp):
    """ Changes all camp_id == from_camp to to_camp for all resources in refugees.json """
    # TODO Have the edit resource method call this method -> Relocate resources
    try:
        with open("resources.json", "r") as resources_file:
            resources = json.load(resources_file)
            for resource_values in resources.values():
                if resource_values["camp_id"] == from_camp:
                    resource_values["camp_id"] = to_camp 
            with open('resources.json','w') as file:
                json.dump(resources, file, indent = 2)
    except:
        print("\nError relocating resources to new camps\n")
    


def update_all_plan_values_in_camps(from_plan, to_plan):
    # TODO Have the modify_plan method in plans.py call this method -> Relocate camps
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


