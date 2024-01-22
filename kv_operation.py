import subprocess
from page import Page
import os


# Working directory where the bazel workspace is located
# working_directory = os.path.expanduser('~/Desktop/incubator-resilientdb')
# Config path relative to the working_directory
# config_path = "/home/ubuntu/Desktop/incubator-resilientdb/scripts/deploy/config_out/client.config"

# config_path = ""


def assign_resdb_path(master_folder_location: str) -> bool:
    config_path = os.path.join(master_folder_location, "scripts/deploy/config_out/client.config")
    if os.path.exists(config_path):
        with open(f"resdb_path.config", "w") as f:
            f.write(master_folder_location)
            return True
    else:
        print(f"{master_folder_location}/scripts/deploy/config_out/client.config does not exists.")
        return False


def load_resdb_path() -> bool or str:
    if os.path.exists("resdb_path.config"):
        with open(f"resdb_path.config", "r") as f:
            config_path = f.readline()
            if os.path.exists(config_path):
                return config_path
            else:
                print(f"{config_path} does not exists.")
                return False
    else:
        print("Please assign ResilientDB path first")
        return False


def send_message(key: str, value: str):
    command = [
        "bazel", "run", "//service/tools/kv/api_tools:kv_service_tools", "--",
        config_path, "set", key, value
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


def get_message(key: str):
    command = [
        "bazel", "run", "//service/tools/kv/api_tools:kv_service_tools", "--",
        config_path, "get", key
    ]
    result = subprocess.run(command, capture_output=True, text=True, cwd=working_directory)
    if result.returncode != 0:
        print("Error executing command:", result.stderr)
        return ""
    return parse_get_stdout(result.stdout)
