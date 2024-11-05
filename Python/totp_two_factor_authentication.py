import time
import base64
import hmac
import hashlib
from math import floor


# By default, use a 30 seconds time window
VALIDITY_DURATION = 30
TOKEN_LENGTH = 6
# Allow 2 time steps in the past to be considered valid
VALID_START = -2
# Allow 2 time steps in the future to be considered valid
VALID_END = 2


def generate_counter_value():
    """Generates the counter value for the TOTP algorithm's hash generator."""
    timestamp = time.time()
    timestamp = float(timestamp)
    counter_value = floor(timestamp / VALIDITY_DURATION)
    return counter_value


def generate_hash(K: str, C: int):
    """Generates a TOTP compatible HMAC hash based on the shared secret (K) and the current time window/counter value C."""
    # Secrets are usually provided in base32 format, so we need to decode it
    # (cf. https://stackoverflow.com/a/57325779)
    key_bytes = base64.b32decode(K)

    # We have to specify how many bytes to use to represent the time. 8 means
    # 64 bit which helps avoid the Y2k38 bug. Python will throw an error if the
    # number is too big to be represented.
    counter_bytes = C.to_bytes(8, byteorder="big")

    # Take the secret and the counter and generate a hash.
    hash = hmac.digest(key_bytes, counter_bytes, hashlib.sha1)

    # NOTE: The hash must be big endian. This code here assumes that hmac.digest() always uses big endian.
    return hash


def truncate_dynamically(hash: bytes):
    """Truncates a generated HMAC hash and returns it as an integer"""
    # Extract the four least significant bits from the hash, which is by definition between zero (0000) and 15 (1111)
    offset = hash[-1] & 0x0F

    # Extract four bytes, or 32 bits from the offset
    truncated = hash[offset : offset + 4]

    # Convert them into a number. The biggest number that can be represented in 32 bit is 2,147,483,647.
    code_number = int.from_bytes(truncated, byteorder="big")

    # Return the least significant 31 bits. This here essentially removes bit 32 to avoid ambiguity with signed/unsigned integers, because the most significant bit is usually 0 for a positive, and 1 for a negative number, but there can be issues with that.)
    return code_number & 0x7FFFFFFF


def truncated_hash_to_token(code: int, digits: int = TOKEN_LENGTH):
    """Takes a truncated HMAC code number and returns the modulo of that to return the requested number of digits"""
    # This is basically a rounding up
    code = code % 10**digits

    # NOTE: Sometimes the resulting code is less than the amount of digits. In that case, we must left-pad with zeros.
    code = str(code)
    if len(code) < digits:
        code = code.rjust(digits, "0")
    return code


def generate_totp_tokens (key: str, timestep_start = VALID_START, timestep_end = VALID_END):
    """Generates a list of valid tokens within the valid window provided."""
    tokens: list[str] = []
    counter_value = generate_counter_value()

    for timestep in range(timestep_start, timestep_end + 1):
        hm = generate_hash(key, counter_value + timestep)
        code = truncate_dynamically(hm)
        valid_token = truncated_hash_to_token(code)
        tokens.append(valid_token)
    return tokens

if __name__ == "__main__":
    secret = "CLAH6OEOV52XVYTKHGKBERP42IUZHY4D"
    client_token = input("Enter TOTP code from device (Ctrl+C to abort): ")
    valid_tokens = generate_totp_tokens(secret)
    if client_token in valid_tokens:
        print("Token is valid!")
    else:
        print("Sorry, but the token is not valid.")
