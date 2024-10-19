from kv_operation import get_message, send_message
import json
import os
from ipfs import get_file_ipfs, send_file_ipfs

"""
friend list structure 
{
    "USERNAME1": {
                    "nickname": "NICKNAME",
                    "public_key": "PUBLIC KEY",
                    "profile_pic_hash": "PROFILE PICTURE HASH",
                    "profile_pic_name": "PROFILE PICTURE NAME",
                },
}
"""


def initial_load_friend_list(username: str) -> dict:
    # Retrieve friend list
    friend_list = json.loads(get_message(username + " FRIEND_LIST"))

    for friend_username, friend_info in friend_list.items():
        profile_pic_hash, profile_pic_ext = (get_message(friend_username + " PROFILE_PICTURE")).split(" ")

        # Check the "profile_pic_hash" and "profile_pic_name" in friend_info
        if (profile_pic_hash == friend_info["profile_pic_hash"] and
                profile_pic_hash + profile_pic_ext == friend_info["profile_pic_name"]):
            # If the image file already exists locally, skip the download
            if os.path.exists("profile_pics/" + friend_info["profile_pic_name"]):
                continue
            else:
                # Download and rename the file
                get_file_ipfs("profile_pics/", profile_pic_hash)
                os.rename("profile_pics/" + profile_pic_hash, "profile_pics/" + profile_pic_hash + profile_pic_ext)
        else:
            # Update the hash and picture name in friend_info
            friend_info["profile_pic_hash"] = profile_pic_hash
            friend_info["profile_pic_name"] = profile_pic_hash + profile_pic_ext

            # If the image file already exists locally, skip the download
            if os.path.exists("profile_pics/" + friend_info["profile_pic_name"]):
                continue
            else:
                # Download and rename the file
                get_file_ipfs("profile_pics/", profile_pic_hash)
                os.rename("profile_pics/" + profile_pic_hash, "profile_pics/" + profile_pic_hash + profile_pic_ext)

    send_message(username + " FRIEND_LIST", json.dumps(friend_list))
    return friend_list


def change_nickname(target_username: str, my_username: str, new_nickname: str, friend_list: dict) -> dict:
    friend_list[target_username]["nickname"] = new_nickname
    send_message(my_username + " FRIEND_LIST", json.dumps(friend_list))
    return friend_list

def delete_friend(target_username: str, my_username: str, friend_list: dict) -> dict:
    del friend_list[target_username]
    send_message(my_username + " FRIEND_LIST", json.dumps(friend_list))
    # TODO: Need to add DELETE action in the page to notify the other party that they have been deleted
    return friend_list


def add_friend(target_username: str, my_username: str, message: str, my_friend_list: dict) -> dict:
    if target_username in my_friend_list:
        return {"result": False, "message": f"{target_username} is already your friend"}

    if len(message) > 50:
        return {"result": False, "message": "Your message is too long"}

    my_request_list = json.loads(get_message(my_username + " REQUEST_SENT"))
    if target_username in my_request_list and my_request_list[target_username]["status"] == "PENDING":
        return {"result": False, "message": f"You already sent a friend request to {target_username}, please wait for the response"}

    my_request_list[target_username] = {"status": "PENDING", "message": message}
    send_message(my_username + " REQUEST_SENT", json.dumps(my_request_list))

    target_receive_list = json.loads(get_message(target_username + " REQUEST_RECEIVED"))
    target_receive_list[my_username] = {"message": message}
    send_message(target_username + " REQUEST_RECEIVED", json.dumps(target_receive_list))
    return {"result": True, "message": f"You have sent a friend request to {target_username} successfully"}


def make_friend_decision(target_username: str, my_username: str, my_friend_list: dict, accept: bool) -> dict:
    my_receive_list = json.loads(get_message(my_username + " REQUEST_RECEIVED"))
    if target_username not in my_receive_list:
        return {"result": False, "message": f"{target_username} has not sent you a friend request"}

    if accept:
        # Modify both users' REQUEST_RECEIVED and REQUEST_SENT
        del(my_receive_list[target_username])
        send_message(my_username + " REQUEST_RECEIVED", json.dumps(my_receive_list))
        target_request_list = json.loads(get_message(target_username + " REQUEST_SENT"))
        target_request_list[my_username]["status"] = "APPROVED"
        send_message(target_username + " REQUEST_SENT", json.dumps(target_request_list))

        # Add target info into my friend list
        target_pic_hash, target_pic_name = (get_message(target_username + " PROFILE_PICTURE")).split(" ")
        my_friend_list[target_request_list] = {"nickname": target_username,
                                               "public_key": get_message(target_username),
                                               "profile_pic_hash": target_pic_hash,
                                               "profile_pic_name": target_pic_name}

        # Update friend list in ResilientDB
        send_message(my_username + " FRIEND_LIST", json.dumps(my_friend_list))

        # Reload friend list and download corresponding files
        initial_load_friend_list(my_username)
        return {"result": True, "message": f"You have approved {target_username}'s friend request"}
    else:
        # Modify both users' REQUEST_RECEIVED and REQUEST_SENT
        del(my_receive_list[target_username])
        send_message(my_username + " REQUEST_RECEIVED", json.dumps(my_receive_list))
        target_request_list = json.loads(get_message(target_username + " REQUEST_SENT"))
        target_request_list[my_username]["status"] = "REJECTED"
        send_message(target_username + " REQUEST_SENT", json.dumps(target_request_list))
        return {"result": True, "message": f"You have rejected {target_username}'s friend request"}
