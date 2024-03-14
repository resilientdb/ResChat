import _io
import datetime
import os.path
import random
import string
import sys
from page import *
import kv_operation as kv
from friend_list import *
from encryption_and_user import *
import client
from file_operation import *
import time


# pybind_kv.set("test", "123", "/home/ubuntu/Desktop/incubator-resilientdb/scripts/deploy/config_out/client.config")
# print(pybind_kv.get("a", "/home/ubuntu/Desktop/incubator-resilientdb/scripts/deploy/config_out/client.config"))
# send_message("2940009621", "\n")
# create_user("2940009621", "123456")
# user_info = load_user("2940009621", "123456")
# add_friend("920904204", usr_name, "test")
# sorted_usernames = sorted([usr_name, "920904204"])
# first_username = sorted_usernames[0]
# second_username = sorted_usernames[1]
# update_page_num("test", usr_name)
# print(get_message(first_username + " " + second_username + " " + "PAGE_NUM"))
def reset_and_clear_all():
    for i in range(10):
        send_message(f"2940009621 920904204 {i + 1}", "\n")

    send_message("2940009621 920904204 PAGE_NUM", "1")
    send_message("2940009621 920904204 FILE 1", "\n")
    for j in range(5):
        for k in range(5):
            # print(f"Resetting 2940009621 920904204 FILE {j} {k}")
            send_message(f"2940009621 920904204 FILE {j} {k}", "\n")
    send_message("2940009621 920904204 FILE_COUNT", "1")


# reset_and_clear_all()
# client.login("2940009621", "123456")
# send_message("920904204", client.my_public_key_string)
# client.encapsulated_add_friend("920904204", "test")
# client.logout()
# print(get_message("test"))
# client.select_friend_to_chat_with("test")
# for i in range(40):
#     print(f"Sending Message {i+1}")
#     client.send_text_message(f"Message {i + 1}")
#
# client.initial_chat_history_loading()
# for i in range(len(client.current_chat_history)):
#     print(client.current_chat_history[i])
with open("test_img.jpeg", "rb") as f:
    print(type(f))

def test(f: _io.BufferedReader)

