from error import InputError
from error import AccessError
import hashlib
import jwt
import helper
import flask
import urllib.request
import os
# To be put into iteration 1


# list of dictionary's containing ALL users :
master_users = []
# (contains ALL data relevant to ALL registered users)
# should update token each time we login

#all channels:
channels = []

# variables storing public and private channels id and name:
private_channels = [] 
# [{'channel_id': 1, 'name': 'channel1'},]
public_channels = [] 
# [{'channel_id': 2, 'name': 'channel2'}, ]

# dictionary of channels and respective members:
channels_and_members = {}
# channels_and_members = { channel_id: [owner_members, all_members], channel2: [owner_members2, all_members2], ...}

# ditionary of u_id's of admins:
admin_users = {}

# dictionary of messages:
messages = {}
# messages = {
#   'message_id': {
#       'message_id':
#       'channel_id':
#       'u_id':
#       'message':
#       'time_created':
#       'reacts': [{'react_id': ?, 'u_ids': ?, 'is_this_user_reacted': ? }]
#       'is_pinned':
#   }
# }

# Total messages sent
total_messages = 0

#channels that have standup active and time it ends
channel_standup_active = []

# hangman
channel_hangman_active = []

# blocked users: key = u_id, value = list of blocked users. 
# cannot block urself
blocked_users = {}

'''
probably needs to be deleted:
# messages in channels
#channels_and_messages = { channel_id: messages, channel_id2: messages2, ... }
#channels_and_messages = { 1: [ { 'message_id': 1, 'u_id': 1, 'message' = 'whtever the fuck', 'time_created' = 1111111111 }, { 'message_id': 2, ... } ... ], 2: ... }
#channels_and_messages = {}
'''

# # # FUNCTIONS THAT ALTER THE VARIABLES ABOVE # # #
# secret token encoder
SECRET = 'kellycyrusandreeajoshnick'
RESET_SECRET = 'shhhh!!!'

# FUNCTIONS USED IN ALL FILES #

def token_check(token):
    ''' check if the token exists in database'''
    token_exists = False
    for user in master_users:
        if token == user["token"] and user["log"] == True:
            token_exists = True
            break

    if token_exists == True:
        decoded_token = jwt.decode(token.encode('utf-8'), SECRET, algorithms=['HS256'])
        return decoded_token["u_id"]
    else:
        raise AccessError #invalid token
    
def convert_from_tok_to_u_id(decoded_token):
    u_id = -1
    for user in master_users:
        if user['token'] == decoded_token:
            u_id = user['u_id']
    return u_id

# OTHER.PY FUNCTIONS #

def clear():
    global master_users
    master_users = []
    global channels
    channels = []
    global private_channels
    private_channels = []
    global public_channels
    public_channels = []
    global channels_and_members
    channels_and_members = {}
    global admin_users
    admin_users = {}
    global messages
    messages = {}
    global total_messages
    total_messages = 0
    global channel_standup_active
    channel_standup_active = []

    
def make_admin(u_id):
    global admin_users
    admin_users[f'{u_id}'] = True

def remove_admin(u_id):
    global admin_users
    admin_users.pop(f'{u_id}', None)
    
def is_str_in_msg(query_str, message):
    return (query_str in message)

def is_flockr_owner(token):    
    if master_users[0]['token'] == token:
        return True
    raise AccessError
    
def add_all_users_to_list(list_of_users):
    single_user = {}
    for user in master_users:
        single_user['u_id'] = user['u_id']
        single_user['email'] = user['email']
        single_user['name_first'] = user['name_first']
        single_user['name_last'] = user['name_last']
        single_user['handle_str'] = user['handle_str']
        single_user['profile_img_url'] = user['profile_img_url']
        list_of_users.append(single_user)
        single_user = {}
    return list_of_users

def add_selected_messages_to_list(query_str, token, list_of_messages):
    single_message = {}
    u_id = convert_from_tok_to_u_id(token)
    for message in messages: 
        message = messages[message]
        try:
            cond_one = channel_in_check(message['channel_id'], u_id)
        except:
            #channel_id doesnt exist (ie channel as been deleted)
            cond_one = False
        cond_two = is_str_in_msg(query_str, message['message'])
        if cond_one and cond_two:
            single_message['message_id'] = message['message_id']
            single_message['u_id'] = message['u_id']
            single_message['message'] = message['message']
            single_message['time_created'] = message['time_created']
            single_message['reacts'] = react_output(u_id, message['message_id'], 1)
            single_message['is_pinned'] = message['is_pinned']
            list_of_messages.append(single_message)
            single_message = {}
    return list_of_messages

    
