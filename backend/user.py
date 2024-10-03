from kv_operation import get_message, send_message
import hashlib
from crypto_service import public_key_to_string, string_to_public_key
from Crypto.PublicKey import RSA






def create_user(username: str, password: str) -> bool:
    """Create a user, return True if user has been created successfully. Return False if username has already taken"""
    user_info = get_message(username)
    if user_info == "" or user_info == "\n":
        key = RSA.generate(2048)
        private_key = key.exportKey(passphrase=password, pkcs=8)
        public_key = key.publickey()
        public_key_str = public_key_to_string(public_key)
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



def load_user(username: str, password: str) -> list:
    """
    Load user information from ResilientDB. Return [username, password, public key, private key].
    如果返回空array说明错误
    """
    public_key_string = get_message(username)

    if public_key_string == "" or public_key_string == "\n":
        print("User not exist")
        return []
    else:
        try:
            with open("private_key.pem", "rb") as f:
                private_key = RSA.import_key(f.read(), passphrase=password)
        except Exception as e:
            print("Error loading private key:", str(e))
            return []
    public_key = string_to_public_key(public_key_string)
    return [username, password, public_key, private_key]