from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import JsonResponse
import os

import encryption
import db
import message

# Create your views here.


def checking_user(request):
    # change this depending on your path
    if os.path.exists("/home/ubuntu/Desktop/ECS189f_Project/private_key.pem") and os.path.exists("/home/ubuntu/Desktop/ECS189f_Project/public_key.pem"):
        redirect_url = 'login'

    else:
        redirect_url = 'register'

    # redirect the loading page to other pages (login.html or register.html)
    return render(request, 'checking_user.html', {'redirect_url': redirect_url})


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    # read the user name from the file and store it in sessions for use later.
    with open("user_info.txt", "r") as f:
        user_name = f.read()
    request.session['user_name'] = user_name

    user_pwd = request.POST.get("pwd")
    private_key = encryption.load_private_key(user_pwd)
    # if the password is correct(not none):
    if private_key:
        request.session['user_pwd'] = user_pwd
        return redirect("loading")
    return render(request, "login.html", {"error_msg": "password is incorrect"})


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    user_name = request.POST.get("name")
    user_psw = request.POST.get("psw")
    print(user_name, user_psw)
    with open(f"user_info.txt", "w") as f:
        f.write(user_name)
    public_key, private_key = encryption.create_keys(user_name, user_psw)
    return redirect("login")


# view function for loading keys page.
def loading_keys(request):
    friend_list = db.get_all_friends()
    print("loading", friend_list)

    # Store the friend list in the session
    request.session['friend_list'] = friend_list
    # Redirect to index page
    return redirect(reverse('index'))

    # redirect_url = 'chatting'
    # return render(request, "loading.html", {'redirect_url': redirect_url})

def index(request):
    # Retrieve the friend list from the session
    friends = request.session.get('friend_list', [])
    #print(friends)
    return render(request, "index.html", {'friends': friends})


def add_friend(request):
    global public_key
    friends = request.session.get('friend_list', [])
    if request.method == "GET":
        return render(request, "addfriend.html",{'friends': friends})
    # upload_file is the file which stored the friend's public key.
    upload_file = request.FILES.get('key')
    nickname = request.POST.get('nickname')
    ### still not sure, need to ask the backend leader. binary?
    if upload_file:
        # Process the uploaded file
        if isinstance(upload_file, InMemoryUploadedFile):
            # If it's an InMemoryUploadedFile, you can read its content directly
            public_key = upload_file.read().decode('utf-8')
    print(nickname)
    print(public_key)
    add_flag = db.add_friend(public_key, nickname)
    # refresh the friend list so the new friend can show in the web page.
    if add_flag is not False:
        friends = db.get_all_friends()
        request.session['friend_list'] = friends
    print(friends)
    return render(request, "addfriend.html", {'friends': friends, 'add_flag': add_flag})


def chatting_page(request, username):
    print("cf:", username)
    user_name = request.session.get("user_name")
    user_pwd = request.session.get("user_pwd")
    friend_name = username
    friends = request.session.get('friend_list', [])
    request.session["friend_name"] = username
    ####
    # get message from server and sent it to the resiliantdb
    if request.method == "POST":
        input_msg = request.POST.get("message")
        print("message##:", input_msg)
        if input_msg is not None:
            message.send_message(input_msg, friend_name)
    history = message.get_update(friend_name, user_pwd)
    if history is None:
        return render(request, 'chatting.html', context={'user': user_name, 'friends': friends, 'friend': friend_name, 'chat_history': history, "history_length": 0})
    else:
        print("history: ", len(history))
        print("history length: ", len(history))
        request.session["his_len"] = len(history)
        return render(request, 'chatting.html',
                      context={'user': user_name, 'friends': friends, 'friend': friend_name, 'chat_history': history,
                               "history_length": len(history)})



def trigger_func(request, username):
    try:
        user_pwd = request.session.get("user_pwd")
        friend_name= request.session.get("friend_name")
        history=message.get_update(friend_name, user_pwd)
        return JsonResponse({'history': history})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
        

def aboutResChat(request):
    return render(request, 'aboutResChat.html')

def profile(request):
    return render(request, 'profile.html')
