import database as db
from error import InputError
from error import AccessError

def message_send(token, channel_id, message):
    # First that the user is in the channel_id
    # To do this we find the u_id through the token
    # Either call a function in the database or copy and paste this
    u_id_exists = False
    for user in db.master_users:
        if user['token'] == token:
            u_id = user['u_id']
            u_id_exists = True
    # If u_id does not exist, the user does not exist
    assert(u_id_exists == True)

    u_id_exists = False

    # Make sure a channel exists
    channel_exists = len(db.channels)
    assert(channel_exists > 0)

    # Now check if the user exists in the channel_id
    for user in db.channels_and_members[channel_id][1]:
        if u_id == user['u_id']:
            u_id_exists = True

    # Raise AccessError if the user is not part of the channel they are trying to post in
    if u_id_exists == False:
        raise AccessError(f"Error, u_id:{u_id} cannot post in a channel they have not joined. The channel has channel_id: {channel_id}.")

    # Now check that the message is not longer than 1000 characters
    message_length = len(message)
    if message_length > 1000:
        raise InputError(f"Error, the message exceeds the 1000 character limit. You have input {message_length} characters.")

    # Otherwise message is valid
    # Create message_id. This is done by incrementing the number of messages in channels_and_messages.
    message_id = len(db.messages)

    message_package = {
        'channel_id': channel_id,
        'u_id': u_id,
        'message': message,
        'deleted': False,
    }
    db.messages[f'{message_id}'] = message_package

    return {
        'message_id': message_id,
    }

# Assumptions for message_send
'''
I assume that checking whether the channel_id is valid first has a higher priority than message length
'''

def message_remove(token, message_id):
    # Conditions to prevent Access Error:
    # - Request made by the authorised user making the request
    # - Authorised user is an owner of the channel or the flokr

    # Check to see if the user is an owner of this channel
    # First that the user is in the channel_id
    # To do this we find the u_id through the token
    # Either call a function in the database or copy and paste this
    u_id_exists = False
    for user in db.master_users:
        if user['token'] == token:
            u_id = user['u_id']
            u_id_exists = True
    # If u_id does not exist, the user does not exist
    assert(u_id_exists == True)

    # Make sure a channel exists
    channel_exists = len(db.channels)
    assert(channel_exists > 0)

    # If a message doesn't exist, return input error
    if f'{message_id}' not in db.messages:
        raise InputError(f"Error, the message does not exist")
    elif db.messages[f'{message_id}']['deleted'] == True:
        raise InputError(f"Error, the message has already been deleted")

    # We have to find the channel_id using message_id
    channel_id = db.messages[f'{message_id}']['channel_id']

    # Reinitialise u_id_exists to False
    u_id_exists = False
    
    # Now check if the user is the owner of the channel_id
    for user in db.channels_and_members[channel_id][0]:
        if u_id == user['u_id']:
            u_id_exists = True

    # Raise AccessError if the user is not part of the channel they are trying to post in
    if u_id_exists == False:
        raise AccessError(f"Error, u_id:{u_id} cannot remove a message in a channel they are not the owner of. The channel has channel_id: {channel_id}.")

    # Next, we find the message using message_id and change the deleted field to 'True'
    db.messages[f'{message_id}']['deleted'] = True

    return {
    }

'''
[NOPE] AccessError is of higher priority than Input Error
'''


def message_edit(token, message_id, message):
    # Message is editable if and only if the user is an owner of the channel
    
    # First check if the message exists
    # If a message doesn't exist, return input error
    if f'{message_id}' not in db.messages:
        raise InputError(f"Error, the message does not exist")
    elif db.messages[f'{message_id}']['deleted'] == True:
        raise InputError(f"Error, the message has already been deleted")
    
    # Check to see if the user is an owner of this channel
    # First that the user is in the channel_id
    # To do this we find the u_id through the token
    # Either call a function in the database or copy and paste this
    u_id_exists = False
    for user in db.master_users:
        if user['token'] == token:
            u_id = user['u_id']
            u_id_exists = True
    # If u_id does not exist, the user does not exist
    assert(u_id_exists == True)

    # Make sure a channel exists
    channel_exists = len(db.channels)
    assert(channel_exists > 0)

    # We have to find the channel_id using message_id
    channel_id = db.messages[f'{message_id}']['channel_id']

    # Reinitialise u_id_exists to False
    u_id_exists = False
    
    # Now check if the user is the owner of the channel_id
    for user in db.channels_and_members[channel_id][0]:
        if u_id == user['u_id']:
            u_id_exists = True

    # Raise AccessError if the user is not part of the channel they are trying to post in
    if u_id_exists == False:
        raise AccessError(f"Error, u_id:{u_id} cannot edit a message in a channel they are not the owner of. The channel has channel_id: {channel_id}.")

    # Otherwise edit the message
    db.messages[f'{message_id}']['message'] = message

    return {
    }


'''
Input error if message does not exist
No action required if message input was the same as message in the database
'''