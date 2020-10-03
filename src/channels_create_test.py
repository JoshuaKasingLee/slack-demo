import pytest
from channels_create import channels_create
import channels
import channel
import auth
from error import AccessError

import database_edited_for_channels as db

## channels_create

# first channel
def test_first_channel():
    user1_token = auth.auth_register('user1@example.com', 'password', 'user1', 'name')['token']
    assert(channels_create(user1_token, 'exceptionalll', True) == 1)
db.clear()

# second channel
def test_second_channel():
    user1_token = auth.auth_register('user1@example.com', 'password', 'user1', 'name')['token']
    channels_create(user1_token, 'exceptionalll', True)
    assert(channels_create(user1_token, 'exceptionalll_2', True) == 2)
db.clear()

# test private channel is private
def test_private():
    user1_token = auth.auth_register('user1@example.com', 'password', 'user1', 'name')['token']
    channels_create(user1_token, 'exceptionalll', False)
    success = 0
    for channel in private_channels:
        if channel['name'] == 'exceptionalll':
            success = 1
    assert(success == 1)
db.clear()

# test public channel is public
def test_public():
    user1_token = auth.auth_register('user1@example.com', 'password', 'user1', 'name')['token']
    channels_create(user1_token, 'exceptionalll', True)
    success = 0
    for channel in public_channels:
        if channel['name'] == 'exceptionalll':
            success = 1
    assert(success == 1)
db.clear()

# channels with duplicate names (should still work?)
def test_repeat_name():
    user1_token = auth.auth_register('user1@example.com', 'password', 'user1', 'name')['token']
    user2_token = auth.auth_register('user2@example.com', 'password', 'user2', 'name')['token']
    channels_create(user1_token, 'duplicate', True)
    assert(channels_create(user2_token, 'duplicate', True) == 2)
db.clear()

# INVALID TOKEN
def test_invalid_token():
    with pytest.raises(AccessError) as e: # what does this e mean
        channels.channels_create('bad token', 'channel1', True)
db.clear()

# user does not exist
def test_missing_user():
    with pytest.raises(AccessError) as e:
        channels.channels_create(996, 'channel1', True)
db.clear()

# name 20+ characters
def test_invalid_name_long():
    user1_token = auth.auth_register('user1@example.com', 'password', 'user1', 'name')['token']
    with pytest.raises(InputError) as e:
        channels_create(user1_token, 'hahahahahahahahahahaaaa', True)
db.clear()

# name 0 characters
def test_invalid_name_empty():
    user1_token = auth.auth_register('user1@example.com', 'password', 'user1', 'name')['token']
    with pytest.raises(InputError) as e:
        channels_create(user1_token, '', True)
db.clear()
