import subprocess
from page import Page
import os

"""TODO: These should be changed when everything works on local"""
command_path = os.path.expanduser('~/Desktop/ECS189f_Project/resilientdb/bazel-bin/service/tools/kv/api_tools/kv_service_tools')
config_path = os.path.expanduser('~/Desktop/ECS189f_Project/resilientdb/service/tools/config/interface/service.config')
def send_message(page: Page):
    page_string = page.to_string()
    page_name = page.pageName
    # print(f"PAGE NAME: {page_name}")
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