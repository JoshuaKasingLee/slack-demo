import database as db
from channel import channel_join
from error import InputError
from error import AccessError

def channels_list(token):
    # check if token is valid
    try:
        u_id = int(token)
    except:
        raise AccessError #invalid token
    valid_user = 0
    for user in db.master_users:
        if user['u_id'] == u_id and user['log'] == True:
            valid_user = 1 # 'log' == True if logged in
    if valid_user != 1:
        raise AccessError
    
    channels = []
    for key in db.channels_and_members:
        for member in db.channels_and_members[key][1]:
            if member['u_id'] == u_id:
                i = 0
                while db.channels[i]['channel_id'] != key:
                    i = i + 1
                channels.append(db.channels[i])
    
    return {
        'channels': channels,
    }


def channels_listall(token):
    try:
        u_id = int(token)
    except:
        raise AccessError #invalid token
    valid_user = 0
    for user in db.master_users:
        if user['u_id'] == u_id and user['log'] == True:
            valid_user = 1 # 'log' == True if logged in
    if valid_user != 1:
        raise AccessError
             
    return {
        'channels': db.channels
    }


def channels_create(token, name, is_public):
    ## check valid token
    try:
        u_id = int(token)
    except:
        raise AccessError
    
    ## check user exists (not currently working, idk)
    user_exists = 0
    for user in db.master_users:
        if user['u_id'] == u_id and user['log'] == True:
            user_exists = 1 # 'log' == True if logged in
    if user_exists != 1:
        raise AccessError   
    
    ## check valid name
    if len(name) > 20 or len(name) == 0:
        raise InputError

    ## add channel details
    channel_id = len(db.channels) - 1

    channel = {}
    channel['channel_id'] = channel_id
    channel['name'] = name

    ## add to various lists
    # extract member details from user
    member = {}
    name_first = db.master_users[u_id]['name_first']
    name_last = db.master_users[u_id]['name_last']
    member['u_id'] = u_id
    member['name_first'] = name_first
    member['name_last'] = name_last
    members = [member]
    db.channels_and_members[channel_id] = [members, members]
    db.channels.append(channel)
    if is_public == True:
        db.public_channels.append(channel)
    elif is_public == False:
        db.private_channels.append(channel)

    ## add creator as owner
    channel_join(token, channel_id)

    return {
        'channel_id': channel_id, # is this right?
    }