import pytest
from channels import channels_list
import channels
import channel
import auth
from error import AccessError
from other import clear
import database as db

def test_one():
    token = auth.auth_register("email@gmail.com", "password", "Andreea", "Viss")['token']
    channel_id = channels.channels_create(token, "Channel1", True)['channel_id']
    assert channels_list(token) == {
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
    assert channels_list(token) == {
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
    assert channels_list(token) == {
        'channels': [
        	{
        		'channel_id': channel_id,
        		'name': 'Channel1',
        	}
        ],
    }
    clear()

def test_two_member():
    token = auth.auth_register("email@gmail.com", "password", "Andreea", "Viss")['token']
    channel_id = channels.channels_create(token, "Channel1", True)['channel_id']
    token2 = auth.auth_register("email2@gmail.com", "password", "Andreea2", "Viss2")['token']
    channel_id2 = channels.channels_create(token2, "Channel2", True)['channel_id']
    channel.channel_join(token, channel_id2)
    assert channels_list(token) == {
        'channels': [
        	{
        		'channel_id': channel_id,
        		'name': 'Channel1',
        	},
        {
        		'channel_id': channel_id2,
        		'name': 'Channel2',
        	}
        ]
    }
    clear()


def test_empty():
    token = auth.auth_register("email@gmail.com", "password", "Andreea", "Viss")['token']
    assert channels_list(token) == {
        'channels': [],
    }
    clear()

def test_error_invalid_token():
    token  = "blahblah"
    with pytest.raises(AccessError): 
        channels_list(token) 
    clear()
    
    
def test_invalid_user():
    token = auth.auth_register("email@gmail.com", "password", "Andreea", "Viss")['token']
    token  = token + "1"
    with pytest.raises(AccessError): 
        channels_list(token)
    clear()