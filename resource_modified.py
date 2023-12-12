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
        self.factors = self.load_factors()
  
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
            print(f"Resources for {camp_id}:")
            for resource, amount in camp_resources.items():
                print(f"-> {resource}: {amount}")
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
    
    @staticmethod
    def load_factors():
        try:
            with open('threshold_parameters.json', 'r') as file:
                factors = json.load(file)
        except (FileNotFoundError, ValueError):
            factors = {  #defualt value for resources
                "factor_food":3,
                "factor_medical":1,
                "factor_wate":2,
                "factor_shelter":1,
                "factor_clothing":1,
                "factor_sanitation":2,
                "warnning_days":1
            }
        return factors
    
    def resource_factor(self):
        """Return the threshold for a given resource."""
        data = self.factors
        factors = {
            "food_packets": data["food_packets_factor"],
            "medical_packets": data["medical_packets_factor"],
            "water_packets": data["water_packets_factor"],
            "shelter_packets": data["shelter_packets_factor"],
            "clothing_packets": data["clothing_packets_factor"],
            "sanitation_packets": data["sanitation_packets_factor"]
        }
        return factors
    @staticmethod
    def reset_factor(reset_value):
        """reset_value should be a dictionary"""
        with open("threshold_parameters.json",'w') as file:
            json.dump(reset_value,file,indent=2)
            return True

