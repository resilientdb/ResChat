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
client.login("2940009621", "123456")
# print(client.my_public_key_string)
# print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:23])

# start_time = time.time()
# image_string = read_file("/home/ubuntu/Desktop/test_large_file_600M.iso")
enc_msg, enc_aes_sender, enc_aes_receiver = encrypt_message_for_two_recipients("123456",
                                                                               client.my_public_key,
                                                                               client.my_public_key,
                                                                               b"1234567890123456")
print(decrypt_aes_key_with_rsa(enc_aes_receiver, client.my_private_key))


# print(((len(enc_msg) / 1024) / 1024) / 1024)
# send_message("test", "\n")
# send_message("test", enc_msg)
# enc_msg_from_chain = get_message("test")
# if enc_msg_from_chain == enc_msg:
#     print("TRUE!!!")
# else:
#     print("FALSE!!!")
# dec_msg = decrypt_message(enc_msg_from_chain, enc_aes_sender, client.my_private_key)
# #
# # write_file("/home/ubuntu/Desktop/test_large_file_600M_2.iso", dec_msg)
# end_time = time.time()
# elapsed_time = end_time - start_time
# print(f"Program took {elapsed_time} seconds to run.")

# file_size_bytes = os.path.getsize("/home/ubuntu/Desktop/test_large_file_600M.iso")
# file_size_KB = file_size_bytes / 1024
# file_size_MB = file_size_KB / 1024
# file_size_GB = file_size_MB / 1024
#
# print(file_size_MB)

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

# my_list = [[1, 2], [3, 4]]
# my_list.insert(0, [5, 6])  # 在列表最前面添加元素1
# print(my_list)  # 输出: [1, 2, 3, 4]
