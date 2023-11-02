import random
import subprocess
from page import Page
import os
import time
"""TODO: These should be changed when everything works on local
(https://github.com/resilientdb/resilientdb/tree/master/scripts/deploy)"""
# Path under Ubuntu environment
command_path = os.path.expanduser('~/Desktop/ECS189f_Project/resilientdb/bazel-bin/service/tools/kv/api_tools/kv_service_tools')
# Path under Ubuntu environment
config_path = os.path.expanduser('~/Desktop/ECS189f_Project/resilientdb/service/tools/config/interface/service.config')


# This function will run commandline instruction to set a value, key = page name, value = message
def send_page(page: Page, page_name: str):
    page_string = page.to_string()
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
        pg
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    return parse_get_stdout(result.stdout)



