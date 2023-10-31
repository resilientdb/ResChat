from encryption import *
from db import *
from chain_operation import *
from page import *
import os

pub_key = ""
pri_key = ""
if os.path.exists("private_key.pem") and os.path.exists("public_key.pem"):
    pub_key = load_public_key()
    pri_key = load_private_key()
else:
    usrName = input("Please input your user name: ")
    psw = input("Please input your password")
    pri_key, pub_key = create_keys(usrName, psw)


while True:
    userInput = input("1. Add Friend \n 2. Chat with Friend \n 3. Quit")
    if userInput == '1':
        friendNickName = input("Please input your friend's nick name")
        friendPublicKey = input("Please input your friend's public key")
        add_friend(friendPublicKey, friendNickName)
        print(f"You successfully add {friendNickName} as friend.")
        continue
    elif userInput == '2':
        friendList = get_all_friends()
        if len(friendList) == 0:
            print("You dont have any friends yet, please add friend")
            continue
        else:
            print("Here is your friends")
            for friend in friendList:
                print(friend + " ")
            chatFriendName = input("Please pick who you want to chat with")
            friendDic = get_friend(chatFriendName)
            friendPubKey = friendDic["public_key"]
            currentPage = friendDic["current_page"]
            while True:
                userInput2 = input("1. Send message 2. Update chat history")
                pageName = sorted([pub_key, friendPubKey])
                pageNameString = "_".join(pageName)
                if userInput2 == 1:
                    msgType = input("1. Message 2. File")
                    if msgType == 1:
                        msg = input("Please input your message: ")
                        pageString = get_page(pageNameString, currentPage)
                        page = from_string()
                    elif msgType == 2:

                elif userInput2 == 2:


    elif userInput == '3':
        break
    else:
        print("Not a valid choice")
        continue


