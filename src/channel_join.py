import database_edited as db
from error import InputError
from error import AccessError

def channel_join(token, channel_id):

    u_id = token
    if_in = 0
    try :
        for member in db.channels_and_members[channel_id][1]:
            if member['u_id'] == u_id:
                if_in = 1
    except:
        raise InputError
    if if_in != 1 :
        return {} 
    '''dont know how to check if private for a channel and also global
        somehow access error is meant to fit here too
    '''
    elif if_in == 0 :
        member = {'u_id' : u_id}
        member_copy = member.copy()
        db.channels_and_members[channel_id][1].append(member_copy)
    