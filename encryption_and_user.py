import Crypto
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
import binascii
import hashlib
from kv_operation import get_message, send_message


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
        send_message(username, public_key_str)
        return True
    else:
        print("Username already taken")
        return False


def load_user(username: str, password: str) -> list or bool:
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


def public_key_to_string(pub_key):
    return pub_key.exportKey(format='PEM').decode('utf-8')


def string_to_public_key(pub_key_string):
    return RSA.importKey(pub_key_string.encode('utf-8'))


# 使用RSA加密AES密钥
def encrypt_aes_key_with_rsa(aes_key, public_key):
    cipher_rsa = PKCS1_OAEP.new(public_key)
    encrypted_aes_key = cipher_rsa.encrypt(aes_key)
    return binascii.hexlify(encrypted_aes_key).decode('ascii')


# 使用RSA解密AES密钥
def decrypt_aes_key_with_rsa(encrypted_aes_key, private_key):
    encrypted_aes_key = binascii.unhexlify(encrypted_aes_key)
    cipher_rsa = PKCS1_OAEP.new(private_key)
    aes_key = cipher_rsa.decrypt(encrypted_aes_key)
    return aes_key


# 使用AES加密数据
def encrypt_data_with_aes(data):
    aes_key = get_random_bytes(16)
    cipher_aes = AES.new(aes_key, AES.MODE_GCM)
    ciphertext, tag = cipher_aes.encrypt_and_digest(data)
    return aes_key, cipher_aes.nonce, tag, ciphertext


# 使用AES解密数据
def decrypt_data_with_aes(encrypted_data, aes_key, nonce, tag):
    cipher_aes = AES.new(aes_key, AES.MODE_GCM, nonce)
    data = cipher_aes.decrypt_and_verify(encrypted_data, tag)
    return data


# 修改后的加密消息函数
def encrypt_message_for_two_recipients(message: str or bytes, public_key_sender, public_key_receiver):
    if isinstance(message, str):
        message = message.encode('utf-8')

    aes_key, nonce, tag, encrypted_data = encrypt_data_with_aes(message)
    encrypted_aes_key_sender = encrypt_aes_key_with_rsa(aes_key, public_key_sender)
    encrypted_aes_key_receiver = encrypt_aes_key_with_rsa(aes_key, public_key_receiver)

    encrypted_message = binascii.hexlify(nonce + tag + encrypted_data).decode('ascii')
    return encrypted_message, encrypted_aes_key_sender, encrypted_aes_key_receiver


# 修改后的解密消息函数
def decrypt_message(encrypted_message, encrypted_aes_key, private_key):
    encrypted_message = binascii.unhexlify(encrypted_message)
    nonce = encrypted_message[:16]
    tag = encrypted_message[16:32]
    encrypted_data = encrypted_message[32:]

    aes_key = decrypt_aes_key_with_rsa(encrypted_aes_key, private_key)
    decrypted_data = decrypt_data_with_aes(encrypted_data, aes_key, nonce, tag)
    return decrypted_data.decode('utf-8')
