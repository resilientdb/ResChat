import datetime
import json

import gnupg, os
# !/usr/bin/python

import sqlite3
import hashlib
import base64


class DB:
    def __init__(self):
        self.conn = sqlite3.connect('user.db')

    def get(self, key):
        fin = open('db.json', 'r')
        db = json.load(fin)
        return db[key]

    def set(self, key, value):
        fout = open('db.json', 'rw')
        db = json.load(fout)
        db[key] = value
        json.dump(db, fout)

    def close(self):
        self.conn.commit()
        self.conn.close()


class Local_client:
    def __init__(self):
        self.gpg = gnupg.GPG()
        self.db = DB()
        self.user_name = 'None'
        self.email = "None"

    # check user login status
    def login(self, email, password):
        # access SQLite DB and USER table
        cur = self.db.conn.cursor()
        cursor = cur.execute(f'SELECT name, email, password from USER WHERE EMAIL = {email}')

        # check is username and password are correct
        for row in cursor:
            if row and row[1] == email and row[2] == hashlib.sha256(password):
                self.user_name = row[0]
                self.email = row[1]
                print(f"Welcome User {self.user_name}")
                return
        print("Login Failed!")

    #
    def add_friend(self, email):

        # get friend's pub_key from shared DB
        pub_key = self.db.get(email + '.pub')
        if not pub_key:
            print("No such a User!")
            return False

        # persist the mapping between local_user and remote_user
        cur = self.db.conn.cursor()
        cursor = cur.execute(
            f'SELECT local_email, friend_email, friend_pub_key from RELATIONSHIP WHERE local_email = {self.email} and friend_email = {email}')
        if cursor:
            print('You are already friends!')
            return
        cur.execute(
            f"INSERT INTO RELATIONSHIP (LOCAL_EMAIL, FRIEND_EMAIL, FRIEND_PUB_KEY) VALUES ( {self.email}, {email}, {pub_key} )")

    # send message from local_user to remote_user
    def send_message(self, local, remote, msg):
        cur_msg = self.db.get(local + '-' + remote + '.msg')
        self.db.set(local + '-' + remote + '.msg',
                    cur_msg + str(datetime.datetime.now()) + ',' + self.gpg.encrypt(msg, remote) + ';')

    # receive message
    def receive_message(self, sender, receiver, ):
        cur_msg = self.db.get(receiver + '-' + sender + '.msg')


    # create a new user include:
    # create key pair
    def create_user(self, user_name, email, password):
        mate_data = {'name_real': user_name,
                     'name_email': email,
                     'expire_date': '2029-04-01',
                     'key_type': 'RSA',
                     'key_length': 1024,
                     'key_usage': '',
                     'subkey_type': 'RSA',
                     'subkey_length': 1024,
                     'subkey_usage': 'encrypt,sign,auth',
                     'passphrase': password}
        input_data = self.gpg.gen_key_input(**mate_data)
        key = self.gpg.gen_key(input_data)
        public_key = self.gpg.export_keys(keyids=email, secret=False)
        private_key = self.gpg.export_keys(keyids=email, secret=True, passphrase=password)
        with open(email + '.pub', 'w') as file:
            file.write(public_key)
        with open(email + '.pri', 'w') as file:
            file.write(private_key)
        # store pub_key of current user in shared DB
        self.db.set(email + '.pub', public_key)
        self.user_name = user_name
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
