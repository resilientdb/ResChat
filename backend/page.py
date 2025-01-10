from datetime import datetime
from pydoc import pager

import numpy as np
from RSDB_kv_service import set_kv, get_kv

"""
TODO: Test all these functions
"""
class Page:
    def __init__(self):
        """
        Page structure use to transmit and store chat history, and each message has 6 fields
        - Sender's RSA public key a string (sender_rsa_pub)
        - Message type a string, either "TEXT" or "FILE" (msg_type)
        - Time stamp a string (time_stamp)
        - AES encrypted message/file info (message)
            - file info:    {
                                "file_size": 12356(bytes),
                                "file_name": "test.txt",
                                "cid": 12345678,
                                TODO: might be more
                            }
        - Encrypted AES key by sender's RSA public key (encrypted_aes_key_sender)
        - Encrypted AES key by receiver's RSA public key (encrypted_aes_key_receiver)
        """
        self.message = np.empty((20, 6), dtype=object)
        self.message_count = 0

    def is_full(self):
        return self.message_count >= 20


    def add_message(self, sender_rsa_pub: str, msg_type: str, time_stamp: str,
                    message: str, encrypted_aes_key_sender, encrypted_aes_key_receiver):
        """
        This function will add one message into page, no matter it is a file or text, when passing the message parameter
        it should convert into string format (not Python dict)
        :return True: This message has been added successfully
        :return False: Current page is already full
        """

        if self.is_full():
            print("The page is full. Cannot add more messages.")
            return False
        else:
            self.message[self.message_count] = [sender_rsa_pub, msg_type, time_stamp, message,
                                                encrypted_aes_key_sender, encrypted_aes_key_receiver]

            self.message_count += 1
            return True

    def to_string(self):
        """
        Convert Page class to a string
        :return A string after conversion
        """
        page_string = ""
        for i in range(self.message_count):
            message = self.message[i]
            message_string = "\n".join(map(str, message))
            page_string += message_string + "\n"
        return page_string


    def all_messages(self) -> np.array:
        """获取页面上的所有消息"""
        messages = np.empty((self.message_count, 6), dtype=object)
        for i in range(self.message_count):
            messages[i] = (self.message[i])
        return messages


    def sort_by_time(self):
        """
        Sort messages in the current Page object by their timestamp (ascending).
        """
        sorted_indices = np.argsort(self.message[:self.message_count, 2])
        self.message[:self.message_count] = self.message[sorted_indices]


def from_string(page_string: str) -> Page:
    res_page = Page()
    messages = page_string.strip().split("\n")
    for i in range(0, len(messages), 14):
        sender_rsa_pub = "\n".join(messages[i:i + 9])
        msg_type = messages[i + 9]
        t_stamp = messages[i + 10]
        message = messages[i + 11]
        encrypted_aes_key_sender = messages[i + 12]
        encrypted_aes_key_receiver = messages[i + 13]
        res_page.add_message(sender_rsa_pub, msg_type, t_stamp, message,
                         encrypted_aes_key_sender, encrypted_aes_key_receiver)
    return res_page


