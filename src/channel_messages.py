import database_edited as db
from error import InputError
from error import AccessError

'''
# TO PUT IN DATABASE
channels_and_messages = { channel_id: messages, channel_id2: messages2, ... }
channels_and_messages = { 1: [ { 'message_id': 1, 'u_id': 1, 'message' = 'whtever the fuck', 'time_created' = 1111111111 }, { 'message_id': 2, ... } ... ], 2: ... }
'''

def channel_messages(token, channel_id, start):

    ## check valid token
    try:
        u_id = int(token)
    except:
        raise AccessError 

    ## check if user is a member of channel/ if channel exists
    access = 0
    try:
        for member in db.channels_and_members[channel_id][1]:
            if member['u_id'] == u_id:
                access = 1
    except:
        raise InputError # channel doesn't exist
    if access == 0:
        raise AccessError # user is not a member

    messages = db.channels_and_messages[channel_id]

    ## check 'start' isn't greater than total # of messages
    message_count = max(messages, key = int)
    if start > message_max:
        raise InputError

    messages_return = []
    current = start
    while (current <= message_max) and (current < start + 50):
        messages_return.append(messages[current])
        current += 1
    current -= 1 # because we went one too far at the end

    return { 'messages': messages_return, 'start': start, 'end': current, }
'''
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
        'start': 0,
        'end': 50,
    }
'''