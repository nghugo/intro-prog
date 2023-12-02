from collections import defaultdict
import json

from camp_modified import Camp

def load_refugees():
    try:
        with open("refugees.json", "r") as json_file:
            json_load = json.load(json_file)
            return json_load
    except FileNotFoundError:
        return {}

def get_accessible_refugees_sep_by_camp(username) -> dict:
    accessible_refugees = get_accessible_refugees(username)
    accessible_refugees_sep_by_camp = defaultdict(list)
    for refugee_id, refugee_values in accessible_refugees.items():
        accessible_refugees_sep_by_camp[refugee_values["camp_id"]].append((refugee_id, refugee_values))
    return accessible_refugees_sep_by_camp


def get_accessible_refugees(username):
    all_refugees = load_refugees()
    accessible_refugees = {refugee_id: refugee_values for refugee_id, refugee_values in all_refugees.items() 
                        if Camp.user_has_access(camp_id = refugee_values["camp_id"], username = username)}
    return accessible_refugees