from error import InputError
from error import AccessError
# To be put into iteration 1

# (not given in spec) master users variables (contains ALL data relevant to ALL registered users)
# should update token each time we login
master_users = []

channels = []

private_channels = [] # [{'channel_id': 2, 'name': 'channel1'},]
public_channels = []# [{'channel_id': 1, 'name': 'channel2'}, ]

# channels_and_members = { channel_id: [owner_members, all_members], channel2: [owner_members2, all_members2], ...}
channels_and_members = {}


# messages in channels
#channels_and_messages = { channel_id: messages, channel_id2: messages2, ... }
#channels_and_messages = { 1: [ { 'message_id': 1, 'u_id': 1, 'message' = 'whtever the fuck', 'time_created' = 1111111111 }, { 'message_id': 2, ... } ... ], 2: ... }
channels_and_messages = {}


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
            if password != user["password"]:
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
        if handle == users['handle'] and i < 10:
            handle_list[-1] = str(i)
            handle = "".join(handle_list)
            i = i + 1
        elif handle == users['handle'] and i < 100:
            handle_list[-2] = str(i)[0]
            handle_list[-1] = str(i)[1]
            handle = "".join(handle_list)
            i = i + 1
    return handle


def auth_add_user(master_user):
    ''' add new user to the master_users database '''
    master_users.append(master_user)


# CHANNELS FUNCTIONS #

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
    member = {}
    member['u_id'] = u_id
    member['name_first'] = name_first
    member['name_last'] = name_last
    channels_and_members[channel_id] = [[member], [member]]
    channels.append(channel)
    if is_public == True:
        public_channels.append(channel)
    elif is_public == False:
        private_channels.append(channel)


def channels_user_exist_check(u_id):
    ''' check if a user exists for the given u_id'''
    valid_user = 0
    for user in master_users:
        if user['u_id'] == u_id and user['log'] == True:
            valid_user = 1 # 'log' == True if logged in
    if valid_user != 1:
        raise AccessError
