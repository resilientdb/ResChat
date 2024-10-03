from kv_operation import get_message, send_message
import hashlib
from crypto_service import public_key_to_string, string_to_public_key
from Crypto.PublicKey import RSA



def hash_with_sha256(input_string):
    """Hash a string with SHA256"""
    sha_signature = hashlib.sha256(input_string.encode()).hexdigest()
    return sha_signature



def create_user(username: str, password: str) -> bool:
    """Create a user, return True if user has been created successfully. Return False if username has already taken"""
    user_info = get_message(username)
    if user_info == "" or user_info == "\n":
        key = RSA.generate(2048)
        private_key = key.exportKey(passphrase=username + password, pkcs=8)
        public_key = key.publickey()
        public_key_str = public_key_to_string(public_key)
        enc_psw = hash_with_sha256(password)
        with open(f"keys/private_key.pem", "wb") as f:
            f.write(private_key)
            f.close()
        with open(f"keys/public_key.pem", "wb") as f:
            f.write(public_key_str)
        send_message(username, public_key_str)
        return True
    else:
        print("Username already taken")
        return False