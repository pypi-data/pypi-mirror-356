from .upstox import upstox_login, upstox_auth, upstox_margin, upstox_positions
from .utils import load_creds_from_file  # Adjust import based on where you place it

def auto_login_flow():
    creds = load_creds_from_file()

    creds = upstox_login(creds)
    creds = upstox_auth(creds)
    creds = upstox_margin(creds)
    creds = upstox_positions(creds)
    
    return creds
