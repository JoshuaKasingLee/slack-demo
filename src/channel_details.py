import database_edited as db
from error import InputError
from error import AccessError


def channel_details(token, channel_id):
    
    u_id = token
    db.channels_and_members
    if_in = 0
    try:
        for member in db.channels_and_members[channel_id][1]:
            if member['u_id'] == u_id:
                if_in = 1
    except:
        raise InputError
        
            
    if if_in != 1: 
        raise AccessError
    
    global channels
    for channel in db.channels:
        if channel['channel_id'] == channel_id:
            name = channel['name']
        
        
    return {'name': name, 'owner_members': db.channels_and_members[channel_id][0], 'all_members' : db.channels_and_members[channel_id][1] }
    
    """"
    return {
        'name': 'Hayden',
        'owner_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
        'all_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
    }
    """

"""
Assumptions:
    
    token is same as u_id
    
"""
#print(channel_details(1, 1)) #testing