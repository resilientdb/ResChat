import numpy as np
from page import *
from chain_operation import *
import datetime
from file_operations import *
from encryption import *
from db import *

# 创建Page类的实例
my_page = Page()
my_page.add_message("pub_key1", "msg_type1", datetime.datetime(2023, 11, 1, 1, 1, 1, 23), "msg_type_ext1", "message1", "message2")
my_page.add_message("pub_key2", "msg_type2", datetime.datetime(2023, 1, 1, 1, 1, 1, 100), "msg_type_ext2", "message1", "message2")
my_page.add_message("pub_key2", "msg_type2", datetime.datetime(2023, 11, 1, 1, 1, 1, 12), "msg_type_ext2", "message1", "message2")

# page_string = my_page.to_string()
# print("Original Page:")
# print(page_string)
# newpage = Page.from_string(page_string)



# new_page_string = new_page.to_string()
# print("\nNew Page from String:")
# print(new_page_string)
# send_message(my_page)
# tmp = get_message("Page1")
# print(tmp)


# create_keys("kny", "123456")
# message = "Hello, World!"
# message = message.encode()
# print(f"Original message: {message}")
# private_key = load_private_key("123456")
# public_key = load_public_key()
# encrypted_message = encrypt_message(message, public_key)
# print("Encrypted Message:", encrypted_message)
#
# decrypted_message = decrypt_message(encrypted_message, private_key)
# print("Decrypted Message:", decrypted_message.decode('ascii'))
# print(f"Before send: {my_page.to_string()}")
# print(my_page.to_string())
# check = send_page(my_page, "test")
# print(check)
# page_string = get_page("test", '')
# print(type(page_string))
# pubKey = load_public_key()
# add_friend(pubKey, "kny")
a = get_friend("kny")
print(type(a["public_key"]))




