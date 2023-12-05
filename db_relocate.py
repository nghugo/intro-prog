import json

# cannot import from refugee.py, resources.py, or camp_modified.py
# otherwise circular import

def load_refugees():
    try:
        with open("refugees.json", "r") as json_file:
            json_load = json.load(json_file)
            return json_load
    except FileNotFoundError:
        return {}

def relocate_all_refugees_by_camp(from_camp, to_camp):
    """ Changes all camp_id == from_camp to to_camp for all refugees in refugees.json """
    try:
        with open("refugees.json", "r") as refugees_file:
            refugees = json.load(refugees_file)
            for refugee_values in refugees.values():
                if refugee_values["camp_id"] == from_camp:
                    refugee_values["camp_id"] = to_camp 
            with open('refugees.json','w') as file:
                json.dump(refugees, file, indent=2)
    except:
        print("\nError relocating refugees by camp\n")
    

def relocate_all_resources_by_camp(from_camp, to_camp):
    pass  # TODO -> Relocate resources

def relocate_all_camps_by_plan(from_plan, to_plan):
    pass  # TODO -> Relocate camps

