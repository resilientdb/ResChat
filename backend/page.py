import json



class Page:
    """
    Page
    key = index(int)
    value = {}(dict)
    One page includes 20 messages, and each message is constructed as:
    - Receiver's RSA public key (rsa_pub_key)
    - Message Type (msg_type)
    - Time stamp (t_stamp)
    - File location key (file_location_key)
    - Encrypted message (message)
    - Encrypted AES key with sender's RSA public key (encrypted_aes_key_sender)
    - Encrypted AES key with receiver's RSA public key (encrypted_aes_key_receiver)

    """
    def __init__(self):
        self.msg = {}
        self.message_count = 0

    def is_full(self) -> bool:
        return self.message_count >= 20


    def add_message(self,
                    rsa_pub_key: str,
                    msg_type: str,
                    t_stamp: str,
                    file_location_key: str,
                    encrypted_message: str,
                    encrypted_aes_key_sender: str,
                    encrypted_aes_key_receiver: str) -> bool:
        if self.is_full():
            return False
        else:
            tmp = {"rsa_pub_key": rsa_pub_key,
                   "msg_type": msg_type,
                   "t_stamp": t_stamp,
                   "file_location_key": file_location_key,
                   "encrypted_message": encrypted_message,
                   "encrypted_aes_key_sender": encrypted_aes_key_sender,
                   "encrypted_aes_key_receiver": encrypted_aes_key_receiver}

            self.msg[self.message_count] = tmp
            self.message_count += 1
            return True



    def to_string(self) -> str:
        """将page类转换为string类"""
        return json.dumps(self.msg)

    @classmethod
    def from_string(cls, page_string: str):
        """从string类构建page"""
        page = cls()
        # 将 JSON 字符串反序列化
        msg_dict = json.loads(page_string)
        # 将字典键从字符串转换回整数
        page.msg = {int(k): v for k, v in msg_dict.items()}
        page.message_count = len(page.msg)
        return page


    def sort_by_time(self):
        """根据时间戳对页面上的消息进行排序"""
        # 对消息按照时间戳（t_stamp）排序，但保持原始数据类型不变
        sorted_items = sorted(self.msg.items(), key=lambda x: x[1]['t_stamp'])
        # 更新排序后的消息，同时保持消息的索引一致
        self.msg = {index: item[1] for index, item in enumerate(sorted_items)}



