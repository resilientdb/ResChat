import subprocess
from page import Page
import os

"""TODO: These should be changed when everything works on local"""
command_path = os.path.expanduser('~/Desktop/ECS189f_Project/resilientdb/bazel-bin/service/tools/kv/api_tools/kv_service_tools') # Path under Ubuntu environment
config_path = os.path.expanduser('~/Desktop/ECS189f_Project/resilientdb/service/tools/config/interface/service.config') # Path under Ubuntu environment

# This function will run commandline instruction to set a value, key = page name, value = message
def send_message(page: Page):
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


# This function will get a key from the chain
def get_message(page_name: str):
    command = [
        command_path,
        config_path,
        "get",
        page_name
    ]
    result = subprocess.run(command, capture_output=True, text=True)

    def parse_get_stdout(output):
        stripped_output = output[len('client get value = '):]
        return stripped_output
    return parse_get_stdout(result.stdout)

# This function is to send a friend request
def friend_request(receiver_pub: str, sender_pub: str):
    msg_string = "FRIEND" + sender_pub
    command = [
        command_path,
        config_path,
        "set",
        receiver_pub,
        msg_string
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.stdout == "client set ret = 0":
        return True
    else:
        return False

