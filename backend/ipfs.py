import ipfshttpclient.client as ipfs
import os


client = ipfs.connect()


def read_ipfs_config() -> int:
    """
    Load IPFS config
    return 0 load successfully
    return 1 config file doesn't exist
    """
    global client
    config_path = "config/ipfs.config"

    # 检查文件是否存在
    if os.path.exists(config_path):
        with open(config_path) as f:
            client = ipfs.connect(f.readline())
            return 0
    else:
        print(f"Configuration file {config_path} does not exist.")
        return 1



def send_file_ipfs(file_path: str):
    if client is None:
        res = read_ipfs_config()
        if res == 1:
            return 1

    res = client.add(file_path)
    return res


def get_file_ipfs(save_path: str, cid: str):
    if client is None:
        res = read_ipfs_config()
        if res == 1:
            return 1
    client.get(cid=cid, target=save_path)
    return 0


# tempCid = send_file_ipfs("test/page_test.py")
# get_file_ipfs("profile_pics/", "QmbzKuzMmwt16SBtN7m2ZVMykn8eYqEnAqd72ickF5yCQR")
# print(tempCid)



