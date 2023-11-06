from page import *
from chain_operation import *
from encryption import *
from db import *


def send_message(message: str, nickname: str):
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

    # Get current page from the chain
    page_string = get_page(page_name, str(current_page))

    # Turn this page_string into Page
    page = Page().from_string(page_string)

    # Sort by timestamp
    page.sort_by_time()

    # Encrypt message
    message_1 = encrypt_message(message, sender_pub_key)
    message_2 = encrypt_message(message, receiver_pub_key)

    # Check if this page is full
    if page.is_full():
        # Create a new page
        new_page = Page()

        # Add message into this new_page
        new_page.add_message(receiver_pub_key,
                             "TEXT",
                             datetime.datetime.now(),
                             "NONE",
                             message_1,
                             message_2)

        # Update local database
        update_page_num(nickname)

        # Update local variable
        current_page += 1

        # Send this page string onto the chain
        send_page(new_page, current_page)

    else:
        page.add_message(receiver_pub_key,
                         "TEXT",
                         "NONE",
                         message_1,
                         message_2)

        # Send this page string onto the chain
        send_page(page, current_page)


def get_update(nickname: str):
    """
    TODO: Construct page name base on sender and receiver's public keys
    TODO: Use page name and page number to get latest 2 pages from the chain
    TODO: Sort these two pages by timestamp
    TODO: Check if the last page is full
            If full: Check is there anything on the next page(page number + 1)
            If not: continue
    TODO: Decrypt messages
    TODO: Show the message on the screen
    """

    # Get receiver's information
    receiver_info = get_friend(nickname)

    # Get receiver and sender's public keys
    sender_pub_key = load_public_key()
    receiver_pub_key = receiver_info["public_key"]

    # Get current page number
    current_page_num = receiver_info["current_page"]

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

    """TODO: This is not finished yet"""




