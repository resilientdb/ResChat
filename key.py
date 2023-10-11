import os
from enc_dec import get_mac, PBKDF2_encrypt

def generate_public_key():
    """Generate public key"""
    with open("key.txt", 'w') as file:
        mac = get_mac()
        key = PBKDF2_encrypt(mac)
        file.write(str(key))
    print(f"You public key has been generated")

def get_public_key():
    """Get public key"""
    if os.path.exists("key.txt"):
        with open("key.txt", 'r') as file:
            content = file.read()
            return content
    else:
        print("No current key exist, please generate the key first")
        exit(1)

def show_public_key():
    """Display public key"""
    if os.path.exists("key.txt"):
        with open("key.txt", 'r') as file:
            content = file.read()
            print(f"You public key: {content}")
    else:
        print("No current key exist, please generate the key first")
        exit(1)

def delete_public_key():
    """Delete public key"""
    if os.path.exists("key.txt"):
        os.remove("key.txt")
        print("Key has been deleted!")
    else:
        print("There is no key exists")

