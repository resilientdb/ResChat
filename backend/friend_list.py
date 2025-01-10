import json

from RSDB_kv_service import get_kv, set_kv

"""
Friend list is a JSON/Python dict object stores all friend information
{
    FRIEND1's USER NAME:    {
                                "nick_name": FRIEND1's NICK NAME,
                                "public_key": FRIEND1's PUBLIC KEY,
                                "avatar_cid": FRIEND1's AVATAR CID,
                            },
    FRIEND2's USER NAME:    {
                                "nick_name": FRIEND2's NICK NAME,
                                "public_key": FRIEND2's PUBLIC KEY,
                                "avatar_cid": FRIEND2's AVATAR CID,
                            },
}
"""

def load_my_friend_list(user_name: str) -> {}:
    """
    Load friend list from RSDB
    : return a python dict friend list

    """
    friend_list_str = get_kv(user_name + " FRIEND")
    try:
        return json.loads(friend_list_str)
    except:
        return {}


def update_rsdb_friend_list(friend_list: {}, username: str) -> None:
    """
    All modification of friend list are only done in local, call this function to update friend list in RSDB after
        any modification to friend list
    : return None
    """
    set_kv(username + " FRIEND", json.dumps(friend_list))
    return


def update_avatar_list(friend_list: {}) -> {}:
    """
    Update friends' avatar cid
    : return an updated python dict
    """
    for username in friend_list.keys():
        new_avatar_cid = get_kv(username + " AVATAR")
        if new_avatar_cid == "\n" or new_avatar_cid == "" or new_avatar_cid == " ":
            friend_list[username]["avatar_cid"] = ""
        else:
            friend_list[username]["avatar_cid"] = new_avatar_cid
    return friend_list


def add_friend(username: str, friend_list: {}, nickname: str) -> {}:
    """
    Add a new friend to friend list, and set corresponding kv pairs in RSDB
    : return an updated friend list python dict with status True if success
        {"result": True, "message": {UPDATED FRIEND LIST}}
    : return result False with an error message
    """
    friend_public_key = get_kv(username)
    friend_avatar_cid = get_kv(username + " AVATAR")
    if friend_public_key == " " or friend_public_key == "\n" or friend_public_key == "":
        return {"result": False, "message": "Friend doesn't exists"}
    else:
        if friend_avatar_cid == "\n" or friend_avatar_cid == " " or friend_avatar_cid == "":
            friend_avatar_cid = ""
        friend_list[username] = {"nick_name": nickname, "public_key": friend_public_key, "avatar_cid": friend_avatar_cid}
        # TODO: Sort these two username is ASCII order and create kv in RSDB (a123b456 PAGE_NUM, 1).
        #       But if there is already an exist page number, keep that one