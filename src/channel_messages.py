import database_edited as db
from error import InputError
from error import AccessError

'''
# TO PUT IN DATABASE
#channels_and_messages = { channel_id: messages, channel_id2: messages2, ... }
#channels_and_messages = { 1: [ { 'message_id': 1, 'u_id': 1, 'message' = 'whtever the fuck', 'time_created' = 1111111111 }, { 'message_id': 2, ... } ... ], 2: ... }
channels_and_messages = {}

assumptions: we can only return 50 messages. between start and start+50 there are either 51 or 49 (inclusive or exclusive).
i will return between start and start+49 inclusive, with end index = start+50 (or whatever it happens to be, depending on message count).
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