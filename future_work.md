# 1. Enable delete friend feature
    1. Front-end -> Back-end: Friend nickname to be delated
    2. Backend:Modifyin RAM friendlist
    3. Set updated version to ResilientDB
# 2. Enable add friend request feature
    1. Assume user A with username aaa, B with username bbb, A sends a friend request to B
    2. Add a key for everyone `A REQUEST_RECEIVED`
    3. This key stores a dictionary to represent all the friend request this user received `{B: B's_PUBLIC_KEY}` this value will not be encrypted
    4. Add another key for everyone `B REQUEST_SENT`
    5. This key will store all the friend request being sent `{A: {public_key: A's_PUBLIC_KEY, status: PENDING/APPROVED/DENILED}}`
    6. After Areceived the friend request, there are three status pending, approved and deniled
    7. Pending: A didn`t make any actions on this request
    8. Approved: A will delete this friend request in `A REQUEST_RECEIVED` and modify `B REQUEST_SENT`'s value fron `{A: {public_key: A's_PUBLIC_KEY, status: PENDING}}` to {A: {public_key: A's_PUBLIC_KEY, status: APPROVED}}. Then, A put B's information into A's friendlist. When B is online, he will first check `B REQUEST_SENT`. Then he finds out A approved this request, then B will delete the `{A: {public_key: A's_PUBLIC_KEY, status: APPROVED}` and add A into B's friendlist
    9. Deniled: Same as above. When B is online and checked the key, he will see `{A: {public_key: A's_PUBLIC_KEY, status: DENILED}`. Then on B's side it will appears friend request deniled and delete this message.
# 4. Enable file transfer feature
    1. Same as two user A and B
    2. If A wants to send a file to B, there are two options, encrypt or don't encrypt
    3. If don't encrypt, this file will be sent to IPFS as a whole file, when file transfer process started, and let's assume this is the first file that being transfered to B the key is `A B FILE 1`, the value is `{fileHash: [FILE_HASH_0], key: NONE, status: PENDING/FINISHED}`. At the same time A will add a message to current page `{}`
    TODO

    
