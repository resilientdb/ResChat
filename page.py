import numpy as np
import datetime
"""""
Page is the structure we are going to use transfer and save messages
"""""


class Page:
    def __init__(self):
        # Each page contains 20 messages
        """
        [Receiver's public key,
        message type,
        timestamp,
        message type extension,
        message1(encrypted by sender's pub key),
        message2(encrypted by receiver's pub key)], ... ]
        """
        self.msg = np.empty((20, 6), dtype=object)
        self.message_count = 0

    # Check if this page is full
    def is_full(self):
        return self.message_count >= 20

    # Add one message into the page
    def add_message(self, pub_key: str, msg_type: str, t_stamp: str, msg_type_ext: str, message1: str, message2: str):
        if self.is_full():
            print("The page is full. Cannot add more messages.")
            return
        else:
            self.msg[self.message_count] = [pub_key, msg_type, t_stamp, msg_type_ext, message1, message2]
            self.message_count += 1

    # Convert page to string for chain operation
    def to_string(self):
        page_string = ""
        for i in range(self.message_count):
            message = self.msg[i]
            message_string = "\n".join(map(str, message))
            page_string += message_string + "\n"

        return page_string

    # Sort the page base on timestamp
    def sort_by_time(self):
        sorted_indices = np.argsort(self.msg[:self.message_count, 2])
        self.msg[:self.message_count] = self.msg[sorted_indices]

    @classmethod
    def from_string(cls, page_string: str):
        page = cls()
        messages = page_string.strip().split("\n")
        for i in range(0, len(messages), 14):
            pub_key = "\n".join(messages[i:i + 9])
            msg_type = messages[i + 9]
            t_stamp = messages[i + 10]
            msg_type_ext = messages[i + 11]
            message1 = messages[i + 12]
            message2 = messages[i + 13]
            page.add_message(pub_key, msg_type, t_stamp, msg_type_ext, message1, message2)

        return page

    def all_messages(self) -> np.array:
        messages = np.empty((self.message_count, 6), dtype=object)
        for i in range(self.message_count):
            messages[i] = (self.msg[i])
        return messages