import database as db
from error import InputError
from error import AccessError

def channel_invite(token, channel_id, u_id):
    # can only invite if member of channel
    #instantly join once invited - wouldnt be owner because not the first in

    u_id_inviter = token_check(token)
    token_user_exist_check(u_id_inviter)
    
    valid_channel(channel_id)
    inviter_in_check(channel_id, u_id_inviter)
    user_exist_check(u_id)
    add_required = no_add_required(channel_id, u_id)
    if (add_required == 0):
        return {}

    #find user and make member
    member ={}
    for user in db.master_users:
        if user['u_id'] == u_id:
            member['u_id'] = u_id
            member['name_first'] = user['name_first']
            member['name_last'] = user['name_last']
    # join to all_members:
    db.channels_and_members[channel_id][1].append(member)
    return {}


def channel_details(token, channel_id):
    
    u_id = token_check(token)
        
    token_user_exist_check(u_id)
    valid_channel(channel_id)
    in_all_members(channel_id, u_id)
    for channel in db.channels:
        if channel['channel_id'] == channel_id:
            name = channel['name']
            

        
    return {'name': name, 'owner_members': db.channels_and_members[channel_id][0], 'all_members' : db.channels_and_members[channel_id][1] }
    


def channel_messages(token, channel_id, start):
    ## check valid token
    u_id = token_check(token)

    token_user_exist_check(u_id)
    
    ## check if user is a member of channel/ if channel exists
    valid_channel(channel_id)
    in_all_members(channel_id, u_id)

    if start < 0:
        raise InputError

    messages = db.channels_and_messages[channel_id]

    ## check 'start' isn't greater than total # of messages OR negative
    message_max = len(messages)
    if start > message_max:
        raise InputError

    messages_return = []
    current = start
    while (current <= message_max) and (current < start + 50):
        messages_return.append(messages[current])
        current += 1
    
    # if we have reached the final message, return -1
    if current > message_max:
        current = -1

    return { 'messages': messages_return, 'start': start, 'end': current, }


def channel_leave(token, channel_id):
   #input error if not valid channel id (channel does not exist)
   #access error if user is not part of the channel_id (channel exists). remember to remove from owner if they are owner too. need to check that within code

    u_id = token_check(token)
    
    token_user_exist_check(u_id)

    valid_channel(channel_id)
    in_all_members(channel_id, u_id)
    #search public channels and need to update found after private search too or else return input error
    for channel in db.public_channels:
        owner_exists = 0
        #check if owner
        for owner in db.channels_and_members[channel_id][0]:
            if owner['u_id'] == u_id:
                owner_exists = 1
        if owner_exists == 1:
            #removal from owners 
            for user in db.channels_and_members[channel_id][0]:
                if user['u_id'] == u_id:
                    db.channels_and_members[channel_id][0].remove(user)
        #removal from all members 
        for user in db.channels_and_members[channel_id][1]:
            if user['u_id'] == u_id:
                db.channels_and_members[channel_id][1].remove(user)
            if len(db.channels_and_members[channel_id][1]) == 0 :
                del db.channels_and_members[channel_id]
                del db.public_channels[channel_id]
                del db.channels[channel_id]
    
    #if reached this point, means that channel/user could possibly be in private channel

    for channel in db.private_channels:   
        owner_exists = 0
        #check if owner
        for owner in db.channels_and_members[channel_id][0]:
            if owner['u_id'] == u_id:
                owner_exists = 1
        if owner_exists == 1:
            #removal from owners 
            for user in db.channels_and_members[channel_id][0]:
                if user['u_id'] == u_id:
                    db.channels_and_members[channel_id][0].remove(user)
                    
        #removal from all members 
        for user in db.channels_and_members[channel_id][1]:               
            if user['u_id'] == u_id:
                db.channels_and_members[channel_id][1].remove(user)
            if len(db.channels_and_members[channel_id][1]) == 0 :
                del db.channels_and_members[channel_id]
                del db.private_channels[channel_id]
                del db.channels[channel_id]
    


    return {}


