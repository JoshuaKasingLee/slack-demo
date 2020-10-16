import pytest
from channels import channels_create
import channel
import auth
from error import AccessError
from error import InputError
from other import clear

## channels_create

# first channel
def test_first_channel():
    clear()
    user1_token = auth.auth_register('user1@example.com', 'password', 'user1', 'name')['token']
    assert(channels_create(user1_token, 'exceptionalll', True) == {
        'channel_id': 0, 
    })
    clear()

# second channel
def test_second_channel():
    clear()
    user1_token = auth.auth_register('user1@example.com', 'password', 'user1', 'name')['token']
    channels_create(user1_token, 'exceptionalll', True)
    assert(channels_create(user1_token, 'exceptionalll_2', True) == {
        'channel_id': 1,
    })
    clear()

def test_repeat_name():
    clear()
    user1_token = auth.auth_register('user1@example.com', 'password', 'user1', 'name')['token']
    user2_token = auth.auth_register('user2@example.com', 'password', 'user2', 'name')['token']
    channels_create(user1_token, 'duplicate', True)
    assert(channels_create(user2_token, 'duplicate', True) == {
        'channel_id': 1, 
    })
    clear()

# INVALID TOKEN
def test_invalid_token():
    clear()
    with pytest.raises(AccessError):
        channels_create('bad token', 'channel1', True)
    clear()

# user does not exist
def test_missing_user():
    clear()
    with pytest.raises(AccessError):
        channels_create(996, 'channel1', True)
    clear()

# name 20+ characters
def test_invalid_name_long():
    clear()
    user1_token = auth.auth_register('user1@example.com', 'password', 'user1', 'name')['token']
    with pytest.raises(InputError):
        channels_create(user1_token, 'hahahahahahahahahahaaaa', True)
    clear()

# name 0 characters
def test_invalid_name_empty():
    clear()
    user1_token = auth.auth_register('user1@example.com', 'password', 'user1', 'name')['token']
    with pytest.raises(InputError):
        channels_create(user1_token, '', True)
    clear()
