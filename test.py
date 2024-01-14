from kv_operation import send_message
from kv_operation import get_message

import hashlib

def hash_with_sha256(input_string):
    # 创建一个新的sha256哈希对象
    sha_signature = hashlib.sha256(input_string.encode()).hexdigest()
    return sha_signature

# 使用示例
input_string = "your_password_here"
hashed_string = hash_with_sha256(input_string)
print("原始字符串:", input_string)
print("SHA-256哈希值:", hashed_string)
