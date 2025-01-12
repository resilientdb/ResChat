"""
This file contains all user operations such like create user, load user etc.
"""
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

        # Check if avatar file exists
        if not os.path.exists(avatar_location):
            raise Exception(f"{avatar_location} doesn't exist")

        # Check if username is already in use
        username_check = get_kv(username)
        if username_check != "\n" or username_check != "" or username_check != " ":
            raise Exception("Username already taken, please try another one")

        # Check if avatar is jpeg or jpg file
        if (not os.path.basename(avatar_location).endswith(".jpg")) or (not os.path.basename(avatar_location).endswith(".jpeg")):
            raise Exception("Avatar must with extension .jpg or .jpeg")

        # Create RSA key pair
        public_key, private_key = generate_rsa_keys(password)
        write_keys_in_disk(public_key, private_key)
        private_key = load_rsa_private_key(private_key, password)

        # TODO: 6. Create corresponding key value pair in RSDB
            # TODO: 6.1 create {USERNAME: PUBLIC KEY} key value pair
            # TODO: 6.2 crete {USERNAME + " FRIEND": {}} key value pair
            # TODO: 6.3 create {USERNAME + " AVATAR": AVATAR CID} key value pair

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

create_user("1", "1", "aaa")