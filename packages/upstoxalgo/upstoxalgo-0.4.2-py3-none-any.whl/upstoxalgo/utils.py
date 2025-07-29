import json
import copy
from pprint import pprint

def load_creds_from_file(filepath="creds.json"):
    with open(filepath, "r") as f:
        return json.load(f)
    
def print_safe_creds(creds):
    safe_creds = copy.deepcopy(creds)
    
    # Mask sensitive info
    sensitive_keys = ["client_pass", "client_pin", "api_secret", "api_key"]
    for key in sensitive_keys:
        if key in safe_creds["auth"]:
            safe_creds["auth"][key] = "****"
    
    # Optionally trim access token
    if "access_token" in safe_creds["auth"]:
        token = safe_creds["auth"]["access_token"]
        safe_creds["auth"]["access_token"] = token[:10] + "..." if token else ""

    pprint(safe_creds)

def save_creds_to_file(creds, filepath="creds.json"):
    with open(filepath, "w") as f:
        json.dump(creds, f, indent=4)