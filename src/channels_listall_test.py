import pytest
from channels_listall import channels_listall
import channels
#import channel
import auth
from error import AccessError

import database_edited_for_channels as db # only for clearing

def test_one():
    (u_id, token) = auth.auth_register("email@gmail.com", "password", "Andreea", "Viss")
    channel_id = channels.channels_create(token, "Channel1", True)
    assert channels_listall(token) == {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'Channel1',
        	}
        ],
    }

db.clear()

def test_two_owner():
    (u_id, token) = auth.auth_register("email@gmail.com", "password", "Andreea", "Viss")
    channel_id = channels.channels_create(token, "Channel1", True)
    channel_id = channels.channels_create(token, "Channel2", False)
    assert channels_listall(token) == {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'Channel1',
        	},
        {
        		'channel_id': 2,
        		'name': 'Channel2',
        	}
        ],
    }
        
db.clear()

def test_two_not_owner():
    (u_id, token) = auth.auth_register("email@gmail.com", "password", "Andreea", "Viss")
    channel_id = channels.channels_create(token, "Channel1", True)
    (u_id, token2) = auth.auth_register("email@gmail.com", "password", "Andreea", "Viss")
    channel_id = channels.channels_create(token2, "Channel2", False)
    assert channels_listall(token) == {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'Channel1',
        	},
        {
        		'channel_id': 2,
        		'name': 'Channel2',
        	}
        ],
    }
    

db.clear()
  
def test_empty():
    (u_id, token) = auth.auth_register("email@gmail.com", "password", "Andreea", "Viss")
    assert channels_listall(token) == {
        'channels': [],
    }
    
db.clear()

def test_invalid_token_name():
    token  = "blahblah"
    with pytest.raises(AccessError): 
        channels_listall(token)
        
db.clear()

def test_invalid_user():
    (u_id, token) = auth.auth_register("email@gmail.com", "password", "Andreea", "Viss")
    token  = token + "1"
    with pytest.raises(AccessError): 
        channels_listall(token)
        
db.clear()    

'''
## tests which don't work

# there are no channels
def test_no_channels():
    user1_token = auth.auth_register('user1@example.com', 'password', 'user1', 'name')['token']
    assert(channels.channels_listall(user1_token) == {'channels': [],}

db.clear()

# there is one public channel
def test_no_memberships():
    user1_token = auth.auth_register('user1@example.com', 'password', 'user1', 'name')['token']
    channel1 = channels.channels_create(user1_token, 'channel1', True)
    assert(channels.channels_listall(user1_token) == {'channels': [ {'channel_id': 1, 'name': 'channel1' }],}
db.clear()

# there is one private channel
def test_no_memberships():
    user1_token = auth.auth_register('user1@example.com', 'password', 'user1', 'name')['token']
    channel1 = channels.channels_create(user1_token, 'channel1', False)
    assert(channels.channels_listall(user1_token) == {'channels': [ {'channel_id': 1, 'name': 'channel1' }],}
db.clear()
    
# there are two channels
def test_all_memberships():
    user1_token = auth.auth_register('user@example.com', 'password', 'user1', 'name')['token']
    channel1 = channels.channels_create(user1_token, 'channel1', True)
    channel2 = channels.channels_create(user1_token, 'channel2', False)
    assert(channels.channels_listall(user1_token) == {'channels': [ {'channel_id': 1, 'name': 'channel1' }, { 'channel_id': 2, 'name': 'channel2' }],}
db.clear()

# INVALID TOKEN
def test_invalid_token():
    user1_token = auth.auth_register('user1@example.com', 'password', 'user1', 'name')['token']
    channel1 = channels.channels_create(user1_token, 'channel1', True)
    with pytest.raises(AccessError) as e: # what does this e mean
        channels_listall('bad token')
db.clear()

# user does not exist
def test_missing_user():
    user1_token = auth.auth_register('user1@example.com', 'password', 'user1', 'name')['token']
    channel1 = channels.channels_create(user1_token, 'channel1', True)
    with pytest.raises(AccessError) as e:
        channels_listall(996)
db.clear()
'''