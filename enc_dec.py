from getmac import get_mac_address as gma
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Protocol.KDF import PBKDF2

def PBKDF2_encrypt(mac: str) -> bytes:
    """Use PBKDF2 to encrypt MAC address"""
    return PBKDF2(mac, bytes(16), dkLen=32, count=1000000)

def aes_encrypt(data: str, key: bytes) -> tuple:
    """Encrypts a string using AES encryption."""
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(data.encode(), AES.block_size))
    return cipher.iv.hex(), ct_bytes.hex()  # Convert bytes to hex strings

def aes_decrypt(iv: str, ct: str, key: bytes) -> str:
    """Decrypts an AES encrypted message."""
    cipher = AES.new(key, AES.MODE_CBC, bytes.fromhex(iv))
    pt = unpad(cipher.decrypt(bytes.fromhex(ct)), AES.block_size)
    return pt.decode()
def get_mac():
    return gma()


