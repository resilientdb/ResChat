import numpy as np
from page import Page  # 导入Page类
from chain_operation import send_message, get_message

# 创建Page类的实例
my_page = Page("Page1")
my_page.add_message("pub_key1", "msg_type1", "t_stamp1", "msg_type_ext1", "message1")
my_page.add_message("pub_key2", "msg_type2", "t_stamp2", "msg_type_ext2", "message2")
my_page.add_message("pub_key2", "msg_type2", "t_stamp2", "msg_type_ext2", "message2")

# page_string = my_page.to_string()
# print("Original Page:")
# pstr = '"' + my_page.to_string().replace('"', '\\"') + '"'
# print(pstr)
#
# new_page = Page.from_string(page_string)
# new_page_string = new_page.to_string()
# print("\nNew Page from String:")
# print(new_page_string)
send_message(my_page)
tmp = get_message("Page1")
print(tmp)
