import crypto_service as crypto
import page

pub, pri = crypto.generate_rsa_keys("123456")
pub_str = crypto.public_key_to_string(pub)
new_pub = crypto.string_to_public_key(pub_str)
crypto.write_keys_in_disk(new_pub, pri)
test_pub = crypto.load_public_key_from_disk()
test_pri = crypto.load_private_key_from_disk("123456")
print("Orignal Public Key", test_pub)
print("Orignal Private Key", test_pri)
print(type(new_pub))