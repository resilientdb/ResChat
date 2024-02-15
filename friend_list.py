import Crypto.PublicKey.RSA

from kv_operation import send_message, get_message
import json
import os
from encryption_and_user import *


def search_friend(username: str):
    user_info = get_message(username)
    if user_info == "\n" or user_info == "":
        print("No such user")
        return False
    else:
        return user_info


# Get my friend list from ResilientDB return a dictionary
def get_my_friend_list(username: str) -> dict:
    friend_list_string = get_message(username + " FRIEND")
    if friend_list_string == "\n":
        print("No friend")
        return {}
    else:
        friend_list = json.loads(friend_list_string)
        return friend_list


def set_my_friend_list(username: str, friend_list: dict):
    friend_list_string = json.dumps(friend_list)
    send_message(username + " FRIEND", friend_list_string)


def add_friend(friend_username: str, my_username: str, nickname: str) -> bool:
    friend_list = get_my_friend_list(my_username)
    if nickname in friend_list:
        print(f"you already add {nickname} as friend")
        return False
    else:
        friend_pub_key = search_friend(friend_username)
        friend_list[nickname] = {"public_key": friend_pub_key, "current_page": 1, "friend_username": friend_username}

    sorted_usernames = sorted([my_username, friend_username])
    first_username = sorted_usernames[0]
    second_username = sorted_usernames[1]

    checker = get_my_friend_list(first_username + " " + second_username + " " + "FILE_COUNT")
    if checker == "\n" or checker == "":
        send_message(first_username + " " + second_username + " " + "FILE_COUNT", "0")
    set_my_friend_list(my_username, friend_list)
    return True


def get_all_friends(username: str) -> list:
    friend_list = get_my_friend_list(username)
    if friend_list == {}:
        return []
    else:
        return list(friend_list.keys())


def delete_friend(nickname: str, username: str) -> bool:
    friend_list = get_my_friend_list(username)
    if nickname in friend_list:
        friend_list.pop(nickname)
        set_my_friend_list(username, friend_list)
        return True
    else:
        print(f"{nickname} is not your friend")
        return False


def update_page_num(nickname: str, username: str) -> bool:
    friend_list = get_my_friend_list(username)
    if nickname in friend_list:
        friend_list[nickname]['current_page'] += 1
        set_my_friend_list(username, friend_list)
        return True
    else:
        return False


def update_file_num(nickname: str, username: str) -> bool:
    friend_list = get_my_friend_list(username)
    if nickname in friend_list:
        friend_username = friend_list[nickname]['friend_username']
        sorted_usernames = sorted([username, friend_username])
        first_username = sorted_usernames[0]
        second_username = sorted_usernames[1]
        current_file_count = get_message(first_username + " " + second_username + " " + "FILE_COUNT")
        current_file_count = int(current_file_count)
        send_message(first_username + " " + second_username + " " + "FILE_COUNT", str(current_file_count + 1))
        return True
    else:
        return False
