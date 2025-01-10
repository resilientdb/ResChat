"""
This file contains all function needed for the fronted
"""
import crypto_service
import Crypto
from Crypto.PublicKey import RSA

"""Global Variables"""
my_username: str
my_public_key: Crypto.PublicKey.RSA.RsaKey
my_private_key: Crypto.PublicKey.RSA.RsaKey
my_friend_list: dict
my_password: str
my_public_key_string: str

current_chatting_friend_username: str
current_chatting_friend_public_key: Crypto.PublicKey.RSA.RsaKey
current_chatting_page_name: str
current_chatting_page_number: int
current_chat_previous_page_number: int

current_chat_history: {}

