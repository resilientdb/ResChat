import numpy as np


class Page:
    def __init__(self, page_name: str):
        # Each page contains 20 messages
        """TODO: Find a proper page name that contains some shared things between two users"""
        self.pageName = page_name
        # [[Receiver's public key, message type, timestamp, message type extension, message], ... ]
        self.msg = np.empty((20, 5), dtype=object)
        self.message_count = 0

    # Check if this page is full
    def is_full(self):
        if self.message_count >= 20:
            return True
        else:
            return False

    # Add one message into the page
    def add_message(self, pub_key: str, msg_type: str, t_stamp: str, msg_type_ext: str, message: str):
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

    # Convert the string back to page for chain operation
    @classmethod
    def from_string(cls, page_string: str):
        lines = page_string.split('\n')
        page_name = lines[0]
        messages = lines[0:-1]
        new_page = cls(page_name)
        for message_string in messages:
            pub_key, msg_type, t_stamp, msg_type_ext, message = message_string.split(' ')
            new_page.add_message(pub_key, msg_type, t_stamp, msg_type_ext, message)
        return new_page


