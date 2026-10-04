# Handles encryption key management for the whole system.
# The key generated here is used by server.py to encrypt/decrypt

import os
from cryptography.fernet import Fernet

KEY_FILE = "secret.key"

def load_or_create_key():
    """Load the encryption key from file, or generate a new one if it doesn't exist."""
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as f:
            return f.read()
    else:
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)
        print(f"New encryption key generated and saved to '{KEY_FILE}'.")
        print(f"Keep this file safe and do NOT share it or upload it anywhere.\n")
        return key