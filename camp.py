class camp:
#camp_identification here refer to camp_1 ,camp_2,camp_3 (don't overlap even in different humanitarian plan)
#  location refer to the location of the camp

#capacity is flexiable and size is varied from hundreds to thousands ,here we assume the capacity size is 30
# humanitarian_plan_in refer to the humanitarian plan that the camp is in
    def __init__(self, camp_identification, location, capacity,humanitarian_plan_in):
        self.camp_identification = camp_identification
        self.location = location
        self.capacity = capacity
        self.humanitarian_plan_in = humanitarian_plan_in
        #initialize lists that will hold volunteers and refugees associated with each camp
        self.volunteers = []
        self.refugees = []
        self.resources = {}


 #Edit  camp information(identification of their camp (updating the camp's name, location)and the capacity (Size of Capacity) for new refugees.)
    def edit_camp_information(self, new_camp_identification, new_location, new_capacity,humanitarian_plan_in):
        self.camp_identification = new_camp_identification
        self.location = new_location
        self.capacity = new_capacity
        self.humanitarian_plan_in = humanitarian_plan_in
        return "Camp information updated successfully"
    
# Get camp information
    def get_camp_information(self):
        camp_information ={
            "camp_identification": self.camp_identification,
            "location": self.location,
            "capacity": self.capacity,
            "humanitarian_plan_in": self.humanitarian_plan_in,
        }
        return camp_information

    #manage volunteers in the camp
    #add a volunteer to the camp
    def add_volunteer(self, volunteer):
        if len(self.volunteers) < self.capacity:
            self.volunteers.append(volunteer)
            return "Volunteer added successfully"
        else:
            return "Camp is full"

    #remove a volunteer from the camp
    def remove_volunteer(self, volunteer):
        if volunteer in self.volunteers:
            self.volunteers.remove(volunteer)
            return "Volunteer removed successfully"
        else:
            return "Volunteer not found"
        

        #list volunteers in the camp
    def list_volunteers(self):
        return self.volunteers


    
# manage refugees in the camp
    #add a refugee to the camp
    #here parameter refugee refer to the refugee object
    def add_refugee(self,refugee):
        if len(self.refugees)<self.capacity:
            return self.refugees.append(refugee)
        else:
            return "Camp is full"


    #remove a refugee from the camp
    #here parameter refugee refer to the refugee object
    def remove_refugee(self,refugee):
        if refugee in self.refugees:
            return self.refugees.remove(refugee)
        else:
            return "Can't removed as this Refugee not in the camp"

    
    #list refugees 
    def list_refugees(self):
        return self.refugees
    
    
    
    #manage resources in the camp

    #add a resource to the camp
    def add_resource(self, resource, quantity):
        if resource in self.resources:
            self.resources[resource] += quantity
        else:
            self.resources[resource] = quantity
        return "Resource added successfully"

    #remove a resource from the camp
    def remove_resource(self, resource, quantity):
        if resource in self.resources:
            if self.resources[resource] >= quantity:
                self.resources[resource] -= quantity
                return "Resource removed successfully"
            else:
                return "Not enough resource to remove"
        else:
            return "Resource not found"


    #list all resources in the camp
    def list_resources(self):
        return self.resources
    
    # Creating an instance of the Camp class
camp1 = camp(camp_identification="Camp_1",
             location="Location1",
             capacity=30,
             humanitarian_plan_in="Plan_A")




