import json



class Page:
    """
    Page 结构用于存储和传输加密消息。
    key = index(int)
    value = {}(dict)
    每个 Page 包含多个消息，每个消息由以下部分组成:
    - 接收方的公钥 (rsa_pub_key)
    - 消息类型 (msg_type)
    - 时间戳 (t_stamp)
    - 文件所存放的key (file_location_key)
    - 加密消息本身 (message)
    - 用发送方公钥加密的AES密钥 (encrypted_aes_key_sender)
    - 用接收方公钥加密的AES密钥 (encrypted_aes_key_receiver)

    每个 Page 可以存储的消息数量是固定的（例如，20条消息）。
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

        """
        向页面中添加一条消息
        成功返回true
        失败返回false
        """
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



