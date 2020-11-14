import sys
from json import dumps

from flask import Flask, request, send_from_directory
from flask_cors import CORS

import auth
import channel
import channels
import message
import other
import message
import user
from error import InputError
from database import master_users, return_token_u_id


def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response

APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

# Example
@APP.route("/echo", methods=['GET'])
def echo():
    data = request.args.get('data')
    if data == 'echo':
   	    raise InputError(description='Cannot echo "echo"')
    return dumps({
        'data': data
    })

@APP.route("/auth/register", methods=['POST'])
def auth_registers():
    data = request.get_json()
    email = data['email']
    password = data['password']
    name_first = data['name_first']
    name_last = data['name_last']
    registered = auth.auth_register(email, password, name_first, name_last)
    return dumps(registered)

@APP.route("/auth/login", methods=['POST'])
def auth_logins():
    data = request.get_json()
    email = data['email']
    password = data['password']
    logged = auth.auth_login(email, password)
    return dumps(logged)

@APP.route("/auth/logout", methods=['POST'])
def auth_logouts():
    data = request.get_json()
    token = data['token']
    logout = auth.auth_logout(token)
    return dumps(logout) 

@APP.route("/channel/details", methods=['GET'])
def channel_detail():
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))
    details = channel.channel_details(token, channel_id)
    return dumps(details)

@APP.route("/channel/messages", methods=['GET'])
def channel_message():
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))
    start = int(request.args.get('start'))
    messages = channel.channel_messages(token, channel_id, start)
    return dumps(messages)

@APP.route("/channel/leave", methods=['POST'])
def channel_leaves():
    data = request.get_json()
    token = data['token']
    channel_id = int(data['channel_id'])
    leave = channel.channel_leave(token, channel_id)
    return dumps(leave)

@APP.route("/channel/join", methods=['POST'])
def channel_joins():
    data = request.get_json()
    token = data['token']
    channel_id = int(data['channel_id'])
    join = channel.channel_join(token, channel_id)
    return dumps(join)

@APP.route("/channel/invite", methods=['POST'])
def channel_invites():
    data = request.get_json()
    token = data['token']
    channel_id = int(data['channel_id'])
    u_id = int(data['u_id'])
    invite = channel.channel_invite(token, channel_id, u_id)
    return dumps(invite)

@APP.route("/channel/addowner", methods=['POST'])
def channel_addowners():
    data = request.get_json()
    token = data['token']
    channel_id = int(data['channel_id'])
    u_id = int(data['u_id'])
    add_owner = channel.channel_addowner(token, channel_id, u_id)
    return dumps(add_owner)

@APP.route("/channel/removeowner", methods=['POST'])
def channel_removeowners():
    data = request.get_json()
    token = data['token']
    channel_id = int(data['channel_id'])
    u_id = int(data['u_id'])
    remove_owner = channel.channel_removeowner(token, channel_id, u_id)
    return dumps(remove_owner)


@APP.route("/channels/list", methods=['GET'])
def channels_lists():
    token = request.args.get('token')
    list_return = channels.channels_list(token)
    return dumps(list_return)

@APP.route("/channels/listall", methods=['GET'])
def channels_listalls():
    token = request.args.get('token')
    listall_return = channels.channels_listall(token)
    return dumps(listall_return)

@APP.route("/channels/create", methods=['POST'])
def channel_creates():
    data = request.get_json()
    token = data['token']
    name = data['name']
    is_public = data['is_public']
    created = channels.channels_create(token, name, is_public)
    return dumps(created)

@APP.route("/user/profile", methods=['GET'])
def user_profiles():
  #  data = request.get_json()
  #  u_id = int(data['u_id'])
  #  token = data['token']
    u_id = int(request.args.get('u_id'))
    token = request.args.get('token')
    profile = user.user_profile(token, u_id)
    return dumps(profile)

@APP.route("/user/profile/setname", methods=['PUT'])
def user_profile_setnames():
    data = request.get_json()
    token = data['token']
    name_first = data['name_first']
    name_last = data['name_last']
    user.user_profile_setname(token, name_first, name_last)
    return dumps({})

