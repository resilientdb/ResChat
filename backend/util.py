import base64
import binascii
import datetime
import json
import os
import platform
import sys
import ipfshttpclient
import psutil

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from cryptography.fernet import Fernet

sys.path.append("kv-service_python_api")
from kv_operation import get_value, set_value


def load_config():
    """
    读取ipfs.config文件来获取IPFS接入点的IP地址，端口号等信息
    """
    with open('ipfs.config', 'r') as f:
        return f.readline()


def load_rsa_keypair(username: str, password: str):
    """
    加载RSA公钥和私钥
    """
    if os.path.exists('private_key.pem') and os.path.exists('public_key.pem'):
        with open('public_key.pem', 'rb') as f:
            public_key = RSA.import_key(f.read())
        try:
            with open("private_key.pem", "rb") as f:
                private_key = RSA.import_key(f.read(), passphrase=username + password)
        except Exception as e:
            print("Error loading private key:", str(e))
            return None, None
        return public_key, private_key


def load_fernet_key():
    """
    加载Fernet密钥
    """
    if os.path.exists('fernet.key'):
        with open('fernet.key', 'rb') as f:
            fernet_key = f.read()
        return Fernet(fernet_key)


def public_key_to_string(public_key_bytes):
    """
    将RSA公钥转换为string格式
    """
    return base64.b64encode(public_key_bytes).decode('utf-8')


def string_to_public_key(pub_key_string):
    """
    将string转换为RSA公钥格式
    """
    return RSA.importKey(pub_key_string.encode('utf-8'))


def encrypt_message_with_rsa(pub_key, message: str or bytes):
    """
    将所给定的信息使用RSA公钥进行加密
    """
    cipher_rsa = PKCS1_OAEP.new(pub_key)
    if type(message) is str:
        message = message.encode()
    encrypted_message = cipher_rsa.encrypt(message)
    encrypted_message = binascii.hexlify(encrypted_message).decode('ascii')
    return encrypted_message


def decrypt_message_with_rsa(pri_key, enc_message):
    """
    使用RSA私钥解密信息
    """
    # 将十六进制字符串转换为字节
    encrypted_message_bytes = binascii.unhexlify(enc_message)

    # 创建PKCS1_OAEP对象用于解密
    cipher_rsa = PKCS1_OAEP.new(pri_key)

    # 解密消息
    decrypted_message = cipher_rsa.decrypt(encrypted_message_bytes)

    # 将字节解码成字符串
    return decrypted_message.decode('utf-8')


def get_inner_folder(file_structure: dict, current_folder: list) -> dict:
    """
    获取当前目录下的文件结构，返回一个Python字典
    """
    sub_folder = file_structure
    for i in current_folder:
        sub_folder_name = "/" + i
        sub_folder = sub_folder.get(sub_folder_name)
    return sub_folder


def create_user(username: str, password: str) -> bool:
    """
    创建用户，创建RSA公私钥，Fernet密钥，并将加密后的初始化文件夹结构上传到ResilientDB
    """
    user_info = get_value(username)
    if user_info == "" or user_info == "\n":
        rsa_key = RSA.generate(2048)
        fernet_key = Fernet.generate_key()
        with open("fernet.key", "wb") as key_file:
            key_file.write(fernet_key)
        private_key = rsa_key.exportKey(passphrase=username + password, pkcs=8)
        public_key_str = rsa_key.publickey().export_key()
        public_key = rsa_key.public_key()
        with open(f"private_key.pem", "wb") as f:
            f.write(private_key)
        with open(f"public_key.pem", "wb") as f:
            f.write(public_key_str)
        set_value(username, encrypt_message_with_rsa(public_key, json.dumps({"/root": {}})))
        set_value(username + " public_key", public_key_str)
        return True
    else:
        return False


def clear_screen():
    """
    清屏
    """
    # 检查操作系统
    os_name = platform.system()
    if os_name == "Windows":
        # 如果是Windows系统，使用cls命令
        os.system('cls')
    else:
        # 对于Linux和Mac，使用clear命令
        os.system('clear')


def create_folder(file_structure, current_location, new_folder_name):
    """新建文件夹，将返回一个更新后的Python字典"""
    current_dict = file_structure
    for folder in current_location:
        folder_path = "/" + folder
        current_dict = current_dict.setdefault(folder_path, {})

    new_folder_path = "/" + new_folder_name
    if new_folder_path not in current_dict:
        current_dict[new_folder_path] = {}
        print(f"Folder '{new_folder_name}' created.")
    else:
        print(f"Folder '{new_folder_name}' already exists at {'/'.join(current_location)}")

    return file_structure


def upload_single_file(file_path: str, fernet_key, ipfs_config):
    """
    打开，分块读取，加密，上传单个文件
    """
    client = ipfshttpclient.connect(ipfs_config)
    chunk_size = int(psutil.virtual_memory().available * 0.01)
    tmp_upload_dir = "tmp_upload"
    os.makedirs(tmp_upload_dir, exist_ok=True)

    if os.path.exists(file_path):
        file_name = os.path.basename(file_path)
        file_size_mb = round(os.path.getsize(file_path) / 1024 / 1024, 2)
        hash_list = []
        count = 0
        with open(file_path, 'rb') as input_file:
            while True:
                chunk = input_file.read(chunk_size)
                if not chunk:
                    time_uploaded = datetime.datetime.now()
                    break

                encrypted_chunk = fernet_key.encrypt(chunk)
                encrypted_file_path = os.path.join(tmp_upload_dir, f"{file_name}_{count}.encrypt")
                with open(encrypted_file_path, 'wb') as encrypted_file:
                    encrypted_file.write(encrypted_chunk)
                res = client.add(encrypted_file_path)
                hash_list.append(res['Hash'])
                os.remove(encrypted_file_path)

                count += 1

        print(f"{file_name} uploaded successfully")
    else:
        print(f"{file_path} does not exist")
        return None

    return file_name, hash_list, file_size_mb, time_uploaded


def download_single_file(file_hash: list, file_name: str, fernet_key, ipfs_config, save_path='downloads'):
    """下载文件快，解密，写入单个文件"""
    client = ipfshttpclient.connect(ipfs_config)
    # 确保下载目录存在
    os.makedirs('tmp_download', exist_ok=True)
    os.makedirs('downloads', exist_ok=True)

    # 完整的保存路径
    final_path = os.path.join(save_path, file_name)

    with open(final_path, 'wb') as final_file:
        for h in file_hash:
            client.get(h, target='tmp_download')
            with open('tmp_download/' + h, 'rb') as temp_file:
                encrypted_chunk = temp_file.read()
                decrypted_chunk = fernet_key.decrypt(encrypted_chunk)
                final_file.write(decrypted_chunk)
            os.remove(f'tmp_download/{h}')

    print(f"{file_name} downloaded and decrypted successfully")
    return
