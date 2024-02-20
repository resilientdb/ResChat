import Crypto.PublicKey.RSA

from kv_operation import send_message, get_message
import json
import os
from encryption_and_user import *


# Internal function
def search_friend(username: str):
    """Use friend username to get corresponding public key"""
    user_info = get_message(username)
    if user_info == "\n" or user_info == "":
        print("No such user")
        return False
    else:
        return user_info


# External function
def get_my_friend_list(username: str) -> dict:
    """Use my username to get my friend list from ResilientDB return a dictionary"""
    friend_list_string = get_message(username + " FRIEND")
    if friend_list_string == "\n" or friend_list_string == "":
        print("No friend")
        return {}
    else:
        friend_list = json.loads(friend_list_string)
        return friend_list


# External function
def set_my_friend_list(username: str, friend_list: dict):
    """Set my friend list(dictionary) into ResilientDB"""
    friend_list_string = json.dumps(friend_list)
    send_message(username + " FRIEND", friend_list_string)


# External function
def add_friend(friend_username: str, my_username: str, nickname: str, friend_list: dict) -> dict:
    """Add a friend, return True if add successfully, otherwise return False"""
    if nickname in friend_list:
        print(f"you already add {nickname} as friend")
        return False
    else:
        friend_pub_key = search_friend(friend_username)
        friend_list[nickname] = {"public_key": friend_pub_key, "friend_username": friend_username}

    sorted_usernames = sorted([my_username, friend_username])
    first_username = sorted_usernames[0]
    second_username = sorted_usernames[1]

    checker = get_message(first_username + " " + second_username + " " + "FILE_COUNT")
    if checker == "\n" or checker == "":
        send_message(first_username + " " + second_username + " " + "FILE_COUNT", "0")

    checker = get_message(first_username + " " + second_username + " " + "PAGE_NUM")
    if checker == "\n" or checker == "":
        send_message(first_username + " " + second_username + " " + "PAGE_NUM", "0")

    return friend_list


# External function
def get_all_friends(friend_list: dict) -> list:
    """Return all my friends' nickname"""
    if friend_list == {}:
        return []
    else:
        return list(friend_list.keys())


# External function
def delete_friend(nickname: str, friend_list: dict) -> dict:
    """Delete a friend, return a modified friend list dictionary"""
    if nickname in friend_list:
        friend_list.pop(nickname)
        return friend_list
    else:
        print(f"{nickname} is not your friend")
        return friend_list


# External function
def update_page_num(nickname: str, my_username: str, friend_username: str) -> bool:
    """+1 to the current page number"""
    sorted_usernames = sorted([my_username, friend_username])
    first_username = sorted_usernames[0]
    second_username = sorted_usernames[1]
    current_file_count = get_message(first_username + " " + second_username + " " + "PAGE_NUM")
    current_file_count = int(current_file_count)
    send_message(first_username + " " + second_username + " " + "PAGE_NUM", str(current_file_count + 1))
    return True


# External function
def update_file_num(my_username: str, friend_username: str) -> bool:
    """+1 to the current file count"""
    sorted_usernames = sorted([my_username, friend_username])
    first_username = sorted_usernames[0]
    second_username = sorted_usernames[1]
    current_file_count = get_message(first_username + " " + second_username + " " + "FILE_COUNT")
    current_file_count = int(current_file_count)
    send_message(first_username + " " + second_username + " " + "FILE_COUNT", str(current_file_count + 1))
    return True


# External function
def get_current_page_num(my_username: str, friend_username: str) -> int:
    """Return the current page number"""
    sorted_usernames = sorted([my_username, friend_username])
    first_username = sorted_usernames[0]
    second_username = sorted_usernames[1]
    current_page_num = get_message(first_username + " " + second_username + " " + "PAGE_NUM")
    current_page_num = int(current_page_num)
    return current_page_num


# External function
def get_current_file_count(my_username: str, friend_username: str) -> int:
    """Return the current file count"""
    sorted_usernames = sorted([my_username, friend_username])
    first_username = sorted_usernames[0]
    second_username = sorted_usernames[1]
    current_file_count = get_message(first_username + " " + second_username + " " + "FILE_COUNT")
    current_file_count = int(current_file_count)
    return current_file_count
