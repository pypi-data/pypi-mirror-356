import json

def load_creds_from_file(filepath="creds.json"):
    with open(filepath, "r") as f:
        return json.load(f)