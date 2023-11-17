import sys
import time
import datetime

from encryption import load_public_key, load_private_key, encrypt_message, decrypt_message
from db import add_friend, list_friends, get_friend, update_page_num
from page import Page
from chain_operation import send_page, get_page

def send_message(nickname, message):
    receiver_info = get_friend(nickname)

    if not receiver_info:
        print("This user is not your friend yet. Please add friend first.")
        return

    sender_pub_key = load_public_key()
    receiver_pub_key = receiver_info['public_key']
    current_page = receiver_info['current_page']

    message = message.encode()
    message_1 = encrypt_message(message, sender_pub_key)
    message_2 = encrypt_message(message, receiver_pub_key)

    page_name, current_page, page = prepare_page(sender_pub_key, receiver_pub_key, current_page)

    if page.is_full():
        new_page = Page()
        new_page.add_message(nickname, "TEXT", get_current_timestamp(), "NONE", message_1, message_2)
        update_page_num(nickname)
        current_page += 1
        send_page(new_page, page_name, str(current_page))
    else:
        page.add_message(nickname, "TEXT", get_current_timestamp(), "NONE", message_1, message_2)
        send_page(page, page_name, str(current_page))

    print("Message sent.")

def prepare_page(sender_pub_key, receiver_pub_key, current_page):
    decoded_sender_pub_key = sender_pub_key.exportKey().decode('ascii')
    sender_lines = decoded_sender_pub_key.splitlines()
    decoded_sender_pub_key_str = "\n".join(sender_lines[1:-1])

    decoded_receiver_pub_key = receiver_pub_key.exportKey().decode('ascii')
    receiver_lines = decoded_receiver_pub_key.splitlines()
    decoded_receiver_pub_key_str = "\n".join(receiver_lines[1:-1])

    page_name = ''.join(sorted([decoded_sender_pub_key_str, decoded_receiver_pub_key_str],
                               key=lambda x: [ord(c) for c in x]))

    page_string = get_page(page_name, str(current_page))
    if page_string != "\n":
        page = Page().from_string(page_string)
    else:
        page = Page()

    return page_name, current_page, page

def get_current_timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:23]

def update_chat_history(nickname):
    receiver_info = get_friend(nickname)

    if not receiver_info:
        print("No chat history available.")
        return None

    sender_pub_key = load_public_key()
    sender_pri_key = load_private_key()  # Assuming the private key does not require a password
    receiver_pub_key = receiver_info["public_key"]
    page_num_current = receiver_info["current_page"]

    page_name, _, current_page = prepare_page(sender_pub_key, receiver_pub_key, page_num_current)
    old_page_string = get_page(page_name, str(page_num_current - 1)) if page_num_current > 1 else "\n"

    decrypted_chat_history = []
    for page_string in [old_page_string, current_page.to_string()]:
        if page_string != "\n":
            page = Page().from_string(page_string)
            for msg in page.all_messages():
                sender, _, timestamp, _, message1, message2 = msg
                decrypted_message = decrypt_message(message1 if sender == public_key_to_string(receiver_pub_key) else message2, sender_pri_key)
                decrypted_chat_history.append((sender, timestamp, decrypted_message))

    return decrypted_chat_history

def main():
    while True:
        print("\nMain Menu:")
        print("1. Send message")
        print("2. Quit")
        choice = input("Enter your choice: ")

        if choice == "1":
            second_menu()
        elif choice == "2":
            sys.exit(0)
        else:
            print("Invalid choice. Please try again.")

def second_menu():
    while True:
        print("\nFriends List:")
        print_friends_list()
        print("Second Menu:")
        print("1. Add friend")
        print("2. Pick a nickname to start chatting")
        print("3. Previous menu")
        choice = input("Enter your choice: ")

        if choice == "1":
            friend_info = input("Enter friend's info (nickname, public key): ")
            add_friend(*friend_info.split(','))
        elif choice == "2":
            nickname = input("Enter the nickname: ")
            if get_friend(nickname):
                third_menu(nickname)
            else:
                print("This user is not your friend yet. Please add friend first.")
        elif choice == "3":
            return
        else:
            print("Invalid choice. Please try again.")

def third_menu(nickname):
    while True:
        print("\nChat with", nickname)
        print("Third Menu:")
        print("1. Send message")
        print("2. Update")
        print("3. Previous Menu")
        choice = input("Enter your choice: ")

        if choice == "1":
            message = input("Enter your message: ")
            send_message(nickname, message)
        elif choice == "2":
            update_chat_history(nickname)
        elif choice == "3":
            return
        else:
            print("Invalid choice. Please try again.")

def print_friends_list():
    friends = list_friends()
    for friend in friends:
        print(f"- {friend['nickname']}")

if __name__ == "__main__":
    main()
