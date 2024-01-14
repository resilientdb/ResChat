import encryption as enc
import kv_operation as kv
import file_operation as f

# print(kv.get_message("a"))

# enc.create_user("a", "123456")

# kv.send_message("a", "")

username, password, public_key, private_key = enc.load_user("a", "123456")
# test_msg = "this is a test"
#
# # 加密
# encrypted_msg, encrypted_aes_key = enc.encrypt_message(test_msg, public_key)
#
# # 解密
# decrypted_msg = enc.decrypt_message(encrypted_msg, encrypted_aes_key, private_key)
# print(decrypted_msg)

test_img_path = "test_img.jpeg"
test_img_str = f.read_file(test_img_path)
enc_test_img_str, encrypted_aes_key_sender, encrypted_aes_key_receiver = enc.encrypt_message_for_two_recipients(test_img_str, public_key, public_key)
decrypted_msg = enc.decrypt_message(enc_test_img_str, encrypted_aes_key_receiver, private_key)
f.write_file("test_img1.jpeg", decrypted_msg)

