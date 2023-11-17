import numpy as np
from page import *
from chain_operation import *
import datetime
from file_operations import *
from encryption import *
from db import *
from message import *

print(type(load_public_key()))
# my_page = Page()
# my_page.add_message("pub_key1", "msg_type1", datetime.datetime(2023, 11, 1, 1, 1, 1, 111230).strftime("%Y-%m-%d %H:%M:%S.%f"), "msg_type_ext1", "message1", "Test")
# my_page.add_message("pub_key2", "msg_type2", datetime.datetime(2023, 1, 1, 1, 1, 1, 111100).strftime("%Y-%m-%d %H:%M:%S.%f"), "msg_type_ext2", "message1", "Test")
# my_page.add_message("pub_key2", "msg_type2", datetime.datetime(2023, 11, 1, 1, 1, 1, 111120).strftime("%Y-%m-%d %H:%M:%S.%f"), "msg_type_ext2", "message1", "Test")
#
# my_page.sort_by_time()
#
# page_string = my_page.to_string()
# print(page_string)
# new_page = Page.from_string(page_string)
#
# msg = new_page.all_messages()
#
# print(msg)
# clean("kny")
# send_message("this is a test", "kny")
# update = get_update("kny", "123456")
# print(update[0][0])
# if get_update("kny") is None:
#     print("NONE")
# add_friend("-----BEGIN PUBLIC KEY-----" + "\n" +
#            "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAmZwykmd8pWnFYLSuoTxq" + "\n" +
#            "ZvE2q+WENHcb/HIqhjpquKdJNwCoPV+dSXXTKiVmT806LzN8EJK6DM4b0oYsQ5fU" + "\n" +
#            "OABA4i/kjQtkE2Z1ykc1XEeRbIIXlTDPyJ79iqvHUVQYFnz5lZdNhCpBb4dZqNNO" + "\n" +
#            "dFAA1+Kimtab0lxOIpD2hW/CNzG+Mx1LESSiVvMb9Hl1dVmm0ayvZYJ/GieaV4Pg" + "\n" +
#            "BkpbwawtA1y1bIsUldTvzKIvR4qMfh1N4DLlUJvPhI7IbxNf6xRTtYua147G6wWS" + "\n" +
#            "ia6LQx5vGBUPau5IqbAmTXVlw65rexK2UqusMsDrdHBOEttfsV1b1toYsE259e2z" + "\n" +
#            "FQIDAQAB" + "\n" +
#            "-----END PUBLIC KEY-----", "test")
# clean("test")

print(type(encrypt_message(b"test", load_public_key())))