# AUTH FUNCTIONS #

def auth_check_email_login(email):
    ''' check if an email address is registered'''
    if len(master_users) == 0:
        raise InputError(f"Error, {email} has not been registered")
    exists = False
    for user in master_users:
        if email == user["email"]:
            exists = True
    if exists == False:
        raise InputError(f"Error, {email} has not been registered")


def auth_check_password(email, password): # in context: return auth_check_password(email, password)
    ''' check if password is wrong '''
    for user in master_users:
        if email == user["email"]:
            if hashlib.sha256(password.encode()).hexdigest() != user["password"]:
                raise InputError(f"Error, the password is incorrect")
            else:
                id = user["u_id"]
                tok = user["token"]
                user["log"] = True
    return {
        'u_id': id,
        'token': tok,
    }

def auth_logout_user(token):
    ''' log active user out '''
    # check if token exists
    # if the token is active, log the user out
    for users in master_users:
        if token == users["token"] and users["log"] == True:
            users["log"] = False
            return {
            'is_success': True,
        }
    # else token is inactive, return false
    return {
        'is_success': False,
    }

def auth_check_email_register(email):
    ''' check whether email address is being used by another user '''
    for id in master_users:
        if email == id["email"]:
            raise InputError(f"Error, {email} has been taken")

def auth_assign_id(): # in context: id = auth_assign_id():
    ''' assign u_id in chronological order of registration '''
    return len(master_users)

def auth_assign_user_handle(handle): # in context: handle = auth_check_user_handle(handle):
    ''' loop to ensure new user handle is new '''
    # create variables that allow us to manipulate the handle string
    handle_list = list(handle)
    i = 1
    for users in master_users:
        # if new user handle exists, tweak it
        if handle == users['handle_str'] and i < 10:
            handle_list[-1] = str(i)
            handle = "".join(handle_list)
            i = i + 1
        elif handle == users['handle_str'] and i < 100:
            handle_list[-2] = str(i)[0]
            handle_list[-1] = str(i)[1]
            handle = "".join(handle_list)
            i = i + 1
    return handle

def auth_add_user(master_user):
    ''' add new user to the master_users database '''
    master_users.append(master_user)

# given a valid email address, create a reset code and put it into the database
def create_reset_code(email):
    code = jwt.encode({"email": email}, RESET_SECRET, algorithm='HS256').decode('utf-8')
    for user in master_users:
        if email == user["email"]:
            user['reset_code'] = code
    return code 

def auth_passwordreset_return(email):
    email_exists = False
    for user in master_users:
        if email == user["email"]:
            email_exists = True
            break
    
    if email_exists == True:
        # send the email
        reset_code = create_reset_code(email)
        return reset_code
    

def reset_password(reset_code, new_password):
    reset = False
    for user in master_users:
        if reset_code == user['reset_code']:
            reset = True
            helper.check_password_length(new_password)
            user['password'] = hashlib.sha256(new_password.encode()).hexdigest()
            user['reset_code'] = None
            break
    if reset == False:
        raise InputError("Reset code is incorrect")

# CHANNELS FUNCTIONS #
    
def channel_find_user(u_id):
    ''' find user and make member '''
    member = {}
    for user in master_users:
        if user['u_id'] == u_id:
            member['u_id'] = u_id
            member['name_first'] = user['name_first']
            member['name_last'] = user['name_last']
            member['profile_img_url'] = user['profile_img_url']
            break
    return member

def channel_join_members(channel_id, member):
    ''' add a member to a channel '''
    channels_and_members[channel_id][1].append(member)

def channel_fetch_name(channel_id):
    for channel in channels:
        if channel['channel_id'] == channel_id:
            name = channel['name']
    return name

def channel_fetch_owners(channel_id):
    return channels_and_members[channel_id][0]

def channel_fetch_members(channel_id):
    return channels_and_members[channel_id][1]

def channel_fetch_messages(channel_id):
    return messages

