import json


class CampResources:
    #thresholds set based on population per day (or could set to per week?)
    #food packets 3 packets per person
    #medical packets 1 pack per person
    #water packets 2 packets per person
    #shelter packets 1 packet per person
    #colthing packets 1 packet per person
    #baby packets (don't set threshold)
    #sanitation packets 2 pack per person
    
    #instance variables
    factor_food = 3
    factor_medical = 1
    factor_water = 2
    factor_shelter = 1
    factor_clothing = 1
    factor_sanitation = 2
    warnning_days = 1
    def __init__(self):
        self.resources = self.load_resources()
  
    @staticmethod
    # load resources from camp_resouces.json
    def load_resources():
        try:
            with open('camp_resources.json', 'r') as file:
                resources = json.load(file)
        except (FileNotFoundError, ValueError):
            resources = {}
        return resources

    # display resources in a specfic camp
    def display_resources(self, camp_id):
        if camp_id in self.resources:
            camp_resources = self.resources[camp_id]
            print(f"Resources for camp {camp_id}:")
            for resource, amount in camp_resources.items():
                print(f"{resource}: {amount}")
        else:
            return False
        
    def update_resources(self, camp_id, resource_kind, amount):
        """Set the amount of a resource to an absolute value."""
        if camp_id in self.resources and resource_kind in self.resources[camp_id]:
            self.resources[camp_id][resource_kind] = amount
            self.save_resources()
            return True
        else:
            return False

    def adjust_resources(self, camp_id, resource_kind, relative_amount):
        """Adjust the amount of a resource by a relative amount (positive or negative)."""
        if camp_id in self.resources and resource_kind in self.resources[camp_id]:
            self.resources[camp_id][resource_kind] += relative_amount
            self.save_resources()
            return True
        else:
            return False

    # save resources to json
    def save_resources(self):
        with open('camp_resources.json', 'w') as file:
            json.dump(self.resources, file, indent=4)
        return True
    
    #c
    def check_resource_threshold(self,camp_id):
        """Check if a resource above threshold"""
        if camp_id in self.resources:
            for resource,amount in self.resources[camp_id].items():
                threshold = self.calculate_threshold(resource)
                if amount < threshold:
                    print(f"Warning: {resource} is below threshold")
            return True
        return False
    



    def resource_factor(self):
        """Return the threshold for a given resource."""
        #thresholds set based on population per day (or could set to per week?)
        #food packets 3 packets per person
        #medical packets 1 pack per person
        #water packets 2 packets per person
        #shelter packets 1 packet per person
        #colthing packets 1 packet per person
        #baby packets (don't set threshold)
        #sanitation packets 2 pack per person

        #here need to fix to based on population 
        factors = {
            "food_packets": self.factor_food,
            "medical_packets": self.factor_medical,
            "water_packets": self.factor_water,
            "shelter_packets": self.factor_shelter,
            "clothing_packets": self.factor_clothing,
            "sanitation_packets": self.factor_sanitation
        }
        return factors

