import os
from kv_operation import get_message, send_message
import hashlib
from crypto_service import public_key_to_string, string_to_public_key
from Crypto.PublicKey import RSA
from ipfs import send_file_ipfs, get_file_ipfs
from PIL import Image

def is_image_file(file_path: str) -> bool:
    """Check if the file is an image"""
    try:
        # Try to open the file as an image
        with Image.open(file_path) as img:
            img.verify()  # Verify that it is, indeed, an image
        return True
    except (IOError, SyntaxError):
        return False




def is_file_size_within_limit(file_path: str, limit_in_mb: int) -> bool:
    """Check if the file size is within the specified limit in MB"""
    file_size_in_mb = os.path.getsize(file_path) / (1024 * 1024)  # Convert bytes to MB
    return file_size_in_mb <= limit_in_mb

def create_user(username: str, password: str, profile_pic_path: str) -> dict:
    """Create a user, return True if user has been created successfully. Return False if username has already taken"""

    file_extension = os.path.splitext(profile_pic_path)[1].lower()

    # Check if the file is an image and is in jpg, jpeg, or png format
    if not is_image_file(profile_pic_path) or file_extension not in [".jpg", ".jpeg", ".png"]:
        return {"result": False, "message": f"{profile_pic_path} is not a valid jpg, jpeg, or png image file"}

    # Check if the file size exceeds 20MB
    if not is_file_size_within_limit(profile_pic_path, 20):
        return {"result": False, "message": "File size exceeds 20MB"}

    user_info = get_message(username)
    if user_info == "" or user_info == "\n":
        key = RSA.generate(2048)
        private_key = key.exportKey(passphrase=password, pkcs=8)
        public_key = key.publickey()
        public_key_str = public_key_to_string(public_key)

        with open(f"keys/private_key.pem", "wb") as f:
            f.write(private_key)

        with open(f"keys/public_key.pem", "wb") as f:
            f.write(public_key_str)

        res = send_file_ipfs(profile_pic_path)
        send_message(username, public_key_str)
        send_message(username + " PROFILE_PICTURE", str(res['Hash']) + " " + str(file_extension))
        send_message(username + " REQUEST_RECEIVED", "{}")
        send_message(username + " REQUEST_SENT", "{}")
        send_message(username + " " + "FRIEND_LIST", "{}")
        return {"result": True, "message": "Success"}
    else:
        return {"result": False, "message": "User name already taken"}



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