def channel_join(token, channel_id):
    # can only join if channel is public and go in all_members
    # UNLESS they are the flock owner, then can join private too and go in all_members
    u_id = token_check(token)
    
    # check if the user is valid
    token_user_exist_check(u_id)

    # check whether user has joined the channel already
    valid_channel(channel_id)
    
    add_required = no_add_required(channel_id, u_id)
    if (add_required == 0):
        return {}
 
    for channel in db.public_channels:
        if channel['channel_id'] == channel_id:
            if db.master_users[0]['u_id'] == u_id:
                #  join as normal
                member ={}
                member['u_id'] = u_id
                member['name_first'] = db.master_users[0]['name_first']
                member['name_last'] = db.master_users[0]['name_last']
                # join to all_members:
                db.channels_and_members[channel_id][1].append(member)
            elif db.master_users[0]['u_id'] != u_id:
                    #  join as normal member only
                    member ={}
                    for user in db.master_users:
                        if user['u_id'] == u_id:
                            member['u_id'] = u_id
                            member['name_first'] = user['name_first']
                            member['name_last'] = user['name_last']
                    # join to all_members:
               
                    db.channels_and_members[channel_id][1].append(member)
            return {}
        
    # means that the channel is a private channel because it exists yet is not in public
    # if not flockr owner:
    if db.master_users[0]['u_id'] != u_id:
        raise AccessError
    
    # means the channel is private AND flockr owner
    for channel in db.private_channels:
        if channel['channel_id'] == channel_id:
            #  join as owner of channel and normal
            member = {}
            member['u_id'] = u_id
            member['name_first'] = db.master_users[0]['name_first']
            member['name_last'] = db.master_users[0]['name_last']
            # join to all_members:
            db.channels_and_members[channel_id][1].append(member)
            return {}

    return {}


def channel_addowner(token, channel_id, u_id):
    # can only add owner if token is already an owner of channel or owner of flockr
    # u_id becomes owner
    u_id_inviter = token_check(token)     
    token_user_exist_check(u_id_inviter)    
    if_in = 0
    try:
        for member in db.channels_and_members[channel_id][0]:
            if member['u_id'] == u_id_inviter:
                if_in = 1 #invitee is an owner of channel
            if member['u_id'] == u_id: # invited person is already an owner of channel
                raise InputError
    except:
        raise InputError #channel_id doesnt exist / invitee person is already owner
     
    if u_id_inviter == db.master_users[0]['u_id']: # inviter is flockr owner
        if_in = 1
            
    if if_in != 1: 
        raise AccessError
    
    valid_user = 0
    new_owner = {}
    for user in db.master_users:
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
    return {}


def channel_removeowner(token, channel_id, u_id):
   #input error if not valid channel id (channel does not exist), CASE2 : if removed u_id is not an owner of the channel
   #access error token is not global or local owner
    u_id_inviter = token_check(token)

    token_user_exist_check(u_id_inviter)
    
    token_if_in = 0
    invited_if_in = 0
    try:
        for member in db.channels_and_members[channel_id][0]:
            if member['u_id'] == u_id_inviter:
                token_if_in = 1 #inviter is an owner of channel
            if member['u_id'] == u_id: # owner to be removed is in the channel
                invited_if_in = 1
    except:
        raise InputError #channel_id doesnt exist 
                   
    if token_if_in != 1 and db.master_users[0]['u_id'] != u_id_inviter: 
        #checking if possibly global owner
        raise AccessError
    
    if invited_if_in != 1 : #does u_id exist in the 'owners of channel'
        raise InputError

    for user in db.channels_and_members[channel_id][0]:
        if user['u_id'] == u_id:
            db.channels_and_members[channel_id][0].remove(user)

    return {}






##HELPER FUNCTIONS BELOW

def token_check(token):
    try:
        u_id_inviter = int(token)
    except:
        raise AccessError #invalid token
    return u_id_inviter

def token_user_exist_check(u_id_inviter):
    if_in = 0
    for user in db.master_users:
        if user['u_id'] == u_id_inviter and user['log'] == True:
            if_in = 1 # 'log' == True if logged in
    if if_in != 1:
        raise AccessError #u_id_invitee doesnt exist

def user_exist_check(u_id):
    if_in = 0
    for user in db.master_users:
        if user['u_id'] == u_id:
                if_in = 1
    if if_in != 1: 
        raise InputError

def inviter_in_check(channel_id, u_id_inviter):
    if_in = 0
    for member in db.channels_and_members[channel_id][1]:
        if member['u_id'] == u_id_inviter:
            if_in = 1

    if if_in != 1: 
        raise AccessError

def in_all_members(channel_id, u_id):
    if_in = 0
    for member in db.channels_and_members[channel_id][1]:
        if member['u_id'] == u_id:
            if_in = 1
        
            
    if if_in != 1: 
        raise AccessError # user is not a member OR invalid token


def no_add_required(channel_id, u_id):
    if_in = 0
    for member in db.channels_and_members[channel_id][1]:
        if member['u_id'] == u_id:
            if_in = 1
            return 0 #return 1 if they are already added in channel

    return 1

def valid_channel(channel_id):
    try:
        return db.channels_and_members[channel_id]
    except: 
        raise InputError