def channel_remove_member(channel_id, u_id):
    ''' remove member from channel '''
    # search public channels
    # update found after private search too, else return input error
    owner_exists = 0
    # check if owner
    for owner in channels_and_members[channel_id][0]:
        if owner['u_id'] == u_id:
            owner_exists = 1
    if owner_exists == 1:
        # remove from owners 
        for user in channels_and_members[channel_id][0]:
            if user['u_id'] == u_id:
                channels_and_members[channel_id][0].remove(user)
    #remove from all members 
    for user in channels_and_members[channel_id][1]:
        if user['u_id'] == u_id:
            channels_and_members[channel_id][1].remove(user)
        if len(channels_and_members[channel_id][1]) == 0 :
            del channels_and_members[channel_id]
            for channel in public_channels:
                if channel["channel_id"] == channel_id:
                    public_channels.remove(channel)
            for channel in private_channels:
                if channel["channel_id"] == channel_id:
                    private_channels.remove(channel)
            for channel in channels:
                if channel["channel_id"] == channel_id:
                    channels.remove(channel)

def channel_add_member(channel_id, u_id): # made changes i don't get
    ''' add member to channel '''
    joined = False
    for channel in public_channels:
        if channel['channel_id'] == channel_id:
            member = {}
            for user in master_users:
                if user['u_id'] == u_id:
                    member['u_id'] = u_id
                    member['name_first'] = user['name_first']
                    member['name_last'] = user['name_last']
                    member['profile_img_url'] = user['profile_img_url']
            # join to all_members:
            channels_and_members[channel_id][1].append(member)
            joined = True
    return joined
            
def channel_check_admin(u_id):
    if master_users[0]['u_id'] == u_id:
        return True
    try:
        if admin_users[f'{u_id}'] == True:
            return True
    except:
        return False

def channel_add_member_private(channel_id, u_id):
    for channel in private_channels:
        if channel['channel_id'] == channel_id:
            #  join as owner of channel and normal
            member = {}
            member['u_id'] = u_id
            member['name_first'] = master_users[0]['name_first']
            member['name_last'] = master_users[0]['name_last']
            member['profile_img_url'] = master_users[0]['profile_img_url']
            # join to all_members:
            channels_and_members[channel_id][1].append(member)

def channel_if_owner(u_id_inviter, channel_id):
    if_in = 0
    try:
        for member in channels_and_members[channel_id][0]:
            if member['u_id'] == u_id_inviter:
                if_in = 1 #invitee is an owner of channel
            #if member['u_id'] == u_id: # invited person is already an owner of channel
            #    raise InputError
    except:
        raise InputError #channel_id doesnt exist / invitee person is already owner
    return if_in

def channel_check_valid_user(u_id):
    valid_user = 0
    new_owner = {}
    for user in master_users:
        if user['u_id'] == u_id:
            new_owner['u_id'] = u_id
            new_owner['name_first'] = user['name_first']
            new_owner['name_last'] = user['name_last']
            new_owner['profile_img_url'] = user['profile_img_url']
            valid_user = 1
    return valid_user, new_owner

def channel_add_owner(new_owner, u_id, channel_id):
    # append to owner members, and all members if not already in channel

    if new_owner in channels_and_members[channel_id][0] :
        raise InputError

    channels_and_members[channel_id][0].append(new_owner)
    in_all = 0
    for member in channels_and_members[channel_id][1]:
        if member['u_id'] == u_id: # invited person is already a member of channel                    
            in_all = 1
    if in_all == 0:
        channels_and_members[channel_id][1].append(new_owner)

def channel_check_owners(u_id, channel_id):
    if_in = 0
    try:
        for member in channels_and_members[channel_id][0]:
            if member['u_id'] == u_id: # owner to be removed is in the channel
                if_in = 1
    except:
        raise InputError #channel_id doesnt exist
    return if_in


def channels_return_membership(u_id):
    '''return all channels that a user is a member of'''
    user_channels = []
    for key in channels_and_members:
        for member in channels_and_members[key][1]:
            if member['u_id'] == u_id:
                i = 0
                while channels[i]['channel_id'] != key:
                    i = i + 1
                user_channels.append(channels[i])
    return {
        'channels': user_channels,
    }

def channels_return_all():
    '''return all channels'''
    return {
            'channels': channels
        }

def channels_assign_id():
    ''' assign a new channel id '''
    return len(channels)

