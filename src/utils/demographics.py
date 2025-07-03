import json

def collect_demographics():
    """
    Collect basic demographic information from the user.
    """
    demographics = {}
    demographics['name'] = input("Enter your name: ")
    demographics['age'] = input("Enter your age: ")
    demographics['gender'] = input("Enter your gender: ")
    return demographics

def save_demographics(demographics, filename):
    """
    Save demographic data to a JSON file.
    """
    with open(filename, 'w') as f:
        json.dump(demographics, f, indent=2) 