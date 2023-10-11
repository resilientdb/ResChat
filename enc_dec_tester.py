from enc_dec import get_mac, PBKDF2_encrypt, aes_encrypt, aes_decrypt

# 获取MAC地址
mac_address = get_mac()
print(f"MAC address: {mac_address}")

# 使用 PBKDF2 派生密钥
key = PBKDF2_encrypt(mac_address)
print(f"Encrypted MAC address: {key}")

# 使用派生的密钥来加密字符串 "Hello world"
data = "I am a student in UC Davis"
iv, encrypted_data = aes_encrypt(data, key)
print(f"Original Data: {data}")
print(f"Encrypted Data: {encrypted_data}")

# 解密数据
decrypted_data = aes_decrypt(iv, encrypted_data, key)
print(f"Decrypted Data: {decrypted_data}")