import database_edited as db
from error import InputError
from error import AccessError

def channel_removeowner(token, channel_id, u_id):
   #input error if not valid channel id (channel does not exist), CASE2 : if removed u_id is not an owner of the channel
   #access error token is not global or local owner
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
    
    token_if_in = 0
    invited_if_in = 0
    #print(db.channels_and_members[channel_id][0])
    try:
        for member in db.channels_and_members[channel_id][0]:
            if member['u_id'] == u_id_invitee:
                token_if_in = 1 #invitee is an owner of channel
            if member['u_id'] == u_id: # owner to be removed is in the channel
                invited_if_in = 1
    except:
        raise InputError #channel_id doesnt exist 
                   
    if token_if_in != 1 and db.users[0]['u_id'] != u_id_invitee: 
        #checking if possibly global owner
        raise AccessError
    
    if invited_if_in != 1 : #does u_id exist in the 'owners of channel'
        raise InputError

    for user in db.channels_and_members[channel_id][0]:
        if user['u_id'] == u_id:
            db.channels_and_members[channel_id][0].remove(user)

    return {
    }

#print(db.channels_and_members)
#channel_removeowner('1', 3, 3)
#print ("yay")
#print(db.channels_and_members)