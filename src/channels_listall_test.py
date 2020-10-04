import pytest
from channels import channels_listall
import channels
import auth
from error import AccessError
from other import clear


def test_one():
    token = auth.auth_register("email@gmail.com", "password", "Andreea", "Viss")['token']
    channel_id = channels.channels_create(token, "Channel1", True)['channel_id']
    assert channels_listall(token) == {
        'channels': [
        	{
        		'channel_id': channel_id,
        		'name': 'Channel1',
        	}
        ],
    }
    clear()


def test_two_owner():
    token = auth.auth_register("email@gmail.com", "password", "Andreea", "Viss")['token']
    channel_id = channels.channels_create(token, "Channel1", True)['channel_id']
    channel_id2 = channels.channels_create(token, "Channel2", False)['channel_id']
    assert channels_listall(token) == {
        'channels': [
        	{
        		'channel_id': channel_id,
        		'name': 'Channel1',
        	},
        {
        		'channel_id': channel_id2,
        		'name': 'Channel2',
        	}
        ],
    }
    clear()
        

def test_two_not_owner():
    token = auth.auth_register("email@gmail.com", "password", "Andreea", "Viss")['token']
    channel_id = channels.channels_create(token, "Channel1", True)['channel_id']
    token2 = auth.auth_register("email2@gmail.com", "password", "Andreea2", "Viss2")['token']
    channel_id2 = channels.channels_create(token2, "Channel2", False)['channel_id']
    assert channels_listall(token) == {
        'channels': [
        	{
        		'channel_id': channel_id,
        		'name': 'Channel1',
        	},
        {
        		'channel_id': channel_id2,
        		'name': 'Channel2',
        	}
        ],
    }
    clear()

  
def test_empty():
    token = auth.auth_register("email@gmail.com", "password", "Andreea", "Viss")['token']
    assert channels_listall(token) == {
        'channels': [],
    }
    clear()
    

def test_invalid_token_name():
    token  = "blahblah"
    with pytest.raises(AccessError): 
        channels_listall(token)
    clear()
        

def test_invalid_user():
    token = auth.auth_register("email@gmail.com", "password", "Andreea", "Viss")['token']
    token  = token + "1"
    with pytest.raises(AccessError): 
        channels_listall(token)
    clear()
        

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