import database_edited_for_channels as db
from error import AccessError


def channels_listall(token):
    
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
             
    return {
        'channels': db.channels
    }
