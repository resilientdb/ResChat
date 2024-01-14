from getpass import getpass
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import binascii
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from kv_operation import get_message, send_message
import hashlib


def hash_with_sha256(input_string):
    sha_signature = hashlib.sha256(input_string.encode()).hexdigest()
    return sha_signature


def create_user(username: str, password: str) -> bool:
    user_info = get_message(username)
    if user_info == "" or user_info == "\n":
        key = RSA.generate(2048)
        private_key = key.exportKey(passphrase=username + password, pkcs=8)
        public_key = key.publickey()
        public_key_str = public_key_to_string(public_key)
        enc_psw = hash_with_sha256(password)
        with open(f"private_key.pem", "wb") as f:
            f.write(private_key)
        send_message(username, enc_psw + " " + public_key_str)
        return True
    else:
        return False


def load_user(username: str, password: str) -> list or bool:
    user_info = get_message(username)
    if user_info == "" or user_info == "\n":
        print("User not exist")
        return False
    else:
        split_user_info = user_info.split(" ")
        if len(split_user_info) != 2:
            print("Storage format is wrong")
            return False
        else:
            enc_psw = split_user_info[0]
            public_key_string = split_user_info[1]

            if enc_psw != hash_with_sha256(password):
                print("Wrong password or username")
                return False
            else:
                try:
                    with open("private_key.pem", "rb") as f:
                        private_key = RSA.import_key(f.read(), passphrase=password)
                except Exception as e:
                    print("Error loading private key:", str(e))
                    return False
            public_key = string_to_public_key(public_key_string)
            return [username, password, public_key, private_key]


def public_key_to_string(pub_key):
    return pub_key.exportKey(format='PEM').decode('utf-8')


def string_to_public_key(pub_key_string):
    return RSA.importKey(pub_key_string.encode('utf-8'))
