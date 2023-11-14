import json
import os
from encryption import *
import Crypto.PublicKey.RSA as RSA


# Add one friend with his public key and a nickname that defined by user
def add_friend(public_key: str, nick_name: str):
    file_name = "local_friends_list.json"
    dic = {}
    try:
        if os.path.exists(file_name) and os.path.getsize(file_name) > 0:
            with open(file_name, 'r') as file:
                dic = json.load(file)
    except json.JSONDecodeError:
        print("JSON file is corrupted or empty. It will be overwritten with valid data.")

    if nick_name in dic:
        print(f"{nick_name} is already your friend")
        return None
    else:
        dic[nick_name] = {"public_key": public_key, "current_page": 1}
        with open(file_name, 'w') as file:
            json.dump(dic, file)


# Use nickname to return this user's public key and current page
def get_friend(nick_name: str) -> dict or bool:
    file_name = "local_friends_list.json"
    if os.path.exists(file_name) and os.path.getsize(file_name) > 0:
        with open(file_name, 'r') as file:
            dic = json.load(file)
            if nick_name in dic:
                friend_info = dic[nick_name]
                friend_info["public_key"] = string_to_public_key(friend_info["public_key"])
                return friend_info
    return False


# Increase certain user's page number by 1
def update_page_num(nick_name: str):
    file_name = "local_friends_list.json"
    dic = {}
    if os.path.exists(file_name) and os.path.getsize(file_name) > 0:
        with open(file_name, 'r') as file:
            dic = json.load(file)
    if nick_name in dic:
        dic[nick_name]["current_page"] += 1
        with open(file_name, 'w') as file:
            json.dump(dic, file)
        return True
    else:
        return False


# Return all nicknames in the database
def get_all_friends():
    file_name = "local_friends_list.json"
    if os.path.exists(file_name) and os.path.getsize(file_name) > 0:
        with open(file_name, 'r') as file:
            dic = json.load(file)
            return list(dic.keys())
    return []



