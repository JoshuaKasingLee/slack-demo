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
    ''' 
    ## check user exists
    user_exists = 0
    for user in db.users:
        if user['u_id'] == u_id:
            user_exists = 1
    if user_exists == 0:
        raise AccessError   
    '''
    ## check valid name
    if len(name) > 20 or len(name) == 0:
        raise InputError
    '''
    ## check name not already taken
    for channel in db.channels:
        if channel['name'] == name:
            raise InputError
    '''
    ## add channel details
    channel_id = len(db.channels) + 1

    channel = {}
    channel['channel_id'] = channel_id
    channel['name'] = name

    ## add to various lists

    db.channels_and_members[channel_id] = [[],[],]
    db.channels.append(channel.copy())
    if is_public == True:
        db.public_channels.append(channel.copy())
    elif is_public == False:
        db.private_channels.append(channel.copy())

    ## add creator as owner
    channel_join(token, channel_id)

    return {
        'channel_id': channel_id, # is this right?
    }

user1_token = auth.auth_register('user1@example.com', 'password', 'user1', 'name')['token']
print(channels_create(user1_token, 'exceptionalll', True))