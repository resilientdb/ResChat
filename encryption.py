
from getpass import getpass
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import binascii


def create_keys(username, password):
    key = RSA.generate(2048)

    private_key = key.exportKey(passphrase=password, pkcs=8)
    with open(f"private_key.pem", "wb") as f:
        f.write(private_key)

    public_key = key.publickey().exportKey()
    with open(f"public_key.pem", "wb") as f:
        f.write(public_key)

    print(f"Keys for {username} have been generated and saved.")
    return private_key, public_key


def encrypt_message(message, public_key):
    cipher = PKCS1_OAEP.new(public_key)
    encrypted_message = cipher.encrypt(message)
    return binascii.hexlify(encrypted_message).decode('ascii')


def decrypt_message(encrypted_message, private_key):
    encrypted_message = binascii.unhexlify(encrypted_message)
    cipher = PKCS1_OAEP.new(private_key)
    decrypted_message = cipher.decrypt(encrypted_message)
    return decrypted_message


def load_public_key():
    try:
        with open("public_key.pem", "rb") as f:
            public_key = RSA.import_key(f.read())
        return public_key
    except Exception as e:
        print("Error loading public key:", str(e))
        return None


def load_private_key(password=None):
    try:
        with open("private_key.pem", "rb") as f:
            private_key = RSA.import_key(f.read(), passphrase=password)
        return private_key
    except Exception as e:
        print("Error loading private key:", str(e))
        return None


def public_key_to_string(pub_key):
    # 将公钥转换为字符串
    return pub_key.exportKey(format='PEM').decode('utf-8')


def string_to_public_key(pub_key_string):
    # 将字符串转换回公钥
    return RSA.importKey(pub_key_string.encode('utf-8'))