from encryption import *
from db import *
from chain_operation import *
from page import *
import os
from message import *

# Check the public and private keys exist or not, if yes, load key. If not, ask user to create one
myPublicKey = ""
myPrivateKey = ""
if os.path.exists("private_key.pem") and os.path.exists("public_key.pem"):
    psw = input("Please input your password")
    myPublicKey = load_public_key()
    myPrivateKey = load_private_key(psw)

else:
    usrName = input("Please input your user name: ")
    psw = input("Please input your password")
    myPrivateKey, myPublicKey = create_keys(usrName, psw)


while True:
    userInputMainMenu = input("1. Send Message \n 2. Add Friend \n 3. Quit")

    # When user want to send message
    if userInputMainMenu == "1":
        usrInputNickname = input(f"Here are all of your friend, please pick one th chat with: {get_all_friends()}")
        friendInfo = get_friend(usrInputNickname)
        pubKey = friendInfo["public_key"]
        currentPage = friendInfo["current_page"]
        while True:
            userInputSecondMenu = input("1. Send Message \n 2. Update \n 3. Previous Menu")
            if userInputSecondMenu == "1":
                msg = input("")
                send_message(msg, usrInputNickname)
            elif userInputSecondMenu == "2":
                print("CHECK")
                print(get_update(usrInputNickname, psw))

            elif userInputSecondMenu == "3":
                break


    # Add Friend
    elif userInputMainMenu == "2":
        usrInputNickname = input("Please input the nick name")
        usrInputPubKey = input("Please input the public key")
        add_friend(usrInputPubKey, usrInputNickname)

    # Quit
    elif userInputMainMenu == "3":
        break

    # When user input an invalid number
    else:
        print("Not a valid choice")
        continue