@APP.route("/user/profile/setemail", methods=['PUT'])
def user_profile_setemails():
    data = request.get_json()
    token = data['token']
    email = data['email']
    user.user_profile_setemail(token, email)
    return dumps({})

@APP.route("/user/profile/sethandle", methods=['PUT'])
def user_profile_sethandles():
    data = request.get_json()
    token = data['token']
    handle_str = data['handle_str']
    user.user_profile_sethandle(token, handle_str)
    return dumps({})

# @APP.route("/static/<path:path>")
# def fetch_image(path):
#     return send_from_directory('/static/', path)

@APP.route("/user/profile/uploadphoto", methods=['POST'])
def user_profile_uploadphotos():
    data = request.get_json()
    token = data['token']
    img_url = data['img_url']
    x_start = int(data['x_start'])
    y_start = int(data['y_start'])
    x_end = int(data['x_end'])
    y_end = int(data['y_end'])
    # fetch and crop the image
    image_name = user.user_profile_uploadphoto(token, img_url, x_start, y_start, x_end, y_end)
    #fetch_image(image_name)
    return dumps({})


@APP.route("/users/all", methods=['GET'])
def display_users_all():
    token = request.args.get('token')
    list_of_users = other.users_all(token)
    return dumps(list_of_users)

@APP.route("/admin/userpermission/change", methods=['POST'])
def change_user_permission():
    data = request.get_json()
    token = data['token']
    u_id = int(data['u_id'])
    permission_id = data['permission_id']
    change = other.admin_userpermission_change(token, u_id, permission_id)
    return dumps(change)  

@APP.route("/search", methods=['GET'])
def search_messages():
    token = request.args.get('token')
    query_str = request.args.get('query_str')
    messages = other.search(token, query_str)
    return dumps(messages)  

@APP.route("/clear", methods=['DELETE'])
def clear_all():
    cleared = other.clear()
    return dumps(cleared)  

@APP.route("/message/send", methods=['POST'])
def send_message():
    data = request.get_json()
    token = data['token']
    channel_id = int(data['channel_id'])
    message_to_send = data['message']
    message_id = message.message_send(token, channel_id, message_to_send)
    return dumps(message_id)

@APP.route("/message/remove", methods=['DELETE'])
def remove_message():
    data = request.get_json()
    token = data['token']
    message_id = int(data['message_id'])
    remove = message.message_remove(token, message_id)
    return dumps(remove)

@APP.route("/message/edit", methods=['PUT'])
def edit_message():
    data = request.get_json()
    token = data['token']
    message_id = int(data['message_id'])
    message_ = data['message']
    edit = message.message_edit(token, message_id, message_)
    return dumps(edit)

@APP.route("/message/sendlater", methods=['POST'])
def sendlater_message():
    data = request.get_json()
    token = data['token']
    channel_id = int(data['channel_id'])
    message_to_send = data['message']
    time_sent = data['time_sent']
    message_id = message.message_sendlater(token, channel_id, message_to_send, time_sent)
    return dumps(message_id)

@APP.route("/message/react", methods=['POST'])
def react_message():
    data = request.get_json()
    token = data['token']
    message_id = int(data['message_id'])
    react_id = int(data['react_id'])
    react = message.message_react(token, message_id, react_id)
    return react

@APP.route("/message/unreact", methods=['POST'])
def unreact_message():
    data = request.get_json()
    token = data['token']
    message_id = int(data['message_id'])
    react_id = int(data['react_id'])
    unreact = message.message_unreact(token, message_id, react_id)
    return unreact

@APP.route("/message/pin", methods=['POST'])
def pin_message():
    data = request.get_json()
    token = data['token']
    message_id = int(data['message_id'])
    pinned = message.message_pin(token, message_id)
    return pinned

@APP.route("/message/unpin", methods=['POST'])
def unpin_message():
    data = request.get_json()
    token = data['token']
    message_id = int(data['message_id'])
    unpinned = message.message_unpin(token, message_id)
    return unpinned


if __name__ == "__main__":
    APP.run(port=0) # Do not edit this port
