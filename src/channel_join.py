import database_edited as db
from error import InputError
from error import AccessError

def channel_join(token, channel_id):
    # can only join if channel is public and go in all_members
    # UNLESS they are the flock owner, then can join private too and go in owner_members + all_members
    #print( db.channels_and_members)
    try:
        u_id = int(token)
    except:
        raise AccessError #invalid token
        
    try :
        for member in db.channels_and_members[channel_id][1]:
            if member['u_id'] == u_id:
                return { # already joined
                }
    except:
        raise InputError #channel deosnt exist

    for channel in db.public_channels:
        if channel['channel_id'] == channel_id:
            if db.users[0]['u_id'] == u_id:
                #  join as owner of channel and normal
                member ={}
                member['u_id'] = u_id
                member['name_first'] = db.users[0]['name_first']
                member['name_last'] = db.users[0]['name_last']
                # join to all_members:
                db.channels_and_members[channel_id][1].append(member)
                # join to owner_members:
                db.channels_and_members[channel_id][0].append(member)
                #print(f"owner + public {db.channels_and_members}")
            elif db.users[0]['u_id'] != u_id:
                    #  join as normal member only
                    valid_user = 0
                    member ={}
                    for user in db.users:
                        if user['u_id'] == u_id:
                            member['u_id'] = u_id
                            member['name_first'] = user['name_first']
                            member['name_last'] = user['name_last']
                            valid_user = 1
                    if valid_user != 1:
                        raise AccessError #user doesnt exist ie user token isnt valid 
                    # join to all_members:                    
                    db.channels_and_members[channel_id][1].append(member)
                    #print(f"normal {db.channels_and_members}")
            return {
            }
        
    # means that the channel is a private channel because it exists yet is not in public
    # if not flockr owner:
    if db.users[0]['u_id'] != u_id:
        raise AccessError
    
    # means the channel is private AND flockr owner
    for channel in db.private_channels:
        if channel['channel_id'] == channel_id:
             #  join as owner of channel and normal
             member ={}
             for user in db.users:
                 if user['u_id'] == u_id:
                     member['u_id'] = u_id
                     member['name_first'] = user['name_first']
                     member['name_last'] = user['name_last']
             # join to all_members:
             db.channels_and_members[channel_id][1].append(member)
             # join to owner_members:
             db.channels_and_members[channel_id][0].append(member)
             #print(f"owner + priate {db.channels_and_members}")
             return {
             }

"""
Assumptions:
    token is the same as u_id
    flockr owner can join private channels as well
"""
#channel_join('1', 2 )