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
    def __init__(self):
        self.resources = self.load_ALL_resources()
        self.factors = self.load_factors()
    @staticmethod
    def load_ALL_resources():
        with open('camp_resources.json','r') as file:
            try:
                resources = json.load(file)
            except ValueError:
                resources = {}
        return resources

    
    @staticmethod
    def load_active_resources():
            """load all camps under active plans from camps.json"""

            with open("plans.json", "r") as json_file:  # https://www.w3schools.com/python/ref_func_open.asp
                try: 
                    plans = json.load(json_file)
                except ValueError: 
                    plans = {}

            with open('camps.json', 'r') as file:
                try:
                    camp_data = json.load(file)
                except ValueError:
                    camp_data = {}
            with open('camp_resources.json','r') as file:
                try:
                    resource = json.load(file)
                except ValueError:
                    resource = {}
                return {key: val for key, val in resource.items() if plans[camp_data[key]["humanitarian_plan_in"]]["status"] == "Active"}
            
    # display active resources in a specific camp
    def display_active_resources(self, camp_id):
        active_resources = self.load_active_resources()
        if camp_id in active_resources:
            camp_resources = active_resources[camp_id]
            print(f"Resources for {camp_id}:")
            for resource, amount in camp_resources.items():
                print(f"-> {resource}: {amount}")
            return True # return True when resources are avaliable 
        return False
	
	# display all resources in a specific camp
    def display_ALL_resources(self, camp_id):
        ALL_resources = self.load_ALL_resources()
        if camp_id in ALL_resources:
            camp_resources = ALL_resources[camp_id]
            print(f"Resources for {camp_id}:")
            for resource, amount in camp_resources.items():
                print(f"-> {resource}: {amount}")
            return True # return True when resources are avaliable 
        return False


    def overwrite_resources_amount(self, camp_id, resource_kind, amount):
        """Set the amount of a resource to the given value."""
        if camp_id in self.resources and resource_kind in self.resources[camp_id]:
            self.resources[camp_id][resource_kind] = amount
            self.save_resources()
            return True
        return False
	
    def increment_resources_amount(self, camp_id, resource_kind, relative_amount):
        """Adjust the amount of a resource by a relative amount (positive or negative)."""
        if camp_id in self.resources and resource_kind in self.resources[camp_id]:
            self.resources[camp_id][resource_kind] += relative_amount
            self.save_resources()
            return True
        return False

    # save resources to json
    def save_resources(self):
        with open('camp_resources.json', 'w') as file:
            json.dump(self.resources, file, indent=2)
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
                "warning_days":1
            }
            with open("threshold_parameters.json",'w') as file:
                json.dump(factors,file,indent=2)
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