def channels_add_to_database(u_id, name, channel_id, is_public):
    '''add channel to database'''
    ## add channel details
    channel = {}
    channel['channel_id'] = channel_id
    channel['name'] = name
    ## user details
    name_first = master_users[u_id]['name_first']
    name_last = master_users[u_id]['name_last']
    profile_img_url = master_users[u_id]['profile_img_url']
    member = {}
    member['u_id'] = u_id
    member['name_first'] = name_first
    member['name_last'] = name_last
    member['profile_img_url'] = profile_img_url
    channels_and_members[channel_id] = [[member], [member]]
    channels.append(channel)
    if is_public == True:
        public_channels.append(channel)
    elif is_public == False:
        private_channels.append(channel)

def channels_user_log_check(u_id):
    ''' check if a user exists for the given u_id'''
    valid_user = 0
    for user in master_users:
        if user['u_id'] == u_id and user['log'] == True:
            valid_user = 1 # 'log' == True if logged in
    if valid_user != 1:
        raise AccessError

# CHANNEL FUNCTIONS #

def channel_remove_owner(u_id, channel_id):
    for user in channels_and_members[channel_id][0]:
        if user['u_id'] == u_id:
            channels_and_members[channel_id][0].remove(user)


def channel_user_exist_check(u_id):
    if_in = 0
    for user in master_users:
        if user['u_id'] == u_id:
                if_in = 1
    if if_in != 1: 
        raise InputError

def channel_in_check(channel_id, u_id):
    for member in channels_and_members[channel_id][1]:
        if member['u_id'] == u_id:
            return 1 # return 1 if they are in
    return 0 # return 0 if they are not in


def channel_valid_channel(channel_id):
    try:
        return channels_and_members[channel_id]
    except: 
        raise InputError


def channel_member_permissions(channel_id, u_id):
    if (channel_in_check(channel_id, u_id) == 0):
        raise AccessError # not a member of channel


# MESSAGE FUNCTIONS #

# Check a user exists
def message_user_exists(token):
    # First that the user is in the channel_id
    # To do this we find the u_id through the token
    # Either call a function in the database or copy and paste this
    u_id_exists = False
    for user in master_users:
        if user['token'] == token:
            u_id_exists = True
    # If u_id does not exist, the user does not exist
    return u_id_exists

# Check whether there are any channels (to prevent index errors)
def message_channel_exists():
    channel_exists = len(channels)
    if channel_exists > 0:
        return True
    return False

# Given a channel_id and user_id, check whether user is a member
def message_user_is_member(u_id, channel_id):
    for users in channels_and_members[channel_id][1]:
        if u_id == users['u_id']:
            return True
    return False

# Determine message_id of new message
def message_new_message_id():
    return total_messages

# Given a channel, check if u_id is an owner
def message_user_is_owner(u_id, channel_id):
    for users in channels_and_members[channel_id][0]:
        if u_id == users['u_id']:
            return True
    return False

# Given a channel, check if u_id is an admin
def message_user_is_admin(u_id):
    for users in admin_users:
        if u_id == users:
            return True
    return False

# Given a message_id, change the deleted key to true
def message_delete_message(message_id):
    del messages[f'{message_id}']
    return

# Check if there are any messages in database
def message_messages_empty():
    if len(messages) == 0:
        return True
    return False

# Given a message_id, check if it exists
def message_message_exist(message_id):
    if f'{message_id}' in messages:
        return True
    return False

# Given message_id find channel_id
def message_channel_id_from_message_id(message_id):
    return messages[f'{message_id}']['channel_id']

# Given a message, edit the database
def message_edit_message(message, message_id):
    messages[f'{message_id}']['message'] = message
    return

# Increment the message counter
def message_incrementing_total_messages():
    global total_messages
    total_messages += 1
    return

# Append a message to the database
def message_append_message(message_id, message_package):
    messages[f'{message_id}'] = message_package
    global total_messages
    total_messages += 1
    return

def message_num_messages():
    return messages

def pin_message(message_id):
    if messages[f'{message_id}']['is_pinned'] == False:
        messages[f'{message_id}']['is_pinned'] = True
    else: 
        raise InputError

def unpin_message(message_id):
    if messages[f'{message_id}']['is_pinned'] == True:
        messages[f'{message_id}']['is_pinned'] = False
    else: 
        raise InputError

def react_message(u_id, message_id, react_id):
    react_num = react_id - 1
    reaccs = react_output(u_id,message_id, react_id)
    if reaccs[react_num]['is_this_user_reacted'] == True:
        raise InputError
    else:
        messages[f'{message_id}']['reacts'][react_num]["u_ids"].append(u_id)

