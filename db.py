import json


def add_friend(public_key, nick_name):
    with open("local_friends_list.json", 'rw') as file:
        dic = json.load(file)
        if nick_name in dic:
            print(f"{nick_name} is already your friend")
            return None
        else:
            dic[nick_name] = {"public_key": public_key, "current_page": 1}
            json.dump(dic, file)


def get_friend(nick_name):
    with open("local_friends_list.json", 'rw') as file:
        dic = json.load(file)
        if nick_name in dic:
            return dic[nick_name]
        else:
            print(f"{nick_name} is not your friend yet")


def get_all_friends():
    with open("local_friends_list.json", 'rw') as file:
        dic = json.load(file)
        return dic.keys()





