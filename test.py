import numpy as np
from page import Page  # 导入Page类
from chain_operation import send_message, get_message
import datetime

# 创建Page类的实例
my_page = Page("Page1")
my_page.add_message("pub_key1", "msg_type1", datetime.datetime(2023, 11, 1, 1, 1, 1, 23), "msg_type_ext1", "message1")
my_page.add_message("pub_key2", "msg_type2", datetime.datetime(2023, 1, 1, 1, 1, 1), "msg_type_ext2", "message2")
my_page.add_message("pub_key2", "msg_type2", datetime.datetime(2023, 11, 1, 1, 1, 1, 12), "msg_type_ext2", "message2")

# page_string = my_page.to_string()
# print("Original Page:")
# pstr = '"' + my_page.to_string().replace('"', '\\"') + '"'
# print(pstr)
#
# new_page = Page.from_string(page_string)
# new_page_string = new_page.to_string()
# print("\nNew Page from String:")
# print(new_page_string)
# send_message(my_page)
# tmp = get_message("Page1")
# print(tmp)
my_page.sort_by_time()
print(my_page.to_string())
