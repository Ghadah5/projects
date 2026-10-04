import hmac
import hashlib
import time
import struct
import base64

def generate_totp(secret, interval=30, digits=6):

    key = base64.b32decode(secret)
    counter = int(time.time() / interval)
    counter_bytes = struct.pack(">Q", counter)
    hmac_hash = hmac.new(key, counter_bytes, hashlib.sha1).digest()
    offset = hmac_hash[-1] & 0x0F
    code = struct.unpack(">I", hmac_hash[offset:offset+4])[0] & 0x7fffffff
    otp = code % (10 ** digits)
    return str(otp).zfill(digits)


def verify_totp(secret, code, interval=30, digits=6, window=1):

    key = base64.b32decode(secret)
    current_counter = int(time.time() / interval)

    for delta in range(-window, window + 1):
        counter = current_counter + delta
        counter_bytes = struct.pack(">Q", counter)
        hmac_hash = hmac.new(key, counter_bytes, hashlib.sha1).digest()
        offset = hmac_hash[-1] & 0x0F
        candidate = struct.unpack(">I", hmac_hash[offset:offset+4])[0] & 0x7fffffff
        otp = str(candidate % (10 ** digits)).zfill(digits)
        if otp == code:
            return True

    return False