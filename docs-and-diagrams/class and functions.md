~~1. **Class: `User`**~~
~~- Base class for different types of users.~~
~~- Functions:~~
~~- `login()`: Authenticate user.~~
~~- `logout()`: End user session.~~
~~- `change_password()`: Update user's password.~~

~~2. **Class: `Admin(User)`**~~
~~- Inherits from `User`.~~
~~- Functions:~~
~~- `create_plan()`: Create a new humanitarian plan.~~
~~- `end_event()`: End a humanitarian event.~~
~~- `display_plan()`: Display details of humanitarian plans.~~
~~- `edit_volunteer_accounts()`: Edit volunteer account details.~~
~~- `allocate_resources()`: Allocate resources to different camps.~~

~~3. **Class: `Volunteer(User)`**~~
~~- Inherits from `User`.~~
~~- Functions:~~
~~- `edit_personal_info()`: Edit volunteer's personal information.~~
~~- `edit_camp_info()`: Edit information about the camp they are assigned to.~~
~~- `create_refugee_profile()`: Create profile for each refugee.~~
~~- `view_resources()`: View resources available at the camp.~~

1. **Class: `InterfaceMain`**
   - Provides the user interface for the user to interact with from start to end.
   - Functions:
     - `start()`: Starts the user interface. This runs until the application is closed.
     - `prompt_login()`: Asks the user to log in, and checks against persisted (existing) users using methods from Users class
     - `prompt_options()`: Provides options available to the currently logged in user. Calls either `prompt_admin_options()` or `prompt_volunteer_options()`
     - `prompt_admin_options()`: Admin options
     - `prompt_volunteer_options()`: Volunteer options
     - `prompt_logout()`: Prompts the user to confirm log out
     - `prompt_exit()`: Prompts the user to confirm exit

2. **Class: `Users`**
   - Provides the functionalities to interact with users.json
   - Functions:
     - `load_users()`: Loads users from users.json and returns a dictionary.
     - `add_user()`: Adds user to users.json.
     - `delete_user()`: Deletes user from users.json.
     - `modify_user()`: Modifies a key-value pair in users.json.

4. **Class: `HumanitarianPlan`**
   - Represents a humanitarian plan.
   - Functions:
     - `add_camp()`: Add a camp to the plan.
     - `remove_camp()`: Remove a camp from the plan.
     - `get_plan_details()`: Retrieve details of the plan.

5. **Class: `Camp`**
   - Represents a refugee camp.
   - Functions:
     - `add_refugee()`: Add a refugee to the camp.
     - `remove_refugee()`: Remove a refugee from the camp.
     - `list_volunteers()`: List all volunteers at the camp.
     - `manage_resources()`: Manage resources of the camp.

6. **Class: `Refugee`**
   - Represents an individual refugee.
   - Functions:
     - `update_medical_condition()`: Update the refugee's medical condition.
     - `update_status()`: Update other status details of the refugee.

7. **Class: `ResourceAllocation`**
   - Manages resource allocation to camps.
   - Functions:
     - `allocate_resources()`: Allocate specific resources to a camp.
     - `view_allocation()`: View current resource allocation details.

8. **Utility Classes**
   - **Class: `DataStorage`**
     - Manages data persistence.
     - Functions:
       - `save_data()`: Save data to storage.
       - `load_data()`: Load data from storage.
   - **Class: `DataValidator`**
     - Validates input data for realism and correctness.
     - Functions:
       - `validate_country()`: Validate country names.
       - `validate_date()`: Validate date entries.
       - `validate_name()`: Validate refugee and volunteer names.

