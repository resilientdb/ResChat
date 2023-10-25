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
   1. Finish the detail process of this project
   2. Start working on backend code
3. **Nov, 17**
   1. Basic GUI finished
   2. Backend coding finished
   3. Improve fault tolerance on the chatting system

4. **Dec, 8**
   1. GUI finished
   2. Finish README.md file

## Process
- Command Line:
bazel-bin/service/tools/kv/api_tools/kv_service_tools scripts/deploy/config_out/client.config {set/get} {RECEIVER'S PUBLIC KEY} "{MESSAGE TYPE} {TIMESTAMP} {MESSAGE TYPE EXTENSION} {MESSAGE}"

- MESSAGE TYPE:
  - FRIEND: Friend request, MESSAGE TYPE EXTENTION: none, MESSAGE: Public key of the user sending the friend request
  - REFRIEND: Reply to a friend request, MESSAGE TYPE EXTENSION: Yes/No, MESSAGE: Public key of the user sending this message (Yes if accepting the request)
  - TEXT: Plain text message, MESSAGE TYPE EXTENSION: none, MESSAGE: String
  - FILE: File, MESSAGE TYPE EXTENSION: Filename with extension, MESSAGE: File converted to a binary string
  - TIMESTAMP: Timestamp when this message is sent

- Steps:
  - When user A wants to send a message to user B, A will first send a friend request to B
  - When B receives this friend request, B will store A's public key in the local database and send its own public key to B (if B chooses to accept the friend request)
  - Now both A and B have each other's public keys stored locally
  - When A sends a message to B, this message will be encrypted using B's public key
  - B and A will continuously use their own public keys to read the chain. When B reads a message sent to itself, it will store this message in the local database and then decrypt it using its own private key
  - When B receives a message, it will set this message as null
  - After A sends out a message, it will continuously monitor this message. If the value becomes null, it means B has successfully read the message

- User Offline Scenarios:
  - Assume A wants to send a message to B, but B is offline. This message will be placed in the send queue and wait
  - Assume there are already some messages in the queue, and B has not come online, and A is also going offline. At this time, A will set a special message. This message contains the entire send queue (the send queue contains the command line instructions already written)
  - All online clients will try to read a common key. When another client (C) reads A's queue information, it will set this information as null (already read)
  - Afterward, C will continue to try sending messages to B. If B is online and starts to receive messages, then C will pop the messages that B already received from queue
  - When C is ready to go offline, it will repeat the above steps

- Threads:
  - Thread #1: This thread will continuously use its own public key to read the chain
  - Thread #2: When a message is received, put it in the queue, then store it locally from the queue and decrypt it
  - Thread #3: When sending a message, the sender will activate this thread to check whether the receiver has successfully received the message
  - Thread #4: Send messages
  - Thread #5: Read public information (user offline scenarios)
  - Thread #6: Read acknowledgement of public information (user offline scenarios)

- Queues:
  - Send queue: This queue will store commandline instructions to send message
  - Receive queue: This queue will store messages get from the chain



