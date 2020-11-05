import database
from error import InputError
from error import AccessError
import time
import threading

def message_send(token, channel_id, message):
    # First that the user is in the channel_id
    # To do this we find the u_id through the token
    # Either call a function in the database or copy and paste this
    # If u_id does not exist, the user does not exist
    assert(database.message_user_exists(token) == True)

    # Find u_id from token
    u_id = database.convert_from_tok_to_u_id(token)

    # Make sure a channel exists
    assert(database.message_channel_exists() == True)

    # # Now check if the user exists in the channel_id
    u_id_is_member = database.message_user_is_member(u_id, channel_id)
    
    # Raise AccessError if the user is not part of the channel they are trying to post in
    if u_id_is_member == False:
        raise AccessError(f"Error, u_id:{u_id} cannot post in a channel they have not joined. The channel has channel_id: {channel_id}.")

    # Now check that the message is not longer than 1000 characters
    message_length = len(message)
    if message_length > 1000:
        raise InputError(f"Error, the message exceeds the 1000 character limit. You have input {message_length} characters.")

    # Otherwise message is valid

    # Create message_id. This is done by incrementing the number of messages in channels_and_messages.
    message_id = database.message_new_message_id()

    message_package = {
        'message_id': message_id,
        'channel_id': channel_id,
        'u_id': u_id,
        'message': message,
        'time_created': time.time(),
        'reacts': [{'react_id': 1, 'u_ids': None, 'is_this_user_reacted': False }],
        'is_pinned': False,
    }
    database.messages[f'{message_id}'] = message_package

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
    assert(database.message_user_exists(token) == True)

    # Find u_id from token
    u_id = database.convert_from_tok_to_u_id(token)

    # # Make sure a channel exists
    assert(database.message_channel_exists() == True)

    # If a message doesn't exist, return input error
    if database.message_message_exist(message_id) == False:
        raise InputError(f"Error, the message does not exist")


    # We have to find the channel_id using message_id
    channel_id = database.message_channel_id_from_message_id(message_id)    
    
    # Check if u_id is admin, if not, raise AccessError
    u_id_is_admin = database.message_user_is_admin(u_id)

    # Now check if the user is the owner of the channel_id
    u_id_is_owner = database.message_user_is_owner(u_id, channel_id)

    # Raise AccessError if the user is not part of the channel they are trying to post in
    if u_id_is_owner == False and u_id_is_admin == False:            
        raise AccessError(f"Error, u_id:{u_id} cannot remove a message in a channel they are not the owner of. The channel has channel_id: {channel_id}.")

    # Next, we find the message using message_id and change the deleted field to 'True'
    database.message_delete_message(message_id)

    return {
    }

'''
[NOPE] AccessError is of higher priority than Input Error
'''


def message_edit(token, message_id, message):
    # Message is editable if and only if the user is an owner of the channel
    
    # First check if the message exists
    # If a message doesn't exist, return input error
    if database.message_message_exist(message_id) == False:
        raise InputError(f"Error, the message does not exist")
    
    # Check to see if the user is an owner of this channel
    # First that the user is in the channel_id
    # To do this we find the u_id through the token
    # Either call a function in the database or copy and paste this
    assert(database.message_user_exists(token) == True)

    # Find u_id from token
    u_id = database.convert_from_tok_to_u_id(token)

    # Make sure a channel exists
    assert(database.message_channel_exists() == True)

    # We have to find the channel_id using message_id
    channel_id = database.message_channel_id_from_message_id(message_id)

    # Check if u_id is admin, if not, raise AccessError
    u_id_is_admin = database.message_user_is_admin(u_id)

    # Now check if the user is the owner of the channel_id
    u_id_is_owner = database.message_user_is_owner(u_id, channel_id)

    # Raise AccessError if the user is not part of the channel they are trying to post in
    if u_id_is_owner == False and u_id_is_admin == False:            
        raise AccessError(f"Error, u_id:{u_id} cannot edit a message in a channel they are not the owner or admin of")


    # Otherwise edit the message
    database.message_edit_message(message, message_id)

    return {
    }


'''
Input error if message does not exist
No action required if message input was the same as message in the database
'''
# andreea :
def message_sendlater(token, channel_id, message, time_sent):
    # Stub Code
    # Verify token
    # Use threading library to import the message using message_send
    return {
        #message_id,
    }


def message_react(token, message_id, react_id):
    # Stub Code
    # Find the message_id
    # Change the react_id key in the message dictionary to true
    return {
    }


def message_unreact(token, message_id, react_id):
    # Stub Code
    # Find the message_id
    # Change the react_id key in the message dictionary to false
    return {
    }


def message_pin(token, message_id):
    # Stub Code
    # Find the message_id
    # Change the is_pinned field in the message dictionary to true
    return {
    }


def message_unpin(token, message_id):
    # Stub Code
    # Find the message_id
    # Change the is_pinned field in the message dictionary to false
    return {
    }