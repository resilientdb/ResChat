import json
import os
from encryption import *


def add_friend(public_key, nick_name: str):
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
        dic[nick_name] = {"public_key": public_key_to_string(public_key), "current_page": 1}
        with open(file_name, 'w') as file:
            json.dump(dic, file)


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


def get_all_friends():
    file_name = "local_friends_list.json"
    if os.path.exists(file_name) and os.path.getsize(file_name) > 0:
        with open(file_name, 'r') as file:
            dic = json.load(file)
            return list(dic.keys())
    return []



