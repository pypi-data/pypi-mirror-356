from .upstox import upstox_login, upstox_auth, upstox_margin, upstox_positions
from .utils import *


def auto_login_flow(filepath="creds.json"):
    creds = load_creds_from_file(filepath)
    creds = upstox_login(creds)
    creds = upstox_auth(creds)
    creds = upstox_margin(creds)
    creds = upstox_positions(creds)

    print("\n✅ Full Login Flow Completed. Credentials Snapshot:")
    print_safe_creds(creds)

    return creds
