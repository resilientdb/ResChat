from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import JsonResponse
import os

import encryption
import db

# Create your views here.


def checking_user(request):
    # change this depending on your path
    if os.path.exists("\OneDrive\Documents\ECS189f_Project\private_key.pem") and os.path.exists("\OneDrive\Documents\ECS189f_Project\public_key.pem"):
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
    print("nnff")
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
    if add_flag is not None:
        friends = db.get_all_friends()
    print(friends)
    return render(request, "addfriend.html", {'friends': friends, 'add_flag': add_flag})


def chatting_page(request, username):
    user_name = request.session.get("user_name")
    friend_name = username
    friends = request.session.get('friend_list', [])
    print(friends)
    return render(request, 'chatting.html', context={'user': user_name, 'friends': friends, 'friend':friend_name})

'''
def chatting_page(request):
    # Retrieve the friend list from the session
    friend_list = request.session.get('friend_list', [])
    return render(request, "chatting.html", {'friends_names': friend_list})

    # return render(request, "chatting.html")

'''

