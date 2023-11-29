 
# what need to do next in interface_volunteer_options.py
# 1. Initialize a CampResources instance within the InterfaceVolunteerOptions class.
# 2. Add methods in InterfaceVolunteerOptions for viewing and allocating resources or could move display resources into InterfaceVolunteerOptions as well
# 3. Update the execute_option method to include new options for resource managemen

#resources stored in camp_resources.json  

# assume a standard for needed resource per person
#assume only food_packets, medical_packets, water_packets, shelter_packets, clothing_packets, first_aid_packets, baby_packets, sanitation_packets are needed
#     assume there are resources for a week
#     // food_packets 3 packets per day
#     //medical_packets 2 packets per week
#     //water_packets 2 packets per day
#     //shelter_packets 2 packets per day
#     //clothing_packets 2 packets per week
#     //first_aid_packets 1 packet per week
#     //baby_packets 1 packet per baby
#     //sanitation_packets 1 packet per day 



import json

class CampResources:
    def __init__(self):
        self.resources = self.load_resources()


    @staticmethod
    # load resources from camp_resouces.json
    def load_resources():
        try 
            with open('camp_resources.json', 'r') as file:
                resources = json.load(file)
            except (FileNotFoundError, ValueError):
                resources = {}
            return resources
    
    #display resources in a specfic camp
    def display_resources(self,camp_id):
        camp_resources = self.resources.get(camp_id,{}).get("resources",{})
        print(f"Resources for camp {camp_id}:")
        for resource, amount in camp_resources.items():
            print(f"{resource}: {amount}")


 #update specific resources in a specfic camp
    def update_resources(self,camp_id,resource_kind,amount):
        if camp_id in self.resources and resource_kind in self.resources[camp_id]["resources"]:
            self.resources[camp_id]["resources"][resource_kind] += amount   
            self.save_resources()
            return True
        return False


 #save resources to json
    def save_resources(self):
        with open('camp_resources.json','w') as file:
            json.dump(self.resources,file,indent=4)
        return True

