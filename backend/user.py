"""
This file contains all user operations such like create user, load user etc.
"""


def create_user(username: str, password: str, avatar_location: str) -> {}:
    """
    This function create a user
    : return When success a dict {"result": True, "message": [RSA public key, RSA private key]},
            both of those key's type should be RSA key type (not string or byte)
    : return When fail a dict {"result": False, "message": Corresponding error message}
    """
    # TODO: 1. Check username length
    # TODO: 2. Check password length and other info
    # TODO: 3. Check this user name is already exist or not
        # TODO: 3.1 return {"result": False, "message": "User name already taken"}
    # TODO: 4. Create RSA public and private key
        # TODO: 4.1 Write these two keys in /keys/public_key.pem and /keys/private_key.pem
    # TODO: 5. Add avatar into IPFS
    # TODO: 6. Create corresponding key value pair in RSDB
        # TODO: 6.1 create {USERNAME: PUBLIC KEY} key value pair
        # TODO: 6.2 crete {USERNAME + " FRIEND": {}} key value pair
        # TODO: 6.3 create {USERNAME + " AVATAR": AVATAR CID} key value pair


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