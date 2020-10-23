import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from error import InputError

import channel 
import channels 
import auth
import other

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
    channel_id = request.args.get('channel_id')
    start = request.args.get('start')
    messages = channel.channel_messages(token, channel_id, start)
    return dumps(messages)

@APP.route("/channel/leave", methods=['POST'])
def channel_leaves():
    data = request.get_json()
    token = data['token']
    channel_id = data['channel_id']
    leave = channel.channel_leave(token, channel_id)
    return dumps(leave)

@APP.route("/channel/join", methods=['POST'])
def channel_joins():
    data = request.get_json()
    token = data['token']
    channel_id = data['channel_id']
    join = channel.channel_join(token, channel_id)
    return dumps(join)

@APP.route("/channel/invite", methods=['POST'])
def channel_invites():
    data = request.get_json()
    token = data['token']
    channel_id = data['channel_id']
    u_id = data['u_id']
    invite = channel.channel_invite(token, channel_id, u_id)
    return dumps(invite)

@APP.route("/channel/addowner", methods=['POST'])
def channel_addowners():
    data = request.get_json()
    token = data['token']
    channel_id = data['channel_id']
    u_id = data['u_id']
    add_owner = channel.channel_addowner(token, channel_id, u_id)
    return dumps(add_owner)

@APP.route("/channel/removeowner", methods=['POST'])
def channel_removeowners():
    data = request.get_json()
    token = data['token']
    channel_id = data['channel_id']
    u_id = data['u_id']
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

@APP.route("/users/all", methods=['GET'])
def display_users_all():
    token = request.args.get('token')
    list_of_users = other.users_all(token)
    return dumps(list_of_users)  

@APP.route("/admin/userpermission/change", methods=['POST'])
def change_user_permission():
    data = request.get_json()
    token = data['token']
    u_id = data['u_id']
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






if __name__ == "__main__":
    APP.run(port=0) # Do not edit this port
