import datetime
import sys
from page import *
import kv_operation as kv
from friend_list import *
from encryption_and_user import *
import client
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
client.login("2940009621", "123456")
print(type(client.my_public_key_string))
#
# client.logout()
# pg = Page()
# pg.add_message(pub_key="123",
#                msg_type="TEXT",
#                t_stamp="2024-02-19 19:36:57.0",
#                msg_type_ext="NONE",
#                message="Hi",
#                encrypted_aes_key_sender="123",
#                encrypted_aes_key_receiver="456")
# pg.add_message(pub_key="123",
#                msg_type="TEXT",
#                t_stamp="2024-02-19 19:36:57.2",
#                msg_type_ext="NONE",
#                message="Hi",
#                encrypted_aes_key_sender="123",
#                encrypted_aes_key_receiver="456")
# pg.add_message(pub_key="123",
#                msg_type="TEXT",
#                t_stamp="2024-02-19 19:36:57.1",
#                msg_type_ext="NONE",
#                message="Hi",
#                encrypted_aes_key_sender="123",
#                encrypted_aes_key_receiver="456")
# pg.sort_by_time()
# a = pg.all_messages()
# print(a[0][0])




