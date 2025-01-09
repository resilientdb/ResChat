import crypto_service as crypto
import page

pub, pri = crypto.generate_rsa_keys("123456")
pub_str = crypto.public_key_to_string(pub)
new_pub = crypto.string_to_public_key(pub_str)
print(type(pri))