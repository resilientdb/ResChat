import Crypto
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
import binascii
import hashlib
from kv_operation import get_message, send_message


# Internal function

def hash_with_sha256(input_string):
    """Hash a string with SHA256"""
    sha_signature = hashlib.sha256(input_string.encode()).hexdigest()
    return sha_signature


# External function
def create_user(username: str, password: str) -> bool:
    """Create a user, return True if user has been created successfully. Return False if username has already taken"""
    user_info = get_message(username)
    if user_info == "" or user_info == "\n":
        key = RSA.generate(2048)
        private_key = key.exportKey(passphrase=username + password, pkcs=8)
        public_key = key.publickey()
        public_key_str = public_key_to_string(public_key)
        enc_psw = hash_with_sha256(password)
        with open(f"private_key.pem", "wb") as f:
            f.write(private_key)
        send_message(username, public_key_str)
        return True
    else:
        print("Username already taken")
        return False


# External function
def load_user(username: str, password: str) -> list or bool:
    """
    Load user information from ResilientDB. Return [username, password, public key, private key].
    Return False if user not exist or wrong password
    """
    public_key_string = get_message(username)

    if public_key_string == "" or public_key_string == "\n":
        print("User not exist")
        return False
    else:
        try:
            with open("private_key.pem", "rb") as f:
                private_key = RSA.import_key(f.read(), passphrase=username + password)
        except Exception as e:
            print("Error loading private key:", str(e))
            return False
    public_key = string_to_public_key(public_key_string)
    return [username, password, public_key, private_key]


# Internal function
def public_key_to_string(pub_key):
    """Convert an RSA public key type to string"""
    return pub_key.exportKey(format='PEM').decode('utf-8')


# Internal function
def string_to_public_key(pub_key_string):
    """Convert a string to an RSA public key"""
    return RSA.importKey(pub_key_string.encode('utf-8'))


# Internal function
def encrypt_aes_key_with_rsa(aes_key, public_key):
    """User RSA public key to encrypt AES key"""
    cipher_rsa = PKCS1_OAEP.new(public_key)
    encrypted_aes_key = cipher_rsa.encrypt(aes_key)
    return binascii.hexlify(encrypted_aes_key).decode('ascii')


# Internal function
def decrypt_aes_key_with_rsa(encrypted_aes_key, private_key):
    """Use RSA private key to decrypt AES key"""
    encrypted_aes_key = binascii.unhexlify(encrypted_aes_key)
    cipher_rsa = PKCS1_OAEP.new(private_key)
    aes_key = cipher_rsa.decrypt(encrypted_aes_key)
    return aes_key


# Internal function
def encrypt_data_with_aes(data):
    """User AES to encrypt a string"""
    aes_key = get_random_bytes(16)
    cipher_aes = AES.new(aes_key, AES.MODE_GCM)
    ciphertext, tag = cipher_aes.encrypt_and_digest(data)
    return aes_key, cipher_aes.nonce, tag, ciphertext


# Internal function
def decrypt_data_with_aes(encrypted_data, aes_key, nonce, tag):
    """User AES to decrypt a string"""
    cipher_aes = AES.new(aes_key, AES.MODE_GCM, nonce)
    data = cipher_aes.decrypt_and_verify(encrypted_data, tag)
    return data


# External function

def encrypt_message_for_two_recipients(message: str or bytes, public_key_sender, public_key_receiver):
    """
    Use two senders' RSA public key to encrypt a message
    Return a list [encrypted message,
                    encrypted AES key by sender's RSA public key,
                    encrypted AES key by receiver's RSA public key]
    """
    if isinstance(message, str):
        message = message.encode('utf-8')

    aes_key, nonce, tag, encrypted_data = encrypt_data_with_aes(message)
    encrypted_aes_key_sender = encrypt_aes_key_with_rsa(aes_key, public_key_sender)
    encrypted_aes_key_receiver = encrypt_aes_key_with_rsa(aes_key, public_key_receiver)

    encrypted_message = binascii.hexlify(nonce + tag + encrypted_data).decode('ascii')
    return encrypted_message, encrypted_aes_key_sender, encrypted_aes_key_receiver


# External function
def decrypt_message(encrypted_message, encrypted_aes_key, private_key):
    """Use encrypted message, encrypted AES key and RSA private key to decrypt a messages"""
    encrypted_message = binascii.unhexlify(encrypted_message)
    nonce = encrypted_message[:16]
    tag = encrypted_message[16:32]
    encrypted_data = encrypted_message[32:]

    aes_key = decrypt_aes_key_with_rsa(encrypted_aes_key, private_key)
    decrypted_data = decrypt_data_with_aes(encrypted_data, aes_key, nonce, tag)
    return decrypted_data.decode('utf-8')