def unreact_message(u_id, message_id, react_id):
    react_num = react_id - 1
    reaccs = react_output(u_id,message_id, react_id)
    if reaccs[react_num]['is_this_user_reacted'] == False:
        raise InputError
    else:
        messages[f'{message_id}']['reacts'][react_num]["u_ids"].remove(u_id)
        
def react_output(u_id, message_id, react_id):
    react_num = react_id - 1
    for person in messages[f'{message_id}']['reacts'][react_num]["u_ids"]:
        if person == u_id:
            return [{'react_id': messages[f'{message_id}']['reacts'][react_num]['react_id'],
                     'u_ids': messages[f'{message_id}']['reacts'][react_num]['u_ids'],
                     'is_this_user_reacted': True }]
    return [{'react_id': messages[f'{message_id}']['reacts'][react_num]['react_id'],
             'u_ids': messages[f'{message_id}']['reacts'][react_num]['u_ids'],
             'is_this_user_reacted': False }]


# USER FUNCTIONS #

def return_token_u_id(token):
    ''' check if the token exists in database, and return u_id of token'''
    valid_token = False
    for i in range(0, len(master_users)):
        if token == master_users[i]["token"] and master_users[i]["log"] == True:
            valid_token = True
            found_i = i
    if valid_token == False:
        raise AccessError("Token passed in is not a valid token.")
    return found_i

def check_user_exists(u_id):
    '''check if the u_id exists, if so, return user'''
    # check if u_id exists in database - if not, return InputError
    user_exists = False
    for user in master_users:
        if u_id == user["u_id"]:
            user_exists = True
            found_user = user
            break
    if user_exists == False:
        raise InputError(f"User with u_id {u_id} is not a valid user")
    return found_user

def update_first_name(u_id, name_first):
    master_users[u_id]['name_first'] = name_first
    for channel, member_lists in channels_and_members.items():
        for members in member_lists:
            for users in members:
                if users['u_id'] == u_id:
                    users['name_first'] = name_first
                    channel

def update_last_name(u_id, name_last):
    master_users[u_id]['name_last'] = name_last
    for channel, member_lists in channels_and_members.items():
        for members in member_lists:
            for users in members:
                if users['u_id'] == u_id:
                    users['name_last'] = name_last
                    channel

def update_email(u_id, email):
    master_users[u_id]['email'] = email
    for channel, member_lists in channels_and_members.items():
        for members in member_lists:
            for users in members:
                if users['u_id'] == u_id:
                    users['email'] = email
                    channel

def update_handle(u_id, handle_str):
    master_users[u_id]['handle_str'] = handle_str
    for channel, member_lists in channels_and_members.items():
        for members in member_lists:
            for users in members:
                if users['u_id'] == u_id:
                    users['handle_str'] = handle_str
                    channel

def check_valid_img_url(img_url):
    try:
        urllib.request.urlopen(img_url)
    except:
        raise InputError("Image URL is invalid")

def check_jpg_format(image_type):
    if image_type != "JPEG":
        raise InputError("Image is not of JPEG type")

def check_valid_crop_coordinates(x_start, x_end, y_start, y_end, width, height):
    if x_start > x_end or y_start > y_end:
        raise InputError("Crop co-ordinates must be directed from upper left to lower right")
    if x_start > width or x_start < 0 or x_end > width or x_end < 0:
        raise InputError("x crop co-ordinates are not within image range")
    if y_start > height or y_start < 0 or y_end > height or y_end < 0:
        raise InputError("y crop co-ordinates are not within image range")

def check_file_already_exists(image_name):
    try:
        os.remove("src/static/" + image_name)
    except OSError:
        pass

def update_profile_img_url(u_id, image_name):
    master_users[u_id]['profile_img_url'] = flask.request.host_url + 'static/' + image_name

def update_user_profile_img_url(u_id, image_name):
    for channel, member_lists in channels_and_members.items():
        for members in member_lists:
            for users in members:
                if users['u_id'] == u_id:
                    users['profile_img_url'] = flask.request.host_url + 'static/' + image_name
                    channel

def check_handle(handle_str):
    for user in master_users:
        if handle_str == user["handle_str"]:
            raise InputError(f"Error, {handle_str} handle has been taken")

# STANDUP FUNCTIONS #

def add_standup(channel_id, end_time, u_id):
    for channel in channel_standup_active:
        if channel['channel_id'] == channel_id:
            raise InputError
    
    active_standup = {}
    active_standup['channel_id'] = channel_id
    active_standup['time_finish'] = end_time
    active_standup['message'] = ''
    active_standup['u_id'] = u_id
    channel_standup_active.append(active_standup)

