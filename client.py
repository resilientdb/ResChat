import datetime

from page import Page
from kv_operation import send_message, get_message
from file_operation import read_file, write_file
from friend_list import (add_friend, get_all_friends,
                         delete_friend, update_page_num,
                         update_file_num, get_my_friend_list,
                         set_my_friend_list, get_current_file_count,
                         get_current_page_num)
from encryption_and_user import (create_user, load_user,
                                 encrypt_message_for_two_recipients, decrypt_message,
                                 string_to_public_key, public_key_to_string)

my_public_key = None
my_private_key = None
my_friend_list = {}
my_username = ""
my_password = ""
current_chatting_friend_nickname = ""
current_chatting_friend_public_key = None
current_chatting_friend_public_key_string = ""
current_chatting_friend_username = ""
current_chatting_page_name = ""


def login(username: str, password: str):
    global my_public_key, my_private_key, my_friend_list, my_username, my_password
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


def logout():
    global my_username, my_friend_list
    set_my_friend_list(my_username, my_friend_list)


def select_friend_to_chat_with(nickname: str) -> bool:
    global my_friend_list, current_chatting_friend_nickname, current_chatting_page_name
    global current_chatting_friend_public_key, current_chatting_friend_username
    global current_chatting_friend_public_key_string
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
        return True


def encapsulated_add_friend(friend_username: str, nickname: str):
    global my_username, my_friend_list
    my_friend_list = add_friend(friend_username, my_username, nickname, my_friend_list)


def encapsulated_delete_friend(nickname: str):
    global my_friend_list
    my_friend_list = delete_friend(nickname, my_friend_list)


def send_text_message(message: str, nickname: str) -> bool:
    global my_public_key, my_private_key, my_friend_list, my_username, my_password, current_chatting_page_name
    global current_chatting_friend_public_key, current_chatting_friend_nickname

    # Encrypt message for two users
    (encrypted_message,
     encrypted_aes_key_sender,
     encrypted_aes_key_receiver) = encrypt_message_for_two_recipients(message,
                                                                      my_public_key,
                                                                      current_chatting_friend_public_key)

    # Get current page number
    current_page_num = get_current_page_num(current_chatting_friend_nickname,
                                            my_username,
                                            current_chatting_friend_username)

    # Get current page
    page_string = get_message(current_chatting_page_name + " " + str(current_page_num))

    # Check the page exist or not
    if page_string == "\n" or page_string == "" or page_string == " ":
        page = Page()
    else:
        page = Page().from_string(page_string)
        page = page.sort_by_time()

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