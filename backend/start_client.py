import json
import threading

import util
import sys
import os

sys.path.append('kv-service_python_api/')
from kv_operation import get_value, set_value

username = None
public_key = None
private_key = None
file_structure = {}
current_location = ["root"]
fernet_key = None
util.clear_screen()
ipfs_config = None


def update_structure_with_file_info(file_name, file_hash: list, file_size_mb, upload_time):
    """
    用于增加文件到文件夹结构中
    file_name: 文件名
    file_hash: IPFS所返回的文件哈希
    file_size_mb: 文件大小（Mega Bytes）
    upload_time: 文件上传完毕的时间
    """
    global file_structure, current_location
    # 初始化dict_pointer指向file_structure的根
    dict_pointer = file_structure["/root"]

    # 遍历current_location来定位到正确的目录
    # 注意，这里我们跳过了列表的第一个元素"root"，因为我们已经开始于"/root"
    for folder in current_location[1:]:
        if "/" + folder not in dict_pointer:
            # 如果路径不存在，则创建新目录
            dict_pointer["/" + folder] = {}
        dict_pointer = dict_pointer["/" + folder]

    # 在当前位置添加或更新文件信息
    dict_pointer[file_name] = {
        "hash": file_hash,
        "size_mb": file_size_mb,
        "upload_time": upload_time.isoformat()
    }


def encapsulated_download(download_target: str, save_path='downloads'):
    """
    封装过后的download函数，可以处理单个或多个文件的下载
    download_target: 想要下载的目录或文件
    save_path: 本地的保存路径（默认在downloads文件夹下）
    """

    # 获取最内层嵌套文件夹
    download_inner_folder = util.get_inner_folder(file_structure, current_location)
    # 下载单个文件
    if (not download_target.startswith('/')) and download_target in download_inner_folder:
        # 获取文件信息
        file_detail = download_inner_folder[download_target]
        # 下载，解密，写入
        util.download_single_file(file_detail['hash'], download_target, fernet_key, ipfs_config, save_path)
        return
    # 下载多个文件
    elif download_target.startswith('/') and download_target in download_inner_folder:
        # 获取这个文件夹下所有文件的信息
        folder_detail = download_inner_folder[download_target]
        for file_name, file_info in folder_detail.items():
            # 下载，解密，写入
            util.download_single_file(file_info['hash'], file_name, fernet_key, ipfs_config, save_path)
        return
    else:
        print(f"{download_target} does not exist.")
        return


def encapsulated_upload(path):
    """
    封装过后的upload函数，可以处理单个或多个文件的上传
    path: 文件/文件夹的本地路径
    """

    # 上传单个文件
    if os.path.isfile(path):
        # 读取，分块，加密，上传
        file_name, file_hash_list, file_size_mb, upload_time = util.upload_single_file(path, fernet_key, ipfs_config)
        # 将文件信息写入文件夹结构
        update_structure_with_file_info(file_name, file_hash_list, file_size_mb, upload_time)
    # 上传多个文件
    elif os.path.isdir(path):
        file_path_list, res_list = [], []
        # 遍历该文件夹下的所有文件以及所有嵌套文件夹下的所有文件
        for root, dirs, files in os.walk(path):
            for name in files:
                file_path = str(os.path.join(root, name))
                file_path_list.append(file_path)
        # 统计全部文件个数并询问用户是否上传
        user_in = input(
            f"There are total {len(file_path_list)} files found, do you want to upload them all? [y]/no: ")
        user_in = user_in.lower()

        # 用户选择上传
        if user_in == 'y' or user_in == 'yes':
            # 遍历所有文件
            for file_path in file_path_list:
                # 读取，分块，加密，上传
                file_name, file_hash_list, file_size_mb, upload_time = util.upload_single_file(file_path,
                                                                                               fernet_key,
                                                                                               ipfs_config)
                # 将该文件信息写入临时的列表中
                res_list.append([file_name, file_hash_list, file_size_mb, upload_time])

            # 更新文件夹结构
            for res in res_list:
                update_structure_with_file_info(res[0], res[1], res[2], res[3])
        # 用户不选择上传
        else:
            print("Upload stopped.")
            return
    # 文件或目录不存在
    else:
        print(f"{path} does not exist.")
        return

    # 加密文件夹结构并在ResilientDB中更新
    set_value(username, fernet_key.encrypt((json.dumps(file_structure)).encode()))
    return


# 如果RSA公私钥和Fernet Key不存在，要求用户创建
if not os.path.exists("private_key.pem") or not os.path.exists("public_key.pem") or not os.path.exists("fernet.key"):
    print("No RSA keypair found, please create user")
    while True:
        username_in = input("Please input your username: ")
        password_in = input("Please input your password: ")
        # 检查用户名是否重复
        result = util.create_user(username_in, password_in)
        if not result:
            util.clear_screen()
            print("Username has already taken, please try another one")
        else:
            util.clear_screen()
            print("Sign up successfully, please login")
            break


while True:
    # 登录
    username_in = input("Username: ")
    password_in = input("Password: ")
    public_key, private_key = util.load_rsa_keypair(username_in, password_in)
    # 登陆失败
    if public_key is None and private_key is None:
        util.clear_screen()
        print("Wrong username or password, please try again")
    # 登陆成功
    else:
        print("Login successfully")
        print("loading information")
        # 加载RSA公私钥和Fernet密钥
        username = username_in
        fernet_key = util.load_fernet_key()
        ipfs_config = util.load_config()
        break

# 从ResilientDB获取文件夹结构并解密
file_structure = json.loads(fernet_key.decrypt(get_value(username)))
util.clear_screen()
print("Welcome to ResDrive!")
print("Type help to see commands")

