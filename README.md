# intro-prog
Introductory Programming Project Group 1

### Dependencies
- Requires `python` version `3.12.0` or above
- Requires `pandas`

### Running the app
- This is a command line interface app
- Please clone all files and run `main.py` with `python` from the terminal (depending on your installation, this could be `python main.py`, `python3 main.py`, or `py main.py`)

### Navigation Schematic for Menu Options

#### Homepage
- `[1]` Log out
- `[2]` Manage my user account
  - `[1]` CANCEL
  - `[2]` List my details
  - `[3]` Edit my details
- `[3]` Manage users (volunteers/admins)
  - `[1]` CANCEL
  - `[2]` List all users
  - `[3]` Add user
  - `[4]` Edit user
  - `[5]` Delete user
  - `[6]` Activate user
  - `[7]` Deactivate user
- `[4]` Manage humanitarian plans
  - `[1]` CANCEL
  - `[2]` List plans (active/ended/all)
    - `[1]` CANCEL
    - `[2]` List active plans
    - `[3]` List ended plans
    - `[4]` List all plans
  - `[3]` Create new humanitarian plan
  - `[4]` Modify a humanitarian plan
  - `[5]` Immediately end a humanitarian plan
  - `[6]` Reactivate a humanitarian plan
  - `[7]` Delete a humanitarian plan
- `[5]` Manage camps and volunteers (*)
  - `[1]` CANCEL
  - `[2]` List all camps (under any active plan)
  - `[3]` List all camps under a specific active plan
  - `[4]` Add a camp
  - `[5]` Delete a camp
  - `[6]` Edit camp details
  - `[7]` Edit volunteers: add to/remove from a camp
- `[6]` Manage refugee profiles (*)
  - `[1]` CANCEL
  - `[2]` List all refugee profiles under all camps (in active plans)
  - `[3]` List all refugee profiles under a specific camp (in an active plan)
  - `[4]` Add a refugee profile
  - `[5]` Edit a refugee profile
  - `[6]` Delete a refugee profile
- `[7]` Manage resources (*)
  - `[1]` CANCEL
  - `[2]` List all resource profiles under all camps (*)
  - `[3]` List all resource profiles under a specific camp (*)
  - `[4]` Set (overwrite) resource amounts in a specific camp (*)
  - `[5]` Increment resource amounts in a specific camp (*)
  - `[6]` Display camps with insufficient resources/ Change resource warning thresholds(*)
- `[8]` Generate a report (all entities under active/ended plans)
  - `[1]` CANCEL
  - `[2]` All plans
  - `[3]` Specific plan and its nested camps
  - `[4]` All camps
  - `[5]` Specific camp and its nested resources + refugees
  - `[6]` All resources in ended plans

Please note:
- Options annotated with `(*)` are only available for entities under active plans.
- To view entities under ended plans, choose option `[8]` from the homepage.


