import database
from error import InputError
from error import AccessError

def channel_invite(token, channel_id, u_id):
    # can only invite if member of channel
    #instantly join once invited - wouldnt be owner because not the first in

    u_id_inviter = token_check(token)
    database.channel_token_user_exist_check(u_id_inviter)
    
    database.channel_valid_channel(channel_id)
    database.channel_inviter_in_check(channel_id, u_id_inviter)
    database.channel_user_exist_check(u_id)
    add_required = database.channel_no_add_required(channel_id, u_id)
    if (add_required == 0):
        return {}

    #find user and make member
    member = database.channel_find_user(u_id)

    # join to all_members:
    database.channel_join_members(channel_id, member)

    return {}


def channel_details(token, channel_id):
    
    u_id = token_check(token)
        
    database.channel_token_user_exist_check(u_id)
    database.channel_valid_channel(channel_id)
    database.channel_in_all_members(channel_id, u_id)

    name = database.channel_fetch_name(channel_id)
    owner_members = database.channel_fetch_owners(channel_id)
    members = database.channel_fetch_members(channel_id)
        
    return {'name': name, 'owner_members': owner_members, 'all_members' : members}


def channel_messages(token, channel_id, start):
    ## check valid token
    u_id = token_check(token)

    database.channel_token_user_exist_check(u_id)
    
    ## check if user is a member of channel/ if channel exists
    database.channel_valid_channel(channel_id)
    database.channel_in_all_members(channel_id, u_id)

    if start < 0:
        raise InputError

    messages = database.channel_fetch_messages(channel_id)

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
    
    database.channel_token_user_exist_check(u_id)

    database.channel_valid_channel(channel_id)
    database.channel_in_all_members(channel_id, u_id)

    database.channel_remove_member(channel_id, u_id)

    return {}


def channel_join(token, channel_id):
    # can only join if channel is public and go in all_members
    # UNLESS they are the flock owner, then can join private too and go in all_members
    u_id = token_check(token)
    
    # check if the user is valid
    database.channel_token_user_exist_check(u_id)

    # check whether user has joined the channel already
    database.channel_valid_channel(channel_id)
    
    add_required = database.channel_no_add_required(channel_id, u_id)
    if (add_required == 0):
        return {}
 
    joined = database.channel_add_member(channel_id, u_id)

    if joined == True:
        return {}
        
    # if not returned means that the channel is private
    # because it exists yet is not public

    # if not flockr owner:
    if database.channel_check_flockr_owner(u_id) == False:
        raise AccessError
    
    # means the channel is private AND flockr owner
    database.channel_add_member_private(channel_id, u_id)

    return {}


def channel_addowner(token, channel_id, u_id):
    # can only add owner if token is already an owner of channel or owner of flockr
    # u_id becomes owner
    u_id_inviter = token_check(token)
    database.channel_token_user_exist_check(u_id_inviter)

    if_in = database.channel_if_owner(u_id_inviter, channel_id)
    
    if database.channel_check_flockr_owner(u_id_inviter) == True:
        if_in = 1
            
    if if_in != 1: 
        raise AccessError

    valid_user, new_owner = database.channel_check_valid_user(u_id)

    if valid_user != 1:
        raise InputError # u_id does not exist 
    
    database.channel_add_owner(new_owner, u_id, channel_id)

    return {}


def channel_removeowner(token, channel_id, u_id):
   #input error if not valid channel id (channel does not exist), CASE2 : if removed u_id is not an owner of the channel
   #access error token is not global or local owner
    u_id_inviter = token_check(token)

    database.channel_token_user_exist_check(u_id_inviter)
    
    token_if_in, invited_if_in = database.channel_check_owners(u_id_inviter, u_id, channel_id)
    
    inviter_is_owner = database.channel_check_flockr_owner(u_id_inviter)

    if token_if_in != 1 and inviter_is_owner == False: 
        # if not global owner or current owner
        raise AccessError
    
    if invited_if_in != 1: #does u_id exist in the 'owners of channel'
        raise InputError

    database.channel_remove_owner(u_id, channel_id)

    return {}


# HELPER FUNCTIONS BELOW #

def token_check(token):
    try:
        u_id_inviter = int(token)
    except:
        raise AccessError #invalid token
    return u_id_inviter