def standup_removal(channel_id):
    for active_standup in channel_standup_active:
        if active_standup['channel_id'] == channel_id:
            message_id = message_new_message_id()
            message_package = {
                'message_id': message_id,
                'channel_id': channel_id,
                'u_id': active_standup['u_id'],
                'message': active_standup['message'],
                'time_created': active_standup['time_finish'],
                'reacts': [{'react_id': 1, 'u_ids': [], 'is_this_user_reacted': False }],
                'is_pinned': False,
            }
            if active_standup['message'] != '':
                messages[f'{message_id}'] = message_package
                message_incrementing_total_messages()
            channel_standup_active.remove(active_standup)

def active_check(channel_id):
    status = {}
    for channel in channel_standup_active:
        if channel['channel_id'] == channel_id:
            status['is_active'] = True
            status['time_finish'] = channel['time_finish']
            return status
    status['is_active'] = False
    status['time_finish'] = None
    return status

def standup_message_add(channel_id, standup_message):
    for channel in channel_standup_active:
        if channel['channel_id'] == channel_id:
            channel['message'] += standup_message
            return
    raise InputError # no current standup in channel

def standup_fetch_message(channel_id):
    for channel in channel_standup_active:
        if channel['channel_id'] == channel_id:
            return channel['message']
    raise InputError # no current standup in channel

def fetch_first_name(u_id):
    return master_users[u_id]['name_first']

def fetch_handle(u_id):
    return master_users[u_id]['handle_str']

def block_user(u_id, u_block):
    if u_id == u_block:
        raise InputError('You cannot block yourself.')
    if is_blocked(u_id, u_block):
        raise InputError(f'User {fetch_handle_from_u_id(u_block)} is already blocked.')
    blocked_users[f'{u_id}'].append(u_block)

def unblock_user(u_id, u_unblock):
    if not is_blocked(u_id, u_unblock):
        raise InputError(f'User {fetch_handle_from_u_id(u_unblock)} is not blocked.')
    blocked_users[f'{u_id}'].remove(u_unblock)

def is_blocked(u_id, u_block):
    if blocked_users[f'{u_id}'].count(u_block):
        return True
    return False

def add_blocklist(u_id):
    blocked_users[f'{u_id}'] = []

def fetch_u_id_from_handle(handle):
    u_id = -1
    for user in master_users:
        if user['handle_str'] == handle:
            u_id = user['u_id']
    return u_id

def fetch_handle_from_u_id(u_id):
    for user in master_users:
        if user['u_id'] == u_id:
            return user['handle_str']

def start_hangman(channel_id, word):
    for channel in channel_hangman_active:
        if channel['channel_id'] == channel_id:
            raise InputError
    active_hangman = {}
    active_hangman['channel_id'] = channel_id
    active_hangman['word'] = word
    active_hangman['fails'] = 0
    active_hangman['found'] = []
    channel_hangman_active.append(active_hangman)

def end_hangman(channel_id):
    for active_hangman in channel_hangman_active:
        if active_hangman['channel_id'] == channel_id:
            channel_hangman_active.remove(active_hangman)

def hangman_active_check(channel_id):
    for channel in channel_hangman_active:
        if channel['channel_id'] == channel_id:
            return True
    return False

def hangman_guess(channel_id, guess):
    found = False
    for channel in channel_hangman_active:
        if channel['channel_id'] == channel_id:
            for char in channel['found']:
                if char == guess:
                    raise InputError('Letter already found.')
            for char in channel['word']:
                if char == guess:
                    channel['found'].append(guess)
                    found = True
            if not found:
                channel['fails'] += 1
            return channel['fails']

def print_hangman_progress(channel_id):
    progress = ''
    for channel in channel_hangman_active:
        if channel['channel_id'] == channel_id:
            for char in channel['word']:
                if channel['found'].count(char) > 0:
                    progress += f'{char} '
                else:
                    progress += '_ '
    return progress

def check_hangman_victory(channel_id):
    finished = True
    for channel in channel_hangman_active:
        if channel['channel_id'] == channel_id:
            for char in channel['word']:
                if channel['found'].count(char) == 0:
                    finished = False
    return finished

def fetch_hangman_word(channel_id):
    for channel in channel_hangman_active:
        if channel['channel_id'] == channel_id:
            return channel['word']