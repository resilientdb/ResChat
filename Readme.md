# Decentralized chat system based on ResilientDB
## Project description
### Overview
In today's life, when we try to send a message on most chat software,
the message will first be sent to the central server, 
and then forwarded to the target user by the central server. 
The disadvantage of this is that all data will be captured and stored by the central server, 
which greatly increases the risk of data leakage and leakage of private information. 
Now, we will create a decentralized chat system based on the ResilientDB blockchain. 
This decentralized chat system does not store any personal information, 
and only the sender and recipient can encrypt and decrypt the message during the transmission of the message.

### Key Features
1. **Decentralized Architecture:** Our system avoids the need for a central server. 
All messages are transmitted through ResilientDB blockchain.

2. **Security:** By using the asymmetric encryption algorithm (gpg), 
we can ensure that information cannot be easily cracked during blockchain transmission. 
Only the sender and recipient of the message can use their keys to encrypt and decrypt

3. **Privacy-first Approach:** User data is never stored on any central server. No chat history will be stored.

4. **Open-source:** To ensure utmost transparency and security, our system is fully open-source, allowing community participation and review.

### Potential Use Cases
<!-- TODO -->

### Conclusion
<!-- TODO -->

## Schedule

1. **Oct, 20:**
   1. Finish project proposal
   2. Decide which language to use(Python or C++)
   3. Understand SDK API
2. **Nov, 3:**
   1. Finish the basic chatting system(User can send and receive messages)
3. **Nov, 17**
   1. Basic GUI finished
   2. Improve fault tolerance on the chatting system
   3. User can send images(OPTIONAL)
   4. User can use group chat(OPTIONAL)
4. **Dec, 8**
    1. User can send images(if not finished in last milestone)
    2. User can use group chat(OPTIONAL)
    3. GUI finished

## Process
1. Command Line: bazel-bin/service/tools/kv/api_tools/kv_service_tools scripts/deploy/config_out/client.config set {RECEIVER'S PUBLIC KEY} "{MESSAGE TYPE} {TIMESTAMP} {MESSAGE TYPE EXTENSION} {MESSAGE}"
2. Message Type:
   1. FRIEND: This means this message is a friend request; MESSAGE TYPE EXTENSION: None; MESSAGE: Sender's public key
   2. REFRIEND: This means this message is a reply of friend request; MESSAGE TYPE EXTENSION: YES/NO; MESSAGE: Sender's public key(if YES). Null (if NO)
   3. TEXT: This means this message is a pure text message; MESSAGE TYPE EXTENSION: None; MESSAGE: text string
   4. FILE: This means this message is an file; MESSAGE TYPE EXTENSION: file name; MESSAGE: Binary string of this file.
3. After two users added each other as friend, they will save other user's public key on their local machine.
4. All MESSAGE will encrypt by sender's public key
5. Each user will keep reading from the chain by: bazel-bin/service/tools/kv/api_tools/kv_service_tools scripts/deploy/config_out/client.config get [RECEIVER'S PUBLIC KEY]
6. When They successfully get the message, this message will firstly be stored in local machine, then decrypt this message by receiver's private key and corresponding message type.
7. After successfully receive the message, receiver will: bazel-bin/service/tools/kv/api_tools/kv_service_tools scripts/deploy/config_out/client.config set [RECEIVER'S PUBLIC KEY] null
8. After sender send the message, sender will keep reading the chain too, as soon as sender got the null value, sender will know this message has already read by receiver
