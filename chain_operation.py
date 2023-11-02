import subprocess
from page import Page
import os

# Working directory where the bazel workspace is located
working_directory = os.path.expanduser('~/Desktop/ECS189f_Project/resilientdb')
# Config path relative to the working_directory
config_path = "/home/ubuntu/Desktop/ECS189f_Project/resilientdb/scripts/deploy/config_out/client.config"


def send_page(page: Page, page_name: str):
    page_string = page.to_string()
    command = [
        "bazel", "run", "//service/tools/kv/api_tools:kv_service_tools", "--",
        config_path, "set", page_name, page_string
    ]
    result = subprocess.run(command, capture_output=True, text=True, cwd=working_directory)
    if result.returncode != 0:
        print("Error executing command:", result.stderr)
        return False
    if "client set ret = 0" in result.stdout:
        return True
    else:
        print("Unexpected output:", result.stdout)
        return False


def parse_get_stdout(output):
    stripped_output = output[len('client get value = '):]
    return stripped_output


def get_page(page_name: str, page_num: str):
    pg = page_name + " " + page_num
    command = [
        "bazel", "run", "//service/tools/kv/api_tools:kv_service_tools", "--",
        config_path, "get", pg
    ]
    result = subprocess.run(command, capture_output=True, text=True, cwd=working_directory)
    if result.returncode != 0:
        print("Error executing command:", result.stderr)
        return ""
    return parse_get_stdout(result.stdout)

