from error import InputError
from error import AccessError
import hashlib
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
#       'channel_id':
#       'u_id':
#       'message':
#       'deleted':
#   }
# }


'''
probably needs to be deleted:
# messages in channels
#channels_and_messages = { channel_id: messages, channel_id2: messages2, ... }
#channels_and_messages = { 1: [ { 'message_id': 1, 'u_id': 1, 'message' = 'whtever the fuck', 'time_created' = 1111111111 }, { 'message_id': 2, ... } ... ], 2: ... }
#channels_and_messages = {}
'''

# # # FUNCTIONS THAT ALTER THE VARIABLES ABOVE # # #

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
    #global channels_and_messages
    #channels_and_messages = {}

    
def make_admin(u_id):
    global admin_users
    admin_users['u_id'] = True

def remove_admin(u_id):
    global admin_users
    admin_users.pop('u_id', None)
    '''
    or
    try:
        del admin_users['u_id']
    except KeyError:
        pass
    '''
    
def is_str_in_msg(query_str, message):
    return (query_str in message)

def is_flockr_owner(token):    
    if master_users[0]['token'] == token:
        return True
    raise AccessError
    
def convert_from_tok_to_u_id(token):
    u_id = -1
    for user in master_users:
        if user['token'] == token:
            u_id = user['u_id']
    return u_id

def add_all_users_to_list(list_of_users):
    single_user = {}
    for user in master_users:
        single_user['u_id'] = user['u_id']
        single_user['email'] = user['email']
        single_user['name_first'] = user['name_first']
        single_user['name_last'] = user['name_last']
        single_user['handle_str'] = user['handle_str']
        list_of_users.append(single_user)
        single_user = {}
    return list_of_users

def add_selected_messages_to_list(query_str, token, list_of_messages):
    single_message = {}
    u_id = convert_from_tok_to_u_id(token)
    print("messages is:")
    print(messages)
    for message in messages: 
        print("message is:")
        print(message)
        message = messages[message]
        print("message is:")
        print(message)
        try:
            cond_one = channel_in_check(message['channel_id'], u_id)
        except:
            #channel_id doesnt exist (ie channel as been deleted)
            cond_one = False
        cond_two = is_str_in_msg(query_str, message['message'])
        cond_three = message['deleted'] == False
        if cond_one and cond_two and cond_three:
            single_message['message_id'] = message['message_id']
            single_message['u_id'] = message['u_id']
            single_message['message'] = message['message']
            single_message['time_created'] = message['time_created']
            list_of_messages.append(single_message)
            single_message = {}
    return list_of_messages

def token_check(token):
    try:
        u_id = int(token)
    except:
        raise AccessError #invalid token
    return u_id
   
    
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


# CHANNELS FUNCTIONS #
    
def channel_find_user(u_id):
    ''' find user and make member '''
    member = {}
    for user in master_users:
        if user['u_id'] == u_id:
            member['u_id'] = u_id
            member['name_first'] = user['name_first']
            member['name_last'] = user['name_last']
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

'''
delete?

def channel_fetch_messages(channel_id):
    return channels_and_messages[channel_id]
'''

def channel_remove_member(channel_id, u_id):
    ''' remove member from channel '''
    # search public channels
    # update found after private search too, else return input error
    for channel in public_channels:
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
                del public_channels[channel_id]
                del channels[channel_id]
    
    # if channel/user could be in private channel
    for channel in private_channels:   
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
        # remove from all members 
        for user in channels_and_members[channel_id][1]:               
            if user['u_id'] == u_id:
                channels_and_members[channel_id][1].remove(user)
            if len(channels_and_members[channel_id][1]) == 0 :
                del channels_and_members[channel_id]
                del private_channels[channel_id]
                del channels[channel_id]

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
            # join to all_members:
            channels_and_members[channel_id][1].append(member)
            joined = True
    return joined
            

def channel_check_admin(u_id):
    if master_users[0]['u_id'] == u_id:
        return True
    try:
        if admin_users['u_id'] == True:
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
