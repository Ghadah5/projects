from totp import generate_totp
import base64
import re

def validate_secret(secret):
    if not re.fullmatch(r'[A-Z2-7]+', secret):
        return False, "Secret contains invalid characters. Use only A-Z and 2-7."
    if len(secret) != 32:
        return False, f"Secret must be exactly 32 characters. You entered {len(secret)}."
    return True, None

def generate_code(secret):
    secret = secret.strip().upper()

    valid, error = validate_secret(secret)
    if not valid:
        print(f"Invalid secret: {error}")
        print("Please copy the exact secret shown during registration.")
        return

    try:
        code = generate_totp(secret)
        print("Your TOTP code:", code)
    except Exception:
        print("Invalid secret. Please copy the exact secret shown during registration.")