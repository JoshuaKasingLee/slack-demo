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
    #clear()
    user1_token = auth.auth_register('user1@example.com', 'password', 'user1', 'name')['token']
    assert(channels_create(user1_token, 'exceptionalll', True) == {
        'channel_id': 0, # is this right?
    })
    clear()

# second channel
def test_second_channel():
    user1_token = auth.auth_register('user1@example.com', 'password', 'user1', 'name')['token']
    channels_create(user1_token, 'exceptionalll', True)
    assert(channels_create(user1_token, 'exceptionalll_2', True) == {
        'channel_id': 1, # is this right?
    })
    clear()

# test private channel is private - could potentially test by getting a person to join a private channel to check it doesn't work
#def test_private():
#    user1_token = auth.auth_register('user1@example.com', 'password', 'user1', 'name')['token']
#    channels_create(user1_token, 'exceptionalll', False)
#    success = 0
#    for channel in private_channels:
#        if channel['name'] == 'exceptionalll':
#            success = 1
#    assert(success == 1)
#    clear()

# test public channel is public
#def test_public():
#    user1_token = auth.auth_register('user1@example.com', 'password', 'user1', 'name')['token']
#    channels_create(user1_token, 'exceptionalll', True)
#    success = 0
#    for channel in public_channels:
#        if channel['name'] == 'exceptionalll':
#            success = 1
#    assert(success == 1)
#    clear()

# channels with duplicate names (should still work?)
def test_repeat_name():
    user1_token = auth.auth_register('user1@example.com', 'password', 'user1', 'name')['token']
    user2_token = auth.auth_register('user2@example.com', 'password', 'user2', 'name')['token']
    channels_create(user1_token, 'duplicate', True)
    assert(channels_create(user2_token, 'duplicate', True) == {
        'channel_id': 1, # is this right?
    })
    clear()

# INVALID TOKEN
def test_invalid_token():
    with pytest.raises(AccessError):
        channels_create('bad token', 'channel1', True)
    clear()

# user does not exist
def test_missing_user():
    with pytest.raises(AccessError):
        channels_create(996, 'channel1', True)
    clear()

# name 20+ characters
def test_invalid_name_long():
    user1_token = auth.auth_register('user1@example.com', 'password', 'user1', 'name')['token']
    with pytest.raises(InputError):
        channels_create(user1_token, 'hahahahahahahahahahaaaa', True)
    clear()

# name 0 characters
def test_invalid_name_empty():
    user1_token = auth.auth_register('user1@example.com', 'password', 'user1', 'name')['token']
    with pytest.raises(InputError):
        channels_create(user1_token, '', True)
    clear()
