import binascii
import sys
import unittest
from tempfile import NamedTemporaryFile
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import os
import psutil
sys.path.append("bazel/bazel-out/k8-fastbuild/bin/aes_encryption/")
from pybind_aes import aes_file_encrypt, aes_file_decrypt, aes_key_generate, aes_text_encrypt, aes_text_decrypt




def generate_aes_key() -> str:
    return aes_key_generate()



# Internal function
def public_key_to_string(pub_key):
    """Convert an RSA public key type to string"""
    return pub_key.exportKey(format='PEM').decode('utf-8')



# Internal function
def string_to_public_key(pub_key_string):
    """Convert a string to an RSA public key"""
    return RSA.importKey(pub_key_string.encode('utf-8'))



def encrypt_text_with_aes(plain_text: str) -> [str, str]:
    """
    使用AES加密纯文字
    返回随机生成的AES key和加密过后的字符串
    """
    key = generate_aes_key()
    return key, aes_text_encrypt(plain_text, key)



def decrypt_text_with_aes(cipher_text: str, key: str):
    """
    使用AES解密纯文字
    返回解密过后的文字
    """
    return aes_text_decrypt(cipher_text, key)



def encrypt_file_with_aes(file_path: str) -> str:
    """
    使用AES加密文件
    成功返回AES key
    文件不存在返回1
    内存空间不够返回2
    加密失败返回3
    """
    memory_info = psutil.virtual_memory()
    free_memory = memory_info.available  # 获取可用内存（以字节为单位）
    file_size = os.path.getsize(file_path)
    if not os.path.exists(file_path):
        return "1"
    if free_memory <= file_size:
        return "2"
    else:
        key = generate_aes_key()
        if aes_file_encrypt(file_path, key):
            return key
        else:
            return "3"



def decrypt_file_with_aes(encrypted_file_path: str, save_path: str, key: str) -> str:
    """
    使用AES解密文件
    解密成功返回0
    加密文件不存在返回1
    解密失败返回2
    """
    if not os.path.exists(encrypted_file_path):
        return "1"
    if aes_file_decrypt(encrypted_file_path, save_path, key):
        return "0"
    else:
        return "2"



# Internal function
def encrypt_aes_key_with_rsa(aes_key: str or bytes, public_key):
    """
    使用RSA公钥加密加密AES key
    返回加密后的AES key
    """
    if type(aes_key) == str:
        aes_key = aes_key.encode('utf-8')
    cipher_rsa = PKCS1_OAEP.new(public_key)
    encrypted_aes_key = cipher_rsa.encrypt(aes_key)
    return binascii.hexlify(encrypted_aes_key).decode('ascii')



# Internal function
def decrypt_aes_key_with_rsa(encrypted_aes_key, private_key) -> str:
    """
    使用RSA私钥解密AES key
    返回解密后的AES key
    """
    encrypted_aes_key = binascii.unhexlify(encrypted_aes_key)
    cipher_rsa = PKCS1_OAEP.new(private_key)
    aes_key = cipher_rsa.decrypt(encrypted_aes_key)
    return aes_key.decode('utf-8')  # 确保返回解码后的字符串


def encrypt_message_for_two_recipients(plain_text: str or bytes, public_key_sender , public_key_receiver):
    """
    使用两个用户双方的RSA公钥来加密一条消息
    返回一个List [encrypted message,
                encrypted AES key by sender's RSA public key,
                encrypted AES key by receiver's RSA public key]
    """
    if isinstance(plain_text, str):
        plain_text = plain_text.encode('utf-8')

    aes_key, encrypted_message = encrypt_text_with_aes(plain_text)
    encrypted_aes_key_sender = encrypt_aes_key_with_rsa(aes_key, public_key_sender)
    encrypted_aes_key_receiver = encrypt_aes_key_with_rsa(aes_key, public_key_receiver)

    return encrypted_message, encrypted_aes_key_sender, encrypted_aes_key_receiver



def decrypt_message(encrypted_message: str, encrypted_aes_key, private_key):
    """
    使用RSA私钥解密AES key，并使用该AES key解密消息
    返回解密后的消息
    """
    aes_key = decrypt_aes_key_with_rsa(encrypted_aes_key, private_key)
    decrypted_data = decrypt_text_with_aes(encrypted_message, aes_key)
    return decrypted_data  # 去除 .decode('utf-8')

class TestEncryptionFunctions(unittest.TestCase):

    def test_aes_text_encryption_decryption(self):
        plain_text = "这是一条测试信息！"

        # 使用AES加密纯文本
        aes_key = generate_aes_key()
        encrypted_text = aes_text_encrypt(plain_text, aes_key)

        # 使用AES解密纯文本
        decrypted_text = aes_text_decrypt(encrypted_text, aes_key)

        # 验证解密结果
        self.assertEqual(decrypted_text, plain_text)

    def test_aes_file_encryption_decryption(self):
        # 创建一个临时文件
        with NamedTemporaryFile(delete=False) as temp_file:
            # 将中文字符串编码为 UTF-8 字节
            temp_file.write("这是一个测试文件。".encode('utf-8'))
            temp_file_path = temp_file.name

        # 使用AES加密文件
        aes_key = encrypt_file_with_aes(temp_file_path)

        # 验证AES密钥生成成功
        self.assertNotEqual(aes_key, "1")
        self.assertNotEqual(aes_key, "2")
        self.assertNotEqual(aes_key, "3")

        # 搜索 temp 文件夹中的加密文件
        # temp_folder = os.path.join(os.path.dirname(temp_file_path), "temp")
        temp_folder = "temp/"
        encrypted_file_path = None

        # 遍历 temp 文件夹，找到加密后的文件
        for file_name in os.listdir(temp_folder):
            if file_name.endswith(".enc"):
                encrypted_file_path = os.path.join(temp_folder, file_name)
                break

        # 确保找到加密后的文件
        self.assertIsNotNone(encrypted_file_path, "未找到加密文件")

        # 创建解密后的保存路径
        decrypted_file_path = temp_file_path + ".dec"

        # 使用AES解密文件
        decrypt_status = decrypt_file_with_aes(encrypted_file_path, decrypted_file_path, aes_key)

        # 验证解密状态
        self.assertEqual(decrypt_status, "0")

        # 比较原文件和解密后的文件内容
        with open(temp_file_path, 'rb') as original, open(decrypted_file_path, 'rb') as decrypted:
            self.assertEqual(original.read(), decrypted.read())

        # 清理临时文件
        os.remove(temp_file_path)
        os.remove(decrypted_file_path)
        os.remove("temp/" + os.path.basename(temp_file_path) + ".enc")

if __name__ == '__main__':
    unittest.main()