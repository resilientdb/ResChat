"""
This file contains all function needed for the fronted
"""
from crypto_service import *
from user import *
from friend_list import *
import Crypto
from Crypto.PublicKey import RSA

"""Global Variables"""
"""
Group 1
Following variables will be only initialize once after user login successfully 
"""
my_username: str
my_public_key: Crypto.PublicKey.RSA.RsaKey
my_private_key: Crypto.PublicKey.RSA.RsaKey
my_friend_list: dict
my_password: str
my_public_key_string: str

"""
Group 2
Following variables will be initialized and reinitialized everytime user choose a friend to talk with
"""
current_chatting_friend_username: str
current_chatting_friend_public_key: Crypto.PublicKey.RSA.RsaKey
current_chatting_page_name: str
current_chatting_page_number: int
current_chat_previous_page_number: int

"""This variable will be initialized and reinitialized everytime user choose a friend to talk with and every two seconds"""
current_chat_history: {}


def login(username: str, password: str) -> {}:
    """
    This function includes the whole process of login, if it runs successfully, it will assign all Group 1 variables
    """
    global my_username, my_public_key, my_friend_list, my_password, my_public_key_string, my_private_key

    # Load RSA key pair from local disk
    rsa_key_load_res = load_user(username, password)
    if rsa_key_load_res["result"] is False:
        return {"result": False, "message": rsa_key_load_res["message"]}

    # Assign global variables
    my_public_key = rsa_key_load_res["message"][0]
    my_private_key = rsa_key_load_res["message"][1]
    my_username = username
    my_password = password
    my_public_key_string = public_key_to_string(my_public_key)
    my_friend_list = load_my_friend_list(my_username)

    # Update avatar list
    my_friend_list = update_avatar_list(my_friend_list)
    update_rsdb_friend_list(my_friend_list, my_username)

    return {"result": True, "message": "Login in success"}


def signup(username: str, password: str) -> {}:
    # TODO
    return {}


def select_friend(target_username: str) -> None:
    # TODO: Assign Group 2 variables
    return

def encapsulated_change_nickname(target_username: str, new_nickname: str) -> None:
    global my_friend_list, my_username
    my_friend_list = change_nickname(target_username, my_friend_list, new_nickname)
    update_rsdb_friend_list(my_friend_list, my_username)


def encapsulated_delete_friend(target_username: str):
    # TODO


def encapsulated_add_friend(target_username: str, nickname: str) -> {}:
    global my_friend_list, my_username
    add_friend_result = add_friend(target_username, my_friend_list, nickname)

    # Check if result is True
    if add_friend_result["result"] is False:
        return add_friend_result

    # Update my friend list
    my_friend_list = add_friend_result["message"]
    update_rsdb_friend_list(my_friend_list, my_username)
    return {"result": True, "message": f"{target_username} has added into your friend list"}


def send_text_message(plain_text: str):
    # TODO
    return


def send_file(file_path: str):
    # TODO
    return


def update_chat_history():
    #TODO
    return


def load_previous_chat_history():
    #TODO
    return


def download_and_decrypt_file(save_path: str, file_cid: str):
    # TODO
    return

