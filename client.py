import datetime
import os
import numpy as np
from Crypto.Random import get_random_bytes
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from page import Page
from kv_operation import send_message, get_message
from friend_list import (add_friend, get_all_friends,
                         delete_friend, update_page_num,
                         update_file_num, get_my_friend_list,
                         set_my_friend_list, get_current_file_count,
                         get_current_page_num)
from encryption_and_user import (create_user, load_user,
                                 encrypt_message_for_two_recipients, decrypt_message,
                                 string_to_public_key, public_key_to_string, decrypt_aes_key_with_rsa,
                                 encrypt_aes_key_with_rsa)
import random
import string

# Global Variables
"""Setting, please change following variable base on your RAM size and computing power"""
max_chunk_size_MB = 2

"""These global variables will be assigned when login function been called"""
# This variable stores login user's public key(RSA public key)
my_public_key = None

# This variable stores login user's private key(RSA private key)
my_private_key = None

# This variable stores login user's public key(string)
my_public_key_string = ""

# This variable stores login user's friend list
my_friend_list = {}

# This variable stores login user's username
my_username = ""

# This variable stores login user's password
my_password = ""

"""These global variables will be assigned/reassigned when select_friend_to_chat_with function been called"""
# This variable stores the current selected friend's nickname
current_chatting_friend_nickname = ""

# This variable stores the current selected friend's public key(RSA public key)
current_chatting_friend_public_key = None

# This variable stores the current selected friend's public key(string)
current_chatting_friend_public_key_string = ""

# This variable stores the current selected friend's username
current_chatting_friend_username = ""

# This variable stores the page name, when system want to get a page just use this variable + " " + page_number
current_chatting_page_name = ""

# This variable records which previous page the user has loaded.
previous_page_num = -1

# This list contains all information that required for frontend message display
# - Decrypted message/file location(key)
# - Message type(TEXT or FILE)
# - Timestamp
# - Message type extension(NONE or file name)
# - NONE or encrypted AES key(NONE if this message is TEXT)
# - RECEIVER or SENDER to identify current user is sender or receiver of this message
current_chat_history = []

# Not in use right now
current_chatting_message_count = -1


def check_connection_to_chain():
    """BUG!!"""
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for i in range(10))

    # 使用ThreadPoolExecutor来处理超时
    with ThreadPoolExecutor(max_workers=2) as executor:
        # 尝试send_message并设置超时时间
        send_future = executor.submit(send_message, "test", random_string)
        try:
            send_future.result(timeout=3)  # 3秒超时
        except TimeoutError:
            print("send有问题")

        # 尝试get_message并设置超时时间
        get_future = executor.submit(get_message, "test")
        try:
            result = get_future.result(timeout=3)
            if result == random_string:
                return True
        except TimeoutError:
            print("get有问题")

    return False


def update_max_data_chunk_size(size):
    """This function should be called when user want to change max_chunk_size_MB"""
    global max_chunk_size_MB
    max_chunk_size_MB = size


def login(username: str, password: str):
    """This function will be called when user login. It will assign values to user's information global variables."""
    global my_public_key, my_private_key, my_friend_list
    global my_username, my_password, my_public_key_string
    user_info = load_user(username, password)
    if user_info is False:
        print("User not exist or wrong password or error loading private key")
        return False
    else:
        my_public_key = user_info[2]
        my_private_key = user_info[3]
        my_friend_list = get_my_friend_list(username)
        my_username = username
        my_password = password
        my_public_key_string = public_key_to_string(my_public_key)
        return True


def logout():
    """This function will be called when user logout. It will set an updated friend list into ResilientDB"""
    global my_username, my_friend_list
    set_my_friend_list(my_username, my_friend_list)


def select_friend_to_chat_with(nickname: str) -> bool:
    """This function will be called when select a friend to chat. It will update all the global variables"""
    global my_friend_list, current_chatting_friend_nickname, current_chatting_page_name
    global current_chatting_friend_public_key, current_chatting_friend_username
    global current_chatting_friend_public_key_string, current_chatting_message_count
    global current_chat_history, previous_page_num
    if nickname not in my_friend_list:
        return False
    else:
        current_chatting_friend_public_key = string_to_public_key(my_friend_list[nickname]['public_key'])
        current_chatting_friend_nickname = nickname
        current_chatting_friend_username = my_friend_list[nickname]['friend_username']
        sorted_usernames = sorted([my_username, current_chatting_friend_username])
        first_username = sorted_usernames[0]
        second_username = sorted_usernames[1]
        current_chatting_page_name = first_username + " " + second_username
        current_chatting_friend_public_key_string = public_key_to_string(current_chatting_friend_public_key)
        current_chatting_message_count = -1
        current_chat_history = []
        current_page_num = get_current_page_num(my_username, current_chatting_friend_username)
        if current_page_num >= 3:
            previous_page_num = current_page_num - 2
        return True


