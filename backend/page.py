import numpy as np
from kv_operation import send_message, get_message


class Page:
    """
    Page 结构用于存储和传输加密消息。
    每个 Page 包含多个消息，每个消息由以下部分组成:
    - 接收方的公钥 (pub_key)
    - 消息类型 (msg_type)
    - 时间戳 (t_stamp)
    - 消息类型的扩展 (msg_type_ext)
    - 加密消息本身 (message)
    - 用发送方公钥加密的AES密钥 (encrypted_aes_key_sender)
    - 用接收方公钥加密的AES密钥 (encrypted_aes_key_receiver)

    每个 Page 可以存储的消息数量是固定的（例如，20条消息）。
    """

    def __init__(self):
        # 每个页面包含20条消息，每条消息有7个部分
        self.msg = np.empty((20, 7), dtype=object)
        self.message_count = 0

    def is_full(self):
        """检查此页面是否已满"""
        return self.message_count >= 20

    def add_message(self, pub_key: str, msg_type: str, t_stamp: str, msg_type_ext: str, message: str,
                    encrypted_aes_key_sender: str, encrypted_aes_key_receiver: str):
        """向页面添加一条消息"""
        if self.is_full():
            print("The page is full. Cannot add more messages.")
            return
        else:
            self.msg[self.message_count] = [pub_key, msg_type, t_stamp, msg_type_ext, message, encrypted_aes_key_sender,
                                            encrypted_aes_key_receiver]
            self.message_count += 1

    def to_string(self):
        """将页面转换为字符串以便于传输或存储"""
        page_string = ""
        for i in range(self.message_count):
            message = self.msg[i]
            message_string = "\n".join(map(str, message))
            page_string += message_string + "\n"
        return page_string

    def sort_by_time(self):
        """根据时间戳对页面上的消息进行排序"""
        sorted_indices = np.argsort(self.msg[:self.message_count, 2])
        self.msg[:self.message_count] = self.msg[sorted_indices]

    @classmethod
    def from_string(cls, page_string: str):
        """从字符串创建 Page 对象"""
        page = cls()
        messages = page_string.strip().split("\n")
        for i in range(0, len(messages), 15):
            # print(f"i: {i}")
            pub_key = "\n".join(messages[i:i + 9])
            msg_type = messages[i + 9]
            t_stamp = messages[i + 10]
            msg_type_ext = messages[i + 11]
            message = messages[i + 12]
            encrypted_aes_key_sender = messages[i + 13]
            encrypted_aes_key_receiver = messages[i + 14]
            page.add_message(pub_key, msg_type, t_stamp, msg_type_ext, message, encrypted_aes_key_sender,
                             encrypted_aes_key_receiver)

        return page

    def all_messages(self) -> np.array:
        """获取页面上的所有消息"""
        messages = np.empty((self.message_count, 7), dtype=object)
        for i in range(self.message_count):
            messages[i] = (self.msg[i])
        return messages
