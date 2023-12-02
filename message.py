from page import *
from chain_operation import *
from encryption import *
from db import *
import numpy as np


def send_message(message: str, nickname: str):
    # Get receiver information
    receiver_info = get_friend(nickname)

    message = message.encode()

    # Get sender public key
    sender_pub_key = load_public_key()

    # Check if receiver information is in database or not
    if not receiver_info:
        print("Send message failed, because this receiver is not in database")
        return False

    # Get receiver's public key and current page
    receiver_pub_key = receiver_info['public_key']
    current_page = receiver_info['current_page']

    # Decode sender and receiver's public key and delete the first and last line
    decoded_receiver_pub_key = receiver_pub_key.exportKey().decode('ascii')
    lines = decoded_receiver_pub_key.splitlines()
    decoded_receiver_pub_key_str = "\n".join(lines[1:-1])

    decoded_sender_pub_key = sender_pub_key.exportKey().decode('ascii')
    lines = decoded_sender_pub_key.splitlines()
    decoded_sender_pub_key_str = "\n".join(lines[1:-1])

    # Sort these two string base on ASCII and combine them into one string
    page_name = ''.join(sorted([decoded_sender_pub_key_str, decoded_receiver_pub_key_str],
                        key=lambda x: [ord(c) for c in x]))

    # Get current page from the chain
    page_string = get_page(page_name, str(current_page))
    # Check the page exist or not
    if page_string != "\n":
        # Turn this page_string into Page
        page = Page().from_string(page_string)

        # Sort by timestamp
        page.sort_by_time()
    else:
        page = Page()

    # Encrypt message
    message_1 = encrypt_message(message, sender_pub_key)
    message_2 = encrypt_message(message, receiver_pub_key)

    # Check if this page is full
    if page.is_full():
        # Create a new page
        new_page = Page()

        # Add message into this new_page
        new_page.add_message(public_key_to_string(receiver_pub_key),
                             "TEXT",
                             datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:23],
                             "NONE",
                             message_1,
                             message_2)

        # Update local database
        update_page_num(nickname)

        # Update local variable
        current_page += 1

        # Send this page string onto the chain
        send_page(new_page, page_name, str(current_page))

    else:
        page.add_message(public_key_to_string(receiver_pub_key),
                         "TEXT",
                         datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:23],
                         "NONE",
                         message_1,
                         message_2)

        # Send this page string onto the chain
        send_page(page, page_name, str(current_page))


def get_update(nickname: str, password: str):

    # Get receiver's information
    receiver_info = get_friend(nickname)

    # Get receiver and sender's public keys
    sender_pub_key = load_public_key()
    receiver_pub_key = receiver_info["public_key"]
    sender_pri_key = load_private_key(password)

    # Get current page number
    page_num_current = receiver_info["current_page"]

    if page_num_current > 1:
        page_num_old = page_num_current - 1
    else:
        page_num_old = 0

    # Decode sender and receiver's public key and delete the first and last line
    decoded_receiver_pub_key = receiver_pub_key.exportKey().decode('ascii')
    lines = decoded_receiver_pub_key.splitlines()
    decoded_receiver_pub_key_str = "\n".join(lines[1:-1])

    decoded_sender_pub_key = sender_pub_key.exportKey().decode('ascii')
    lines = decoded_sender_pub_key.splitlines()
    decoded_sender_pub_key_str = "\n".join(lines[1:-1])

    # Sort these two string base on ASCII and combine them into one string
    page_name = ''.join(sorted([decoded_sender_pub_key_str, decoded_receiver_pub_key_str],
                               key=lambda x: [ord(c) for c in x]))

    # Get pages from chain
    current_page_string = get_page(page_name, str(page_num_current))
    old_page_string = get_page(page_name, str(page_num_old))

    # Check current page and old page are empty or not
    if current_page_string == "\n" and old_page_string == "\n":
        return None
    elif old_page_string != "\n" and current_page_string != "\n":
        old_page = Page().from_string(old_page_string)
        current_page = Page().from_string(current_page_string)
    else:
        current_page = Page().from_string(current_page_string)
        old_page = Page()

    # Check if current page is full
    if current_page.is_full():
        new_page_string = get_page(page_name, str(int(page_num_current) + 1))
        if new_page_string != "\n":
            old_page = current_page
            current_page = Page().from_string(new_page_string)
            update_page_num(nickname)

    # Combine those two pages
    old_arr = old_page.all_messages()
    current_arr = current_page.all_messages()
    encrypted_chat_history = np.vstack((old_arr, current_arr))

    # Decrypt chat history
    """
    [Receiver's public key,
    message type,
    timestamp,
    message type extension,
    message1(encrypted by sender's pub key),
    message2(encrypted by receiver's pub key)], ... ]
    """
    decrypted_chat_history = []
    for msg in encrypted_chat_history:
        tmp = []
        if msg[0] == public_key_to_string(sender_pub_key):
            tmp.append("received")
            tmp.append(msg[2])
            tmp.append(decrypt_message(msg[5], sender_pri_key).decode())
        elif msg[0] == public_key_to_string(receiver_pub_key):
            tmp.append("sent")
            tmp.append(msg[2])
            tmp.append(decrypt_message(msg[4], sender_pri_key).decode())
        decrypted_chat_history.append(tmp)

    return decrypted_chat_history


# This is a helper function to test the system. It cleans the RSDB
def clean(nickname: str):
    # Get receiver information
    receiver_info = get_friend(nickname)

    # Get sender public key
    sender_pub_key = load_public_key()

    # Check if receiver information is in database or not
    if not receiver_info:
        print("Send message failed, because this receiver is not in database")
        return False

    # Get receiver's public key and current page
    receiver_pub_key = receiver_info['public_key']
    current_page = receiver_info['current_page']

    # Decode sender and receiver's public key and delete the first and last line
    decoded_receiver_pub_key = receiver_pub_key.exportKey().decode('ascii')
    lines = decoded_receiver_pub_key.splitlines()
    decoded_receiver_pub_key_str = "\n".join(lines[1:-1])

    decoded_sender_pub_key = sender_pub_key.exportKey().decode('ascii')
    lines = decoded_sender_pub_key.splitlines()
    decoded_sender_pub_key_str = "\n".join(lines[1:-1])

    # Sort these two string base on ASCII and combine them into one string
    page_name = ''.join(sorted([decoded_sender_pub_key_str, decoded_receiver_pub_key_str],
                        key=lambda x: [ord(c) for c in x]))

    set_none(page_name, str(current_page))








