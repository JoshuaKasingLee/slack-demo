import pytest
from channels_list import channels_list
import channels
import channel
import auth
from error import AccessError

import database_edited_for_channels as db # only for clearing

def test_one():
    (u_id, token) = auth.auth_register("email@gmail.com", "password", "Andreea", "Viss")
    channel_id = channels.channels_create(token, "Channel1", True)
    assert channels_list(token) == {
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
    assert channels_list(token) == {
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
    assert channels_list(token) == {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'Channel1',
        	}
        ],
    }

db.clear()

def test_two_member():
    (u_id, token) = auth.auth_register("email@gmail.com", "password", "Andreea", "Viss")
    channel_id = channels.channels_create(token, "Channel1", True)
    (u_id, token2) = auth.auth_register("email@gmail.com", "password", "Andreea", "Viss")
    channel_id = channels.channels_create(token2, "Channel2", True)
    channel.channel_join(token, channel_id)
    assert channels_list(token) == {
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
    assert channels_list(token) == {
        'channels': [],
    }

db.clear()

def test_error_invalid_token():
    token  = "blahblah"
    with pytest.raises(AccessError): 
        channels_list(token) 
        
db.clear()

def test_invalid_user():
    (u_id, token) = auth.auth_register("email@gmail.com", "password", "Andreea", "Viss")
    token  = token + "1"
    with pytest.raises(AccessError): 
        channels_list(token)

db.clear()