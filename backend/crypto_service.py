"""
This file contains all the encryption and decryption functions
"""
import os
from helper import write_log
import Crypto
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.PublicKey import RSA
import binascii
import sys
sys.path.append("bazel/bazel-bin/aes_encryption")
import pybind_aes

def public_key_to_string(public_key: Crypto.PublicKey.RSA.RsaKey) -> str:
    """Convert RSA public key into string"""
    write_log("Writing public key into disk")
    return public_key.exportKey(format='PEM').decode('utf-8')


def string_to_public_key(public_key_string: str) -> Crypto.PublicKey.RSA.RsaKey:
    """Convert RSA public key string into RSA public key"""
    write_log("Converting string into public key")
    return RSA.importKey(public_key_string.encode('utf-8'))


def load_rsa_private_key(private_key: bytes, password: str) -> Crypto.PublicKey.RSA.RsaKey:
    """Convert RSA private key from bytes to Crypto.PublicKey.RSA.RsaKey"""
    try:
        return RSA.import_key(private_key, passphrase=password)
    except Exception as e:
        write_log(str(e))



def generate_rsa_keys(password: str) -> list:
    """
    Generate a random RSA key pair and assign password to RSA private key
    : return [RSA public key(Crypto.PublicKey.RSA.RsaKey), RSA private key(bytes)]
    !!!!! this RSA private key can not be used directly,
        it has to call load_rsa_private_key to change RSA
        private key from bytes to Crypto.PublicKey.RSA.RsaKey!!!!!
    """
    write_log("Generating RSA key pair")
    key = RSA.generate(2048)
    private_key = key.exportKey(passphrase=password, pkcs=8)
    public_key = key.public_key()
    return [public_key, private_key]


def write_keys_in_disk(public_key, private_key):
    write_log("Writing RSA public key into disk")
    with open(f"keys/public_key.pem", "wb") as pub_key_f:
        pub_key_f.write(public_key.encode('utf-8'))
        pub_key_f.close()

    write_log("Writing RSA private key into disk")
    with open("keys/private_key.pem", "wb") as pri_key_f:
        pri_key_f.write(private_key)
        pri_key_f.close()
    return


def encrypt_aes_key_with_rsa(aes_key: str, public_key):
    """User RSA public key to encrypt AES key"""
    write_log("Encrypting AES key")
    cipher_rsa = PKCS1_OAEP.new(public_key)
    encrypted_aes_key = cipher_rsa.encrypt(aes_key.encode('utf-8'))
    return binascii.hexlify(encrypted_aes_key).decode('ascii')


def decrypt_aes_key_with_rsa(encrypted_aes_key: str, rsa_private_key) -> str:
    """Use RSA private key to decrypt AES key"""
    write_log("Decrypting AES key")
    encrypted_aes_key_bytes = binascii.unhexlify(encrypted_aes_key)
    cipher_rsa = PKCS1_OAEP.new(rsa_private_key)
    aes_key = cipher_rsa.decrypt(encrypted_aes_key_bytes)
    return aes_key.decode('utf-8')


def encrypt_text_with_aes(plain_text: str, aes_key: str) -> str:
    """Use AES to encrypt a string"""
    write_log("Encrypting text")
    cipher_text= pybind_aes.aes_encrypt_text(plain_text, aes_key)
    return cipher_text


def decrypt_text_with_aes(cipher_text: str, aes_key: str) -> str:
    """Use AES to decrypt a string"""
    write_log("Decrypting text")
    plain_text = pybind_aes.aes_decrypt_text(cipher_text, aes_key)
    return plain_text


def generate_random_aes_key():
    """Random generate one AES key"""
    write_log("Generating AES key")
    return pybind_aes.generate_random_key()


def load_public_key_from_disk() -> Crypto.PublicKey.RSA.RsaKey:
    """
    Load RSA public key from disk(/keys/public_key.pem)
    : return RSA key type object (Not a string or bytes)
    """
    # TODO: Finish this


def load_private_key_from_disk(password: str) -> Crypto.PublicKey.RSA.RsaKey:
    """
    Load RSA private from disk(/keys/private_key.pem)
    : return RSA key type object (Not a string or bytes)
    """
    # TODO: Finish this


def verify_key_pair(public_key: Crypto.PublicKey.RSA.RsaKey, private_key: Crypto.PublicKey.RSA.RsaKey) -> bool:
    """Verify if the RSA key pair matches"""
    write_log("Verifying RSA key pair")
    try:
        test_message = binascii.hexlify(os.urandom(20)).decode('utf-8')
        cipher_rsa_enc = PKCS1_OAEP.new(public_key)
        encrypted_message = cipher_rsa_enc.encrypt(test_message.encode('utf-8'))
        cipher_rsa_dec = PKCS1_OAEP.new(private_key)
        decrypted_message = cipher_rsa_dec.decrypt(encrypted_message).decode('utf-8')
        write_log("RSA key pair verified")
        return decrypted_message == test_message
    except (ValueError, TypeError):
        write_log("RSA key pair not verified")
        return False


generate_rsa_keys("12345678")