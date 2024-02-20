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
# print(type(client.my_public_key_string))
# enc_msg, enc_aes_sender, enc_aes_receiver = encrypt_message_for_two_recipients("123456",
#                                                                                client.my_public_key,
#                                                                                client.my_public_key)
#
# pg = Page()
# pg.add_message("000",
#                "TEXT",
#                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:23],
#                "NONE",
#                enc_msg,
#                enc_aes_sender,
#                "000")
# msg_string = pg.all_messages()
# tmp = client.encapsulated_decrypt_message(msg_string[0])
# print(tmp)
# pg.sort_by_time()
# a = pg.all_messages()
# print(a[0][0])

tmp_list = [[1, 2], [3, 4], [5, 6]]  # 示例列表
target_list = [[10, 20], [30, 40]]  # 另一个列表，想要将tmp_list的元素从后往前加入到这个列表中

# 将tmp_list从后往前加入到target_list中
target_list.extend(tmp_list[::-1])

print(target_list)
