import database_edited_for_channels as db
import auth
import channel
from error import InputError
from error import AccessError
'''
assumptions:
    duplicate channel names are allowed
    empty character names are not allowed
'''
def channels_create(token, name, is_public):

    ## check valid token
    try:
        u_id = int(token)
    except:
        raise AccessError
    
    ## check user exists (not currently working, idk)
    user_exists = 0
    for user in db.users:
        if user['u_id'] == u_id:
            user_exists = 1
    if user_exists != 1:
        raise AccessError   
    
    ## check valid name
    if len(name) > 20 or len(name) == 0:
        raise InputError

    ## add channel details
    channel_id = len(db.channels) + 1

    channel = {}
    channel['channel_id'] = channel_id
    channel['name'] = name

    ## add to various lists
    # extract member details from user
    name_first = users[u_id]['name_first']
    name_last = users[u_id]['name_last']
    member = { u_id, name_first, name_last }
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