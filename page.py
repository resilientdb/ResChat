import numpy as np
import datetime
"""""
Page is the structure we are going to use transfer and save messages
"""""


class Page:
    def __init__(self):
        # Each page contains 20 messages
        # [[Receiver's public key, message type, timestamp, message type extension, message], ... ]
        self.msg = np.empty((20, 5), dtype=object)
        self.message_count = 0

    # Check if this page is full
    def is_full(self):
        return self.message_count >= 20

    # Add one message into the page
    def add_message(self, pub_key: str, msg_type: str, t_stamp: datetime.datetime, msg_type_ext: str, message: str):
        if self.is_full():
            print("The page is full. Cannot add more messages.")
            return
        else:
            self.msg[self.message_count] = [pub_key, msg_type, t_stamp, msg_type_ext, message]
            self.message_count += 1

    # Convert page to string for chain operation
    def to_string(self):
        page_string = ""
        for i in range(self.message_count):
            message = self.msg[i]
            message_string = " ".join(map(str, message))
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
        for message in messages:
            pub_key, msg_type, t_stamp_day, t_stamp_sec, msg_type_ext, message = message.split(" ")
            t_stamp = datetime.datetime.strptime(t_stamp_day + " " + t_stamp_sec, '%Y-%m-%d %H:%M:%S.%f')
            page.add_message(pub_key, msg_type, t_stamp, msg_type_ext, message)
        return page
