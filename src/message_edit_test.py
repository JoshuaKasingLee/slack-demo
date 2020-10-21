import pytest
from message import message_send, message_remove, message_edit
import auth
import channels
from error import AccessError
from error import InputError
from other import clear

# Test that an Access Error is raised when user is not a channel owner
def test_user_not_owner():
    user_token = auth.auth_register("user@gmail.com", "password", "John", "Smith")['token']
    channel_id = channels.channels_create(user_token, "Test Channel", True)['channel_id']
    message_to_send = 'Hi!'
    message_id = message_send(user_token, channel_id, message_to_send)['message_id']
    user_token = auth.auth_register("user2@gmail.com", "password", "Sam", "Smith")['token']
    message_to_send = 'New Message!'
    with pytest.raises(AccessError):
        message_edit(user_token, message_id, message_to_send)
    clear()

# Test that an Input Error is raised when the message does not exist
def test_message_never_existed():
    user_token = auth.auth_register("user@gmail.com", "password", "John", "Smith")['token']
    channels.channels_create(user_token, "Test Channel", True)['channel_id']
    message_id = 15
    message_to_send = 'Edited Message!'
    with pytest.raises(InputError):
        message_edit(user_token, message_id, message_to_send)
    clear()

# Test that an Input Error is raised when the message was deleted
def test_message_already_deleted():
    user_token = auth.auth_register("user@gmail.com", "password", "John", "Smith")['token']
    channel_id = channels.channels_create(user_token, "Test Channel", True)['channel_id']
    message_to_send = 'Hi!'
    message_id = message_send(user_token, channel_id, message_to_send)['message_id']
    message_remove(user_token, message_id)
    message_to_send = 'Edited Message!'
    with pytest.raises(InputError):
        message_edit(user_token, message_id, message_to_send)
    clear()

# Test message was edited correctly
def test_message_success():
    user_token = auth.auth_register("user@gmail.com", "password", "John", "Smith")['token']
    channel_id = channels.channels_create(user_token, "Test Channel", True)['channel_id']
    message_to_send = 'Hi!'
    message_id = message_send(user_token, channel_id, message_to_send)['message_id']
    message_to_send = 'New Message!'
    clear()
