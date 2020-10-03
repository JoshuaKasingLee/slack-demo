import database as db
from error import InputError
from error import AccessError

def channel_leave(token, channel_id):
   #input error if not valid channel id (channel does not exist)
   #access error if user is not part of the channel_id (channel exists). remember to remove from owner if they are owner too. need to check that within code

    try:
        u_id = int(token)
    except:
        raise AccessError #invalid token
    
    channel_found = 0
    user_found = 0
    #search public channels and need to update found after private search too or else return input error
    for channel in db.public_channels:
        if channel['channel_id'] == channel_id:
            channel_found = 1
            #check if owner
            if db.users[0]['u_id'] == u_id:
                #removal from owners 
                for user in db.channels_and_members[channel_id][0]:
                    if master_users['u_id'] == u_id:
                        db.channels_and_members[channel_id][0].remove(user)
            #removal from all members 
            for user in db.channels_and_members[channel_id][1]:
                if master_users['u_id'] == u_id:
                    db.channels_and_members[channel_id][1].remove(user)
                    user_found = 1
    
    #if reached this point, means that channel/user could possibly be in private channel

    for channel in db.private_channels:
        if channel['channel_id'] == channel_id:
            channel_found = 1
            
            #check if owner
            if db.users[0]['u_id'] == u_id:
                #removal from owners 
                
                for user in db.channels_and_members[channel_id][0]:
                    if master_users['u_id'] == u_id:
                        db.channels_and_members[channel_id][0].remove(user)
                        
            #removal from all members 
            for user in db.channels_and_members[channel_id][1]:
                #print("yay")
                if master_users['u_id'] == u_id:
                    db.channels_and_members[channel_id][1].remove(user)
                    user_found = 1
                    

    if channel_found != 1 :
        raise InputError
    if user_found != 1 :
        raise AccessError

    return {
    }


