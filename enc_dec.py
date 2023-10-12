import gnupg, os


class Local_client:
    def __init__(self):
        self.gpg = gnupg.GPG()

    def create_user(self, user_name, email, password):
        alice = {'name_real': user_name,
                 'name_email': email,
                 'expire_date': '2029-04-01',
                 'key_type': 'RSA',
                 'key_length': 1024,
                 'key_usage': '',
                 'subkey_type': 'RSA',
                 'subkey_length': 1024,
                 'subkey_usage': 'encrypt,sign,auth',
                 'passphrase': password}
        input_data = self.gpg.gen_key_input(**alice)
        key = self.gpg.gen_key(input_data)
        public_key = self.gpg.export_keys(keyids=email, secret=False)
        private_key = self.gpg.export_keys(keyids=email, secret=True, passphrase=password)
        with open("public_key.txt", 'w') as file:
             file.write(public_key)
        with open("private_key.txt", 'w') as file:
             file.write(private_key)
        return public_key, private_key


if __name__ == '__main__':
    l = Local_client()
    public, private = l.create_user('kenny', 'kny@gmail.com', '123')

    plaintext = "This is a secret message"
    encrypted_data = l.gpg.encrypt(plaintext, 'kny@gmail.com')
    encrypted_string = str(encrypted_data)
    print(f"Encrypted string: {encrypted_string}")

    decrypted_data = l.gpg.decrypt(message=encrypted_string)
    print(decrypted_data)

