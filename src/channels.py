import database as db
from channel import channel_join
from error import InputError
from error import AccessError

def channels_list(token):

    u_id = token_check(token)
    user_exist_check(u_id)

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

    u_id = token_check(token)
    user_exist_check(u_id)
             
    return {
        'channels': db.channels
    }


def channels_create(token, name, is_public):

    u_id = token_check(token)
    user_exist_check(u_id) 
    
    ## check valid name
    if len(name) > 20 or len(name) == 0:
        raise InputError

    ## add channel details
    channel_id = len(db.channels)
    channel = {}
    channel['channel_id'] = channel_id
    channel['name'] = name

    ## add to database
    name_first = db.master_users[u_id]['name_first']
    name_last = db.master_users[u_id]['name_last']
    member = {}
    member['u_id'] = u_id
    member['name_first'] = name_first
    member['name_last'] = name_last
    db.channels_and_members[channel_id] = [[member], [member]]
    db.channels.append(channel)
    if is_public == True:
        db.public_channels.append(channel)
    elif is_public == False:
        db.private_channels.append(channel)

    ## add creator as owner
    channel_join(token, channel_id)

    return {
        'channel_id': channel_id,
    }

def token_check(token):
    ''' check if the token string is a valid integer'''
    try:
        u_id = int(token)
    except:
        raise AccessError #invalid token
    return u_id

def user_exist_check(u_id):
    ''' check if a user exists for the given u_id'''
    valid_user = 0
    for user in db.master_users:
        if user['u_id'] == u_id and user['log'] == True:
            valid_user = 1 # 'log' == True if logged in
    if valid_user != 1:
        raise AccessError