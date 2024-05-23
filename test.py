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

kv.send_message("test_1", "\n")
kv.send_message("test_0", "\n")
kv.send_message("test", "\n")
kv.send_message("2940009621", "\n")
kv.send_message("test1", "\n")
kv.send_message("test0", "\n")

print(kv.get_message("test_0 test_1 3"))
kv.send_message("test_0 test_1 1", "\n")
kv.send_message("test_0 test_1 2", "\n")