def encapsulated_create_user(username: str, password: str):
    """Encapsulated create_user function to allow front-end use it more easily"""
    result = create_user(username, password)
    if result:
        login(username, password)
        return True
    else:
        return False


def encapsulated_add_friend(friend_username: str, nickname: str):
    """
    Encapsulates the add_friend function to allow it can modify those global variables.
    This function should be called when user want to add a friend
    """
    global my_username, my_friend_list
    result = add_friend(friend_username, my_username, nickname, my_friend_list)
    if not result:
        return result
    else:
        my_friend_list = result
        set_my_friend_list(my_username, my_friend_list)
        return result


def encapsulated_decrypt_message(encrypted_message) -> []:
    """Encapsulated decrypt_message_function to allow other function to use it more easily"""

    if encrypted_message[0] == my_public_key_string:
        if encrypted_message[1] == "TEXT":
            decrypted_message = decrypt_message(encrypted_message[4], encrypted_message[6], my_private_key)
            tmp = [decrypted_message, "TEXT", encrypted_message[2], "NONE", "NONE"]
        elif encrypted_message[1] == "FILE":
            tmp = [encrypted_message[4],
                   "FILE",
                   encrypted_message[2],
                   encrypted_message[3],
                   encrypted_message[6],
                   "RECEIVER"]
    else:
        if encrypted_message[1] == "TEXT":
            decrypted_message = decrypt_message(encrypted_message[4], encrypted_message[5], my_private_key)
            tmp = [decrypted_message, "TEXT", encrypted_message[2], "NONE", "NONE"]
        elif encrypted_message[1] == "FILE":
            tmp = [encrypted_message[4],
                   "FILE",
                   encrypted_message[2],
                   encrypted_message[3],
                   encrypted_message[5],
                   "SENDER"]
    return tmp


def encapsulated_delete_friend(nickname: str):
    """
    Encapsulates the delete_friend function to allow it can modify those global variables
    This function should be called when user want to delete a friend
    """
    global my_friend_list
    my_friend_list = delete_friend(nickname, my_friend_list)


def send_text_message(message: str) -> bool:
    """This function should be called when user want to send a full text message"""
    global my_public_key, my_private_key, my_friend_list, my_username, my_password, current_chatting_page_name
    global current_chatting_friend_public_key, current_chatting_friend_nickname

    # Encrypt message for two users
    (encrypted_message,
     encrypted_aes_key_sender,
     encrypted_aes_key_receiver) = encrypt_message_for_two_recipients(message,
                                                                      my_public_key,
                                                                      current_chatting_friend_public_key)

    # Get current page number
    current_page_num = get_current_page_num(my_username,
                                            current_chatting_friend_username)

    # Get current page
    page_string = get_message(current_chatting_page_name + " " + str(current_page_num))

    # Check the page exist or not
    if page_string == "\n" or page_string == "" or page_string == " ":
        page = Page()
    else:
        page = Page().from_string(page_string)
        page.sort_by_time()

    # Check if the page is full
    if page.is_full():
        # Create a new page
        new_page = Page()

        # Add message into this new page
        new_page.add_message(current_chatting_friend_public_key_string,
                             "TEXT",
                             datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:23],
                             "NONE",
                             encrypted_message,
                             encrypted_aes_key_sender,
                             encrypted_aes_key_receiver)

        # Update page number
        update_page_num(current_chatting_friend_nickname, my_username, current_chatting_friend_username)
        current_page_num += 1

        # Send page
        new_page_string = new_page.to_string()
        send_message(current_chatting_page_name + " " + str(current_page_num), new_page_string)
        return True

    else:
        # Add message into page
        page.add_message(current_chatting_friend_public_key_string,
                         "TEXT",
                         datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:23],
                         "NONE",
                         encrypted_message,
                         encrypted_aes_key_sender,
                         encrypted_aes_key_receiver)

        # Send page
        page_string = page.to_string()
        send_message(current_chatting_page_name + " " + str(current_page_num), page_string)

        return True


