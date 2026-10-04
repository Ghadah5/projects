import hmac
import base64
import os
import json
import hashlib
import time
from cryptography.fernet import Fernet
from totp import generate_totp, verify_totp
from config import load_or_create_key

used_codes = set()

password_attempts = {}
totp_attempts = {}
MAX_ATTEMPTS = 3

ENCRYPTION_KEY = load_or_create_key()
fernet = Fernet(ENCRYPTION_KEY)


def _hash_password(password):
    """Hash a password with a random salt. Returns 'salt$hash' string."""
    salt = os.urandom(16).hex()
    hashed = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 260000).hex()
    return f"{salt}${hashed}"

def _verify_password(password, stored):
    """Verify a password against a stored 'salt$hash' string."""
    salt, hashed = stored.split("$", 1)
    candidate = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 260000).hex()
    return hmac.compare_digest(candidate, hashed)

def _hash(value):
    """Used only for non-secret lookups like username keys."""
    return hashlib.sha256(value.encode()).hexdigest()


def register_user(username, password):
    secret = base64.b32encode(os.urandom(20)).decode()

    try:
        with open("users.json", "r") as f:
            users = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        users = {}

    hashed_username = _hash(username)

    if hashed_username in users:
        print("Username already exists. Registration FAILED")
        return

    hashed_password = _hash_password(password)
    encrypted_secret = fernet.encrypt(secret.encode()).decode()

    users[hashed_username] = {
        "password": hashed_password,
        "secret": encrypted_secret
    }

    with open("users.json", "w") as f:
        json.dump(users, f)

    print("User registered")
    print("Secret:", secret)


def verify(username, password, code):

    try:
        with open("users.json", "r") as f:
            users = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("No users registered yet")
        return

    hashed_username = _hash(username)
    user_data = users.get(hashed_username)

    if not user_data:
        print("User not found")
        return

    # --- Password brute-force check ---
    pw_info = password_attempts.get(hashed_username, {"count": 0, "locked": False})
    if pw_info["locked"]:
        print(f"Account locked after {MAX_ATTEMPTS} failed password attempts. Authentication FAILED")
        return

    # --- Password check ---
    if not _verify_password(password, user_data["password"]):
        pw_info["count"] += 1
        if pw_info["count"] >= MAX_ATTEMPTS:
            pw_info["locked"] = True
            print(f"Incorrect password. Account is now LOCKED after {MAX_ATTEMPTS} failed attempts.")
        else:
            remaining = MAX_ATTEMPTS - pw_info["count"]
            print(f"Incorrect password. {remaining} attempt(s) remaining.")
        password_attempts[hashed_username] = pw_info
        return

    # Password correct — reset its own counter only.
    password_attempts[hashed_username] = {"count": 0, "locked": False}

    # --- TOTP brute-force check  ---
    totp_info = totp_attempts.get(hashed_username, {"count": 0, "locked": False})
    if totp_info["locked"]:
        print(f"Account locked after {MAX_ATTEMPTS} failed TOTP attempts. Authentication FAILED")
        return

    # --- TOTP check ---
    secret = fernet.decrypt(user_data["secret"].encode()).decode()

    WINDOW = 1
    current_counter = int(time.time() / 30)
    window_keys = {
        f"{hashed_username}:{current_counter + delta}:{code}"
        for delta in range(-WINDOW, WINDOW + 1)
    }
    already_used = bool(window_keys & used_codes)

    if verify_totp(secret, code):
        if already_used:
            print("Code already used. Authentication FAILED")
        else:
            used_codes.update(window_keys)
            password_attempts[hashed_username] = {"count": 0, "locked": False}
            totp_attempts[hashed_username]     = {"count": 0, "locked": False}
            print("Authentication SUCCESS")
    else:
        totp_info["count"] += 1
        if totp_info["count"] >= MAX_ATTEMPTS:
            totp_info["locked"] = True
            print(f"Invalid TOTP code. Account is now LOCKED after {MAX_ATTEMPTS} failed attempts.")
        else:
            remaining = MAX_ATTEMPTS - totp_info["count"]
            print(f"Invalid TOTP code. {remaining} attempt(s) remaining.")
        totp_attempts[hashed_username] = totp_info