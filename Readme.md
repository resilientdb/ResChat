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
bazel-bin/service/tools/kv/api_tools/kv_service_tools scripts/deploy/config_out/client.config {set/get} "{PAGE NAME} {PAGE NUM}" "{PAGE STRING}"
- PAGE:
  - Page structure: [[Receiver's public key, message type, timestamp, message type extension, message], ... ]
  - MESSAGE TYPE:
    - TEXT: Plain text message, MESSAGE TYPE EXTENSION: none, MESSAGE: String
    - FILE: File, MESSAGE TYPE EXTENSION: Filename with extension, MESSAGE: File converted to a binary string
  - TIMESTAMP: Timestamp when this message is sent
- MESSAGE:
  - Messages are stored in a class called Page
  - Each Page contains 20 chat histories
  - Sender and receiver will obtain some shared Pages
  - When it reaches to 20 messages, sender of the 21th message will create a new page
  - When user want to send message, sender will first get current page from the chain, sort the page based on timestamp. Then, write the message this user want to send, and set this page on the chain
  - When user want to read message, receiver will get current page from the chain, and read the page
    - If the current page is full, receiver will automatically try to get next page({PAGE_NAME}{PAGE_NUM + 1}). If there is nothing on next page, it will be all set, if there is a next page, receiver will update local page number(plus one)
  - System default will contain two pages at the same time, user can load previous pages(chatting history)
  - In this way, sender and receiver's chat history will all on the chain. Also, it can handle when receiver is offline.

