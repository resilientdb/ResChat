import datetime
import os.path
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


send_message("2940009621 920904204 1", "\n")
send_message("2940009621 920904204 FILE_COUNT", "1")
send_message("2940009621 920904204 PAGE_NUM", "1")
client.login("2940009621", "123456")
client.select_friend_to_chat_with("test")

print("CHECK TEST1")
client.send_file("test_img.jpeg")
client.update_chat_history()
# f = read_file("test_img.jpeg")

print("CHECK TEST2")
client.download_file("test_img2.jpeg", client.current_chat_history[0][0], client.current_chat_history[0][4])
# f1 = get_message("2940009621 920904204 FILE 1")

# print(len(f))
# if f == f_str:
#     print("TRUE")
# else:
#     print("FALSE")
# print(len(f))
# print(len(f_str))
# write_file("test_img2.jpeg", f_str)


