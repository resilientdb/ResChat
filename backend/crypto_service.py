import sys
import Crypto
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
import binascii
import hashlib
sys.path.append("bazel/bazel-out/k8-fastbuild/bin/aes_encryption/")
from pybind_aes import aes_file_encrypt, aes_file_decrypt, aes_key_generate, aes_text_encrypt, aes_text_decrypt




def generate_aes_key() -> str:
    return aes_key_generate()

# Internal function
def public_key_to_string(pub_key):
    """Convert an RSA public key type to string"""
    return pub_key.exportKey(format='PEM').decode('utf-8')


# Internal function
def string_to_public_key(pub_key_string):
    """Convert a string to an RSA public key"""
    return RSA.importKey(pub_key_string.encode('utf-8'))