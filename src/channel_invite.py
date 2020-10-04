import database_edited as db
from error import InputError
from error import AccessError

def channel_invite(token, channel_id, u_id):
    # can only invite if member of channel
    #instantly join once invited - wouldnt be owner because not the first in
    #print(db.channels_and_members)
    try:
        u_id_invitee = int(token)
    except:
        raise AccessError #invalid token
     
    if_in = 0
    for user in db.users:
        if user['u_id'] == u_id_invitee:
            if_in = 1
    if if_in != 1:
        raise AccessError #u_id_invitee doesnt exist
    
    if_in = 0
    try:
        for member in db.channels_and_members[channel_id][1]:
            if member['u_id'] == u_id_invitee:
                if_in = 1
            if member['u_id'] == u_id: # already in channel
                return{
                }
    except:
        raise InputError
                   
    if if_in != 1: 
        raise AccessError
    
    if_in = 0
    for user in db.users:
        if user['u_id'] == u_id:
                if_in = 1
    if if_in != 1: 
        raise InputError
     
    #find user and make member
    member ={}
    for user in db.users:
        if user['u_id'] == u_id:
            member['u_id'] = u_id
            member['name_first'] = user['name_first']
            member['name_last'] = user['name_last']
    # join to all_members:
    db.channels_and_members[channel_id][1].append(member)
    #print(db.channels_and_members)
    return {
        
    }

"""
Assumptions:
    token is the same as u_id
"""
#channel_invite(2, 1, 3)
#print(db.channels_and_members)