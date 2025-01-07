import os
import sys

config_path = "config/kv_server.config"

sys.path.append("bazel/bazel-bin/kv_service")
import pybind_kv


def set_kv(key: str, value: str):
    """
    Get a key from RSDB
    :param key: The target key you want to set (str)
    :param value: The target value you want to set (str)
    :return None
    """
    global config_path
    print(f"SETTING {key}, {value}")
    pybind_kv.set(key, value, config_path)


def get_kv(key: str) -> str:
    """
    Get a key from RSDB
    :param key: The target key you want to get (str)
    :return The corresponding value of that key
    """
    global config_path
    print(f"GETTING {key}")
    return pybind_kv.get(key, config_path)
