from encryption import *
from db import *
from chain_operation import *
from page import *
import os

# Check the public and private keys exist or not, if yes, load key. If not, ask user to create one
myPublicKey = ""
myPrivateKey = ""
if os.path.exists("private_key.pem") and os.path.exists("public_key.pem"):
    myPublicKey = load_public_key()
    myPrivateKey = load_private_key()
else:
    usrName = input("Please input your user name: ")
    psw = input("Please input your password")
    myPrivateKey, myPublicKey = create_keys(usrName, psw)


while True:
    userInputMainMenu = input("1. Send Message \n 2. Quit")

    # When user want to send message
    if userInputMainMenu == "1":
        """TODO: Finish it"""

    # exit the program
    elif userInputMainMenu == "2":
        break

    # When user input an invalid number
    else:
        print("Not a valid choice")
        continue



