import database_edited_for_channels as db
from error import AccessError


def channels_list(token):
    
    try:
        u_id = int(token)
    except:
        raise AccessError #invalid token
    valid_user = 0
    for user in db.users:
        if user['u_id'] == u_id:
            valid_user = 1
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
