import numpy as np
from page import *
from chain_operation import *
import datetime
from file_operations import *
from encryption import *
from db import *
from message import *

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
add_friend("-----BEGIN PUBLIC KEY-----" + "\n" +
           "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAw9RejkTXIjGWqPMsOPCO" + "\n" +
           "CivX0aMbYIA5Ii15kDfexTxoMiadnXugjGr9N0POdULTnwvObLnSHgevSLmebqp3" + "\n" +
           "dfgconhBrtD7GK+DFAnTCGvLVYCz+9IMU+H6BxuHjvRqDcIqGgIEKV7pv8pCrnp3" + "\n" +
           "iNFq0C+eKcLu51//jeEYYFDaUZ01bTQzQMobx8zTNZuCd2McBYs82uCJu6HNX/HG" + "\n" +
           "OO2U8RIE/kEA+BNBSB4/81WCTRSiSR74b1sLIoqOTfIL5hSkwvN50OkOfnIPtjby" + "\n" +
           "w7o5mtNJNv6raktThcP2eFBBBWdLLRT97H6EvLxPu2ELJLIv24cGxis8gkjuyf4W" + "\n" +
           "QQIDAQAB" + "\n" +
           "-----END PUBLIC KEY-----", "test")
