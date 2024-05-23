import os
import sys

config_path = None

sys.path.append("bazel-out/k8-fastbuild/bin/")
import pybind_kv


def load_config_path() -> bool:
    global config_path
    if os.path.exists("config_path.config"):
        with open("config_path.config", "r") as f:
            config_path = f.readline().strip()
            return os.path.exists(config_path)
    return False


def send_message(key: str, value: str):
    global config_path
    if config_path is None:
        if not load_config_path():
            raise ValueError("无法加载配置文件路径")
    pybind_kv.set(key, value, config_path)


def get_message(key: str) -> str:
    global config_path
    if config_path is None:
        if not load_config_path():
            raise ValueError("无法加载配置文件路径")
    print(f"CHECK{key}")
    return pybind_kv.get(key, config_path)