# 主程序循环
while True:
    # 获取用户输入
    operation = input("/" + "/".join(current_location) + " >").split()

    # 检查用户输入
    if len(operation) == 0:
        print("Operation unidentified.\nPlease use help command to show operations")
        continue

    # 处理ls指令
    if operation[0] == "ls":
        # 从ResilientDB获取文件夹结构并解密
        file_structure = json.loads(fernet_key.decrypt((get_value(username)).encode()))

        # 找到当前目录下的字典结构
        inner_folder = util.get_inner_folder(file_structure, current_location)

        # 输出所有该目录下的键
        for names in inner_folder.keys():
            print(names, end="\t" + "\t")
        print("\n")

    # 处理cd指令
    elif operation[0] == "cd":
        # 指令长度错误
        if len(operation) != 2:
            print("Please follow: cd [target folder]")
        else:
            # 获取目标文件夹名称
            target_folder_name = operation[1]
            # 获取新文件夹名称
            new_location = current_location + [target_folder_name]
            # 获取新文件夹结构字典
            inner_folder = util.get_inner_folder(file_structure, new_location)
            # 该文件夹存在
            if inner_folder is not None:
                current_location = new_location
            # 该文件夹不存在
            else:
                print(f"{target_folder_name}: No such folder")

    # 处理rm指令
    elif operation[0] == "rm":
        # 指令长度错误
        if len(operation) != 2:
            print("Please follow: rm [target name]")
        else:
            # 目标名称
            target_name = operation[1]
            # 找到当前目录下的字典结构
            inner_folder = util.get_inner_folder(file_structure, current_location)
            # 查看目标名称为文件还是目录
            if target_name in inner_folder:
                target_path = target_name
            else:
                target_path = "/" + target_name

            # 目标在该目录下
            if target_path in inner_folder:
                # 目标为目录并且该目录下用内容
                if len(inner_folder[target_path]) != 0 and target_path.startswith('/'):
                    answer = input(
                        f"{target_name} is not empty, rm will remove all contents inside this folder, "
                        f"do you want to continue [y]/n: ")
                    answer = answer.lower()
                    if answer == "y" or answer == "yes":
                        del inner_folder[target_path]
                        print(f"{target_name} has been removed.")
                        encrypted_fs = fernet_key.encrypt((json.dumps(file_structure)).encode())
                        set_value(username, encrypted_fs)
                # 目标为文件或者为空目录
                else:
                    # 执行删除操作
                    del inner_folder[target_path]
                    print(f"{target_name} has been removed.")
                    encrypted_fs = fernet_key.encrypt((json.dumps(file_structure)).encode())
                    set_value(username, encrypted_fs)
            else:
                print(f"{target_name}: No such file or folder")

    # 处理mkdir指令
    elif operation[0] == "mkdir":
        # 检查指令长度
        if len(operation) != 2:
            print("Please follow: mkdir [new folder name]")
        else:
            # 创建新文件夹
            new_folder_name = operation[1]
            file_structure = util.create_folder(file_structure, current_location, new_folder_name)
            # 更新ResilientDB文件夹结构
            encrypted_fs = fernet_key.encrypt((json.dumps(file_structure)).encode())
            set_value(username, encrypted_fs)

    # 处理quit指令
    elif operation[0] == "quit" or operation[0] == "q":
        break

    # 处理upload指令
    elif operation[0] == "upload":
        # 检查指令长度
        if len(operation) != 2:
            print("Please follow: upload [file/folder location]")
        else:
            # 启用线程后台处理上传，以便用户可以在上传的同时进行其他操作
            upload_thread = threading.Thread(target=encapsulated_upload, args=(operation[1],))
            upload_thread.start()
            # upload_thread.join()
            continue

    # 处理download指令
    elif operation[0] == "download":
        # 检查指令长度
        if len(operation) != 2 and len(operation) != 3:
            print("Please follow: download [file/folder name] [path to save]")
        else:
            # 将文件下载到donwloads目录下
            if len(operation) == 2:
                # 启用线程后台处理下载，以便用户可以在下载的同时进行其他操作
                download_thread = threading.Thread(target=encapsulated_download, args=(operation[1],))
                download_thread.start()
                download_thread.join()
                continue
            # 将文件下载到用户指定的目录中
            else:
                # 启用线程后台处理下载，以便用户可以在下载的同时进行其他操作
                download_thread = threading.Thread(target=encapsulated_download, args=(operation[1], operation[2],))
                download_thread.start()
                download_thread.join()
                continue

    # 处理root指令
    elif operation[0] == "root":
        current_location = ['root']

    # 处理back指令
    elif operation[0] == "back":
        # 检查当前位置
        if current_location == ['root']:
            print("You already at /root")
        else:
            # 回到上一级
            current_location.pop()

    # 处理clear指令
    elif operation[0] == "clear":
        util.clear_screen()

    # 处理share指令（没写）
    elif operation[0] == "share":
        pass

    # 处理detail指令
    elif operation[0] == 'detail':
        # 检查指令长度
        if len(operation) != 2:
            print("Please follow: detail [filename]")
        else:
            # 获取文件名
            file_name = operation[1]
            # 获取当前目录字典结构
            inner_folder = util.get_inner_folder(file_structure, current_location)
            # 检查文件名是否在该目录下
            if file_name in inner_folder:
                # 输出文件名，文件大小，上传日期
                file_detail = inner_folder[file_name]
                upload_date = file_detail['upload_time']
                size_mb = file_detail['size_mb']
                print(f"File name: {file_name} \t\t File size: {size_mb}MB \t\t Upload Date: {upload_date}")

    # 处理help指令
    elif operation[0] == 'help':
        os.system('cat ops.txt')
        print()

    # 处理其他指令
    else:
        print("Operation not recognized, please use help command to show all operations")
