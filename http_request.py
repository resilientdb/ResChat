import asyncio
import json

from aiohttp import web
import client
import os
import aiohttp_cors


async def handle_login(request):
    if os.path.exists('private_key.pem'):
        result = client.login(request.query.get('usrname'), request.query.get('psw'))
        if result:
            return web.json_response({'result': True, 'message': 'Login in successfully'})
        else:
            return web.json_response({'result': False, 'message': 'Wrong username or password'})
    else:
        return web.json_response({'result': False, 'message': 'No private key found, please signup'})


async def handle_signup(request):
    if os.path.exists('private_key.pem'):
        return web.json_response({'result': False, 'message': 'Private key already exists, please login'})
    result = client.encapsulated_create_user(request.query.get('usrname'), request.query.get('psw'))
    if not result:
        return web.json_response({'result': False, 'message': 'Username already taken, please try another one'})
    else:
        return web.json_response({'result': True, 'message': 'Signup successfully, please login'})


async def get_friend_list(request):
    return web.json_response(client.my_friend_list)


async def handle_add_friend(request):
    result = client.encapsulated_add_friend(request.query.get('usrname'), request.query.get('nickname'))
    if not result:
        return web.json_response({'result': False, 'message': 'Username not found or nickname already in use'})
    else:
        return web.json_response({'result': True, 'message': result})


async def handle_send_message(request):
    # print(request)
    result = client.send_text_message(request.query.get('message'))
    return web.json_response({'result': result, 'message': None})


async def handle_select_friend(request):
    select_result = client.select_friend_to_chat_with(request.query.get('message'))
    client.initial_chat_history_loading()
    chat_history = client.current_chat_history
    if select_result:
        return web.json_response({'result': chat_history, 'message': ""})
    else:
        return web.json_response({'result': [], 'message': 'Friend not found in your friend list'})


async def handle_update_chat_history(request):
    client.update_chat_history()
    chat_history = client.current_chat_history
    return web.json_response({'result': chat_history, 'message': ""})


app = web.Application()
app.router.add_get('/login', handle_login)
app.router.add_get('/signup', handle_signup)
app.router.add_get('/friendList', get_friend_list)
app.router.add_get('/addFriend', handle_add_friend)
app.router.add_get('/sendMessage', handle_send_message)
app.router.add_get('/selectFriend', handle_select_friend)
app.router.add_get('/updateChatHistory', handle_update_chat_history)

cors = aiohttp_cors.setup(app, defaults={
    "*": aiohttp_cors.ResourceOptions(
        allow_credentials=True,
        expose_headers="*",
        allow_headers="*",
        allow_methods=["GET", "POST"]
    )
})

for route in list(app.router.routes()):
    cors.add(route)


# 手动启动事件循环
async def start_app():
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', 8080)
    await site.start()


if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(start_app())
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()

# @get('/api/users')
# def api_get_users(*, page='1'):
#     page_index = get_page_index(page)
#     num = yield from User.findNumber('count(id)')
#     p = Page(num, page_index)
#     if num == 0:
#         return dict(page=p, users=())
#     users = yield from User.findAll(orderBy='created_at desc', limit=(p.offset, p.limit))
#     for u in users:
#         u.passwd = '******'
#     return dict(page=p, users=users)
