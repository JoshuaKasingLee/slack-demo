import pytest
from message import message_send, message_remove
import auth
import channels
import message
import channel
from error import AccessError
from error import InputError
from other import clear

# Test inputs


# Test message no longer exists
def test_message_already_deleted():
    clear()
    user_token = auth.auth_register("user@gmail.com", "password", "John", "Smith")['token']
    channel_id = channels.channels_create(user_token, "Test Channel", True)['channel_id']
    message_to_send = 'Hi!'
    message_id = message_send(user_token, channel_id, message_to_send)['message_id']
    message_remove(user_token, message_id)
    with pytest.raises(InputError):
        message_remove(user_token, message_id)
    clear()

# Test message never existed
def test_message_never_existed():
    clear()
    user_token = auth.auth_register("user@gmail.com", "password", "John", "Smith")['token']
    channels.channels_create(user_token, "Test Channel", True)['channel_id']
    message_id = 15
    with pytest.raises(InputError):
        message_remove(user_token, message_id)
    clear()

# Test user is not an owner of the channel
def test_user_not_owner():
    clear()
    user_token = auth.auth_register("user@gmail.com", "password", "John", "Smith")['token']
    channel_id = channels.channels_create(user_token, "Test Channel", True)['channel_id']
    message_to_send = 'Hi!'
    message_id = message_send(user_token, channel_id, message_to_send)['message_id']
    user_token = auth.auth_register("user2@gmail.com", "password", "Sam", "Smith")['token']
    with pytest.raises(AccessError):
        message_remove(user_token, message_id)
    clear()

# Testing removal function
def test_working_removal():
    clear()
    user_token = auth.auth_register("user@gmail.com", "password", "John", "Smith")['token']
    channel_id = channels.channels_create(user_token, "Test Channel", True)['channel_id']
    message_to_send = 'Hi!'
    message_id = message_send(user_token, channel_id, message_to_send)['message_id']
    message_remove(user_token, message_id)
    data = channel.channel_messages(user_token, channel_id, 0)
    assert (data['messages'] == [])
    clear()
