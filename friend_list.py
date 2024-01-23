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
        split_user_info = user_info.split(" ", 1)
        return split_user_info[1]
