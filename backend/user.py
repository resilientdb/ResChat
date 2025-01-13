"""
This file contains all user operations such like create user, load user etc.
"""
import json
from ipfs import *
from RSDB_kv_service import get_kv, set_kv
from crypto_service import *
from helper import write_log
def create_user(username: str, password: str, avatar_location: str) -> {}:
    """
    This function create a user
    : return When success a dict {"result": True, "message": [RSA public key, RSA private key]},
            both of those key's type should be RSA key type (not string or byte)
    : return When fail a dict {"result": False, "message": Corresponding error message}
    """
    write_log("Creating User")
    try:
        # Check username format
        if len(username) != 10:
            raise Exception("The length of username must be 10")

        # Check password format
        if len(password) < 8:
            raise Exception("The length of password mast be greater or equal to 8")

        # Check if there are keys in keys folder
        if os.path.exists("keys/private_key.pem") or os.path.exists("keys/public_key.pem"):
            raise Exception("There are already RSA key pair under key/ folder, please login")

        # Check if avatar file exists
        if not os.path.exists(avatar_location):
            raise Exception(f"{avatar_location} doesn't exist")

        # Check if username is already in use
        username_check = get_kv(username)
        if username_check != "\n" and username_check != "" and username_check != " ":
            raise Exception("Username already taken, please try another one")

        # Check if avatar is jpeg or jpg file
        if (not os.path.basename(avatar_location).endswith(".jpg")) and (not os.path.basename(avatar_location).endswith(".jpeg")):
            raise Exception("Avatar must with extension .jpg or .jpeg")

        # Create RSA key pair
        public_key, private_key = generate_rsa_keys(password)
        write_keys_in_disk(public_key, private_key)
        private_key = load_rsa_private_key(private_key, password)
        public_key_string = public_key_to_string(public_key)

        # Upload avatar into IPFS cluster
        avatar_cid = add_file_to_cluster(avatar_location)
        if avatar_cid is None:
            raise Exception("Fail to upload")

        # Create corresponding key pair in RSDB
        set_kv(username, public_key_string)
        set_kv(username + " FRIEND", json.dumps({}))
        set_kv(username + " AVATAR", avatar_cid)

        return {"result": True, "message": [public_key, private_key]}
    except Exception as e:
        write_log(e)
        return {"result": False, "message": str(e)}


def load_user(username: str, password: str) -> {}:
    """
    This function should be called when user wants to log in
    : return When success {"result": True, "message": [RSA public key, RSA private key]},
        both of those key's type should be RSA key type (not string or byte)
    : return When fail a dict {"result": False, "message": Corresponding error message}
    """

    # TODO: 1. Load RSA private and public key from disk (/keys/*)
    # TODO: 2. Check if loaded RSA public key matches RSA public key on RSDB
    # TODO: 3. Check if password can unlock RSA private key
    # TODO: 4. Check if RSA public key and private key matches (call verify_key_pair() in crypto_service.py)



def update_avatar():
    # TODO
    return

