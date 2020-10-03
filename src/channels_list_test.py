import pytest
from channels_list import channels_list
import channels
import channel
import auth
from error import AccessError

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
    
    
def test_empty():
    (u_id, token) = auth.auth_register("email@gmail.com", "password", "Andreea", "Viss")
    assert channels_list(token) == {
        'channels': [],
    }

def test_error():
    token  = "blahblah"
    with pytest.raiser(AccessError): 
        channels_list(token) 