def send_file(path: str):
    """This function should be called when user decide to send a file"""
    global my_public_key, my_private_key, my_friend_list, my_username, my_password, current_chatting_page_name
    global current_chatting_friend_public_key, current_chatting_friend_nickname, max_chunk_size_MB

    # Check file size
    if os.path.getsize(path) / 1024 / 1024 > 5:
        print("Can not send file greater then 5MB")
        return

    with open(path, 'rb') as file:
        # Generate random AES key to ensure all file chunks encrypted with same AES key
        aes_key = get_random_bytes(16)

        # Get file name
        file_name = os.path.basename(path)

        # Get current page number
        current_page_num = get_current_page_num(my_username,
                                                current_chatting_friend_username)

        # Get current file count
        current_file_count = get_current_file_count(my_username,
                                                    current_chatting_friend_username)

        # Update file count on ResilientDB
        update_file_num(my_username, current_chatting_friend_username)

        encrypted_aes_key_sender = encrypt_aes_key_with_rsa(aes_key, my_public_key)
        encrypted_aes_key_receiver = encrypt_aes_key_with_rsa(aes_key, current_chatting_friend_public_key)

        # Get current page
        page_string = get_message(current_chatting_page_name + " " + str(current_page_num))

        # Check the page exist or not
        if page_string == "\n" or page_string == "" or page_string == " ":
            page = Page()
        else:
            page = Page().from_string(page_string)
            page.sort_by_time()

        # Check if the page is full
        if page.is_full():
            # Create a new page
            new_page = Page()

            # Add file location into this new page
            new_page.add_message(current_chatting_friend_public_key_string,
                                 "FILE",
                                 datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:23],
                                 file_name,
                                 current_chatting_page_name + " FILE " + str(current_file_count),
                                 encrypted_aes_key_sender,
                                 encrypted_aes_key_receiver)

            # Update page number
            update_page_num(current_chatting_friend_nickname, my_username, current_chatting_friend_username)
            current_page_num += 1

        else:
            # Add file location into this new page
            page.add_message(current_chatting_friend_public_key_string,
                             "FILE",
                             datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:23],
                             file_name,
                             current_chatting_page_name + " FILE " + str(current_file_count),
                             encrypted_aes_key_sender,
                             encrypted_aes_key_receiver)

        # Send page
        new_page_string = page.to_string()
        send_message(current_chatting_page_name + " " + str(current_page_num), new_page_string)

        i = 1
        while True:

            next_chunk = file.read(max_chunk_size_MB * 1024 * 1024)
            if not next_chunk:
                # print(f"CHECK i: {i}")
                break

            # Convert next chunk into string
            next_chunk_string = next_chunk.hex().encode()

            # Encrypt next chunk
            encrypted_next_chunk, _, _ = encrypt_message_for_two_recipients(next_chunk_string,
                                                                            my_public_key,
                                                                            current_chatting_friend_public_key,
                                                                            aes_key)

            # Send next chunk
            send_message(current_chatting_page_name + " FILE " + str(current_file_count) + " " + str(i),
                         encrypted_next_chunk)

            # Update counter
            i += 1

        # Send FINISHED message
        send_message(current_chatting_page_name + " FILE " + str(current_file_count), "FINISHED")


def initial_chat_history_loading():
    """
    This function should be only called once when chat history been first loaded
    Return type is a list and constructed by following elements:
    - Decrypted message/file location(key)
    - Message type(TEXT or FILE)
    - Timestamp
    - Message type extension(NONE or file name)
    - NONE or decrypted AES key(NONE if this message is TEXT)
    """
    global my_username, current_chatting_friend_username, my_public_key_string, my_private_key, current_chat_history

    # Get current page
    current_page = get_current_page_num(my_username, current_chatting_friend_username)

    # Get page
    page_string_2 = get_message(current_chatting_page_name + " " + str(current_page))
    page_string_1 = get_message(current_chatting_page_name + " " + str(current_page - 1))

    # Check page is empty or not
    if (page_string_2 == "\n" or page_string_2 == "" or page_string_2 == " ") and (
            page_string_1 == "\n" or page_string_1 == "" or page_string_1 == " "):
        return
    elif (page_string_2 != "\n" or page_string_2 != "" or page_string_2 != " ") and (
            page_string_1 == "\n" or page_string_1 == "" or page_string_1 == " "):
        page_2 = Page().from_string(page_string_2)
        page_1 = Page()
    else:
        page_2 = Page().from_string(page_string_2)
        page_1 = Page().from_string(page_string_1)

    # Sort by time
    page_2.sort_by_time()
    page_1.sort_by_time()

    # Get all messages from these two pages
    page_2_messages = page_2.all_messages()
    page_1_messages = page_1.all_messages()

    # Create a return list
    current_chat_history = []

    # Decrypt messages
    for i in range(len(page_1_messages)):
        current_chat_history.append(encapsulated_decrypt_message(page_1_messages[i]))

    for j in range(len(page_2_messages)):
        current_chat_history.append(encapsulated_decrypt_message(page_2_messages[j]))


