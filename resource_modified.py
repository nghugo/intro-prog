import json


class CampResources:
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
    
    def resource_threshold(self, resource):
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
        thresholds = {
            "food_packets": 3,
            "medical_packets": 1,
            "water_packets": 2,
            "shelter_packets": 1,
            "clothing_packets": 1,
            "baby_packets": 0,
            "sanitation_packets": 2
        }
        return thresholds[resource]

#possible need another function to calculate the concrete amount of resources threshold  based on population
        def calculate_threshold(resource):
            #here only example code ,which really need fix
            #Retrieve the counts of families and members for all camps.
            refugee_count_dict = get_num_families_and_members_by_camp()

            # Get the number of members in campA from the retrieved data.
            num_refugees_camp1 = refugee_count_dict["camp1"]["num_of_members"]

            # Calculate the amount of resource_X needed for campA based on a threshold.
            # Suppose we have defined that each person needs 2 units of resource_X.
            num_resource_X_needed_for_campA = num_refugees_campA * 2  # Threshold is 2 units of resource_X per person.

            # Calculate the amount of resource_Y needed for campA based on a different threshold.
            # Suppose we have defined that each person needs 1 unit of resource_Y.
            num_resource_Y_needed_for_campA = num_refugees_campA  # Threshold is 1 unit of resource_Y per person.
