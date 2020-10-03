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
