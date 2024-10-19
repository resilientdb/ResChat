import binascii
import sys
import unittest
from tempfile import NamedTemporaryFile
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import os
import psutil
sys.path.append("bazel/bazel-bin/aes_encryption/")
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


def encrypt_text_with_aes(plain_text: str) -> [str, str]:
    """
    Use AES to encrypt plain text
    return randomly generated AES key
    """
    key = generate_aes_key()
    return key, aes_text_encrypt(plain_text, key)


def decrypt_text_with_aes(cipher_text: str, key: str):
    """
    Use AES to decrypt cipher text
    return decrypted text
    """
    return aes_text_decrypt(cipher_text, key)


def encrypt_file_with_aes(file_path: str) -> str:
    """
    Use AES to encrypt file
    If successful, return the AES key
    If the file does not exist, return 1
    If there is not enough RAM, return 2
    If encryption fails, return 3
    """
    memory_info = psutil.virtual_memory()
    free_memory = memory_info.available  # Get available memory (in bytes)
    file_size = os.path.getsize(file_path)
    if not os.path.exists(file_path):
        return "1"
    if free_memory <= file_size:
        return "2"
    else:
        key = generate_aes_key()
        if aes_file_encrypt(file_path, key):
            return key
        else:
            return "3"


def decrypt_file_with_aes(encrypted_file_path: str, save_path: str, key: str) -> str:
    """
    Use AES to decrypt file
    If successful, return 0
    If the encrypted file does not exist, return 1
    If decryption fails, return 2
    """
    if not os.path.exists(encrypted_file_path):
        return "1"
    if aes_file_decrypt(encrypted_file_path, save_path, key):
        return "0"
    else:
        return "2"


# Internal function
def encrypt_aes_key_with_rsa(aes_key: str or bytes, public_key):
    """
    Use an RSA public key to encrypt the AES key
    Returns the encrypted AES key
    """
    if type(aes_key) == str:
        aes_key = aes_key.encode('utf-8')
    cipher_rsa = PKCS1_OAEP.new(public_key)
    encrypted_aes_key = cipher_rsa.encrypt(aes_key)
    return binascii.hexlify(encrypted_aes_key).decode('ascii')


# Internal function
def decrypt_aes_key_with_rsa(encrypted_aes_key, private_key) -> str:
    """
    Use an RSA private key to decrypt the AES key
    Returns the decrypted AES key
    """
    encrypted_aes_key = binascii.unhexlify(encrypted_aes_key)
    cipher_rsa = PKCS1_OAEP.new(private_key)
    aes_key = cipher_rsa.decrypt(encrypted_aes_key)
    return aes_key.decode('utf-8')  # Ensure the returned value is decoded


def encrypt_message_for_two_recipients(plain_text: str or bytes, public_key_sender , public_key_receiver):
    """
    Use both the sender's and receiver's RSA public keys to encrypt a message
    Returns a list [encrypted message,
                encrypted AES key by sender's RSA public key,
                encrypted AES key by receiver's RSA public key]
    """
    if isinstance(plain_text, str):
        plain_text = plain_text.encode('utf-8')

    aes_key, encrypted_message = encrypt_text_with_aes(plain_text)
    encrypted_aes_key_sender = encrypt_aes_key_with_rsa(aes_key, public_key_sender)
    encrypted_aes_key_receiver = encrypt_aes_key_with_rsa(aes_key, public_key_receiver)

    return encrypted_message, encrypted_aes_key_sender, encrypted_aes_key_receiver


def decrypt_message(encrypted_message: str, encrypted_aes_key, private_key):
    """
    Use an RSA private key to decrypt the AES key and then use that AES key to decrypt the message
    Returns the decrypted message
    """
    aes_key = decrypt_aes_key_with_rsa(encrypted_aes_key, private_key)
    decrypted_data = decrypt_text_with_aes(encrypted_message, aes_key)
    return decrypted_data  # Remove .decode('utf-8')


class TestEncryptionFunctions(unittest.TestCase):

    def test_aes_text_encryption_decryption(self):
        plain_text = "This is a test message!"

        # Use AES to encrypt the plain text
        aes_key = generate_aes_key()
        encrypted_text = aes_text_encrypt(plain_text, aes_key)

        # Use AES to decrypt the plain text
        decrypted_text = aes_text_decrypt(encrypted_text, aes_key)

        # Verify the decryption result
        self.assertEqual(decrypted_text, plain_text)

    def test_aes_file_encryption_decryption(self):
        # Create a temporary file
        with NamedTemporaryFile(delete=False) as temp_file:
            # Encode the string into UTF-8 bytes
            temp_file.write("This is a test file.".encode('utf-8'))
            temp_file_path = temp_file.name

        # Use AES to encrypt the file
        aes_key = encrypt_file_with_aes(temp_file_path)

        # Verify AES key generation was successful
        self.assertNotEqual(aes_key, "1")
        self.assertNotEqual(aes_key, "2")
        self.assertNotEqual(aes_key, "3")

        # Search for the encrypted file in the temp folder
        # temp_folder = os.path.join(os.path.dirname(temp_file_path), "temp")
        temp_folder = "temp/"
        encrypted_file_path = None

        # Iterate through the temp folder to find the encrypted file
        for file_name in os.listdir(temp_folder):
            if file_name.endswith(".enc"):
                encrypted_file_path = os.path.join(temp_folder, file_name)
                break

        # Ensure the encrypted file is found
        self.assertIsNotNone(encrypted_file_path, "Encrypted file not found")

        # Create a save path for the decrypted file
        decrypted_file_path = temp_file_path + ".dec"

        # Use AES to decrypt the file
        decrypt_status = decrypt_file_with_aes(encrypted_file_path, decrypted_file_path, aes_key)

        # Verify the decryption status
        self.assertEqual(decrypt_status, "0")

        # Compare the original file with the decrypted file
        with open(temp_file_path, 'rb') as original, open(decrypted_file_path, 'rb') as decrypted:
            self.assertEqual(original.read(), decrypted.read())

        # Clean up temporary files
        os.remove(temp_file_path)
        os.remove(decrypted_file_path)
        os.remove("temp/" + os.path.basename(temp_file_path) + ".enc")


if __name__ == '__main__':
    unittest.main()
