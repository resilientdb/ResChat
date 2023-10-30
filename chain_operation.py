import random
import subprocess
from page import Page
import os
import time
"""TODO: These should be changed when everything works on local"""
# Path under Ubuntu environment
command_path = os.path.expanduser('~/Desktop/ECS189f_Project/resilientdb/bazel-bin/service/tools/kv/api_tools/kv_service_tools')
# Path under Ubuntu environment
config_path = os.path.expanduser('~/Desktop/ECS189f_Project/resilientdb/service/tools/config/interface/service.config')


# This function will run commandline instruction to set a value, key = page name, value = message
def send_page(page: Page):
    page_string = page.to_string()
    page_name = page.pageName
    command = [
        command_path,
        config_path,
        "set",
        page_name,
        page_string
    ]

    result = subprocess.run(command, capture_output=True, text=True)
    if result.stdout == "client set ret = 0":
        return True
    else:
        return False


def parse_get_stdout(output):
    stripped_output = output[len('client get value = '):]
    return stripped_output


# This function will get a page from the chain
def get_page(page_name: str, page_num: str):
    pg = page_name + " " + page_num
    command = [
        command_path,
        config_path,
        "get",
        page_name
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    return parse_get_stdout(result.stdout)


# This function is to send a friend request
def send_friend_request(receiver_pub: str, sender_pub: str) -> bool:
    msg_string = "FRIEND " + sender_pub
    command = [
        command_path,
        config_path,
        "set",
        receiver_pub,
        msg_string
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    time.sleep(random.randint(2, 5))
    if result.stdout == "client set ret = 0":
        return True
    else:
        return False


# This function is to set up and send REFRIEND type of message
def re_friend_request(receiver_pub: str, answer: bool, sender_pub: str = None):
    if answer:
        msg_string = "REFRIEND YES" + " " + sender_pub
        command = [
            command_path,
            config_path,
            "set",
            receiver_pub,
            msg_string
        ]
        time.sleep(random.randint(2, 5))
        result = subprocess.run(command, capture_output=True, text=True)
        if result.stdout == "client set ret = 0":
            print("You have successfully add this user as friend.")
            return True
        else:
            return False
    else:
        print("You have rejected this friend request")
        return True


# This function will read the chain by user's public key to check is there any friend request send to this user
def get_friend_request(pub_key) -> None or str:
    command = [
        command_path,
        config_path,
        "get",
        pub_key
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    stripped_string = parse_get_stdout(result.stdout)
    if stripped_string == '\n':
        return None
    else:
        return stripped_string