def update_chat_history():
    """This function should be cyclic called after initial_chat_history been called"""

    global my_username, current_chatting_friend_username, current_chatting_page_name, current_chat_history


    # Get current page number
    current_page_num = get_current_page_num(my_username, current_chatting_friend_username)

    # Get page string
    page_string = get_message(current_chatting_page_name + " " + str(current_page_num))

    # Check page_string is empty or not
    if page_string == "\n" or page_string == "" or page_string == " ":
        return

    # Construct page
    page = Page().from_string(page_string)

    # Get all messages
    all_messages = page.all_messages()

    tmp_list = []
    # Check if current_chat_history and all_messages is empty
    if len(all_messages) == 0 and len(current_chat_history) == 0:
        return

    elif len(current_chat_history) != 0 and len(all_messages) != 0:
        # Check if update needed
        if all_messages[len(all_messages) - 1][2] == current_chat_history[len(current_chat_history) - 1][2]:
            # No update needed situation
            return
        else:
            # Update needed situation
            flag = True
            while flag:
                pg = Page().from_string(get_message(current_chatting_page_name + " " + str(current_page_num)))
                all_messages = pg.all_messages()

                for i in range(len(all_messages) - 1, -1, -1):
                    if all_messages[i][2] == current_chat_history[len(current_chat_history) - 1][2]:
                        flag = False
                        break
                    else:
                        tmp_list.append(encapsulated_decrypt_message(all_messages[i]))

                if flag:
                    current_page_num -= 1
    else:
        # Update needed situation
        flag = True
        while flag:
            pg = Page().from_string(get_message(current_chatting_page_name + " " + str(current_page_num)))
            all_messages = pg.all_messages()

            for i in range(len(all_messages) - 1, -1, -1):
                tmp_list.append(encapsulated_decrypt_message(all_messages[i]))

            if current_page_num == 1:
                flag = False
            else:
                current_page_num -= 1

    current_chat_history.extend(tmp_list[::-1])


def download_file(path: str, key: str, encrypted_aes_key: str):
    """This function should be called when user decide to download a file"""
    # Check if this file is broken
    if get_message(key) != "FINISHED":
        print("File is broken")
        return False

    with open(path, 'wb') as file:

        i = 1
        flag = True
        while flag:
            # Get next data chunk
            encrypted_next_data_chunk_string = get_message(key + " " + str(i))

            # print(key + " " + str(i) + "222222")

            # Check is this data chunk is empty or not
            if encrypted_next_data_chunk_string == "\n" or encrypted_next_data_chunk_string == "" or encrypted_next_data_chunk_string == " ":
                # print(f"CHECK i: {i}")
                flag = False
            else:
                # Decrypt next data chunk
                decrypted_next_data_chunk = decrypt_message(encrypted_next_data_chunk_string,
                                                            encrypted_aes_key,
                                                            my_private_key)

                # Write next data chunk into file
                file.write(bytes.fromhex(decrypted_next_data_chunk))

                # Update counter
                i += 1


def load_previous_chat_history():
    """This function load one previous page and add it into chat history list"""
    global current_chat_history, previous_page_num

    # Check is there still previous page exist
    if previous_page_num == -1:
        print("No more previous chat history")
        return

    # Get page string
    previous_page_string = get_message(current_chatting_page_name + " " + str(previous_page_num))

    # Construct page
    page = Page().from_string(previous_page_string)

    # Get all messages
    all_messages = page.all_messages()

    # Decrypt messages
    for i in range(len(all_messages)):
        tmp = encapsulated_decrypt_message(all_messages[i])
        current_chat_history.insert(0, tmp)

    # Update previous_page_num
    if previous_page_num == 1:
        previous_page_num = -1
    else:
        previous_page_num -= 1
