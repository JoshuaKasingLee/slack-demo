import database_edited as db
from error import InputError
from error import AccessError

def channel_addowner(token, channel_id, u_id):
    # can only add owner if token is already an owner of channel or owner of flockr
    # u_id becomes owner
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
    #print(db.channels_and_members[channel_id][0])
    try:
        for member in db.channels_and_members[channel_id][0]:
            if member['u_id'] == u_id_invitee:
                if_in = 1 #invitee is an owner of channel
            if member['u_id'] == u_id: # invited person is already an owner of channel
                raise InputError
    except:
        raise InputError #channel_id doesnt exist / invited person is already owner
     
    if u_id_invitee == db.users[0]['u_id']: # invitee is flockr owner
        if_in = 1
            
    if if_in != 1: 
        #print(if_in)
        raise AccessError
    
    valid_user = 0
    new_owner ={}
    for user in db.users:
        if user['u_id'] == u_id:
            new_owner['u_id'] = u_id
            new_owner['name_first'] = user['name_first']
            new_owner['name_last'] = user['name_last']
            valid_user = 1
    if valid_user != 1:
        raise InputError #the person youre trying to add doesnt exist ie u_id isnt valid 
   
    #join to owner members, and maybe all members if not already part of channel
    db.channels_and_members[channel_id][0].append(new_owner)
    in_all = 0
    for member in db.channels_and_members[channel_id][1]:
            if member['u_id'] == u_id: # invited person is already a member of channel                    
                in_all = 1
    if in_all == 0:
        db.channels_and_members[channel_id][1].append(new_owner)
    #print(db.channels_and_members)     
    return {
    }

"""
Assumptions:
    Assuming an Input Error is returned if a u_id which isnt registered is entered
    
    Assuming someone not a member of a channel can become owner if called add_owner upon,
    subsequently getting added to all_members as well.
    
    Assuming that the flockr owner can make another u_id an owner of a channel the flockr owner 
    has'nt joined yet. This assumptions comes from the fact that the global permissions of
    flockr owner is that they can edit other owners permissions, and global permissions come
    before channel permissions which implies flockr owner has power over all owners, not just
    the ones of channels theyve joined.
"""
#channel_addowner('1', 2, 3)