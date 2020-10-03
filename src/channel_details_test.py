from channel_details import channel_details
from channel_invite import channel_invite
from channel_addowner import channel_addowner
import pytest
import database
import auth
import channels

def test_no_owner():   
    (u_id, token) = auth.auth_register("email@gmail.com", "password", "Andreea", "Vissarion")
    channel_id = channels.channels_create(token, "Channel1", True)
    channel_invite(token, channel_id, u_id)   
    assert channel_details(token, channel_id) == {
        'name': 'Channel1',
        'owner_members': [],
        'all_members': [
            {
                'u_id': 1, # should this be a 0?
                'name_first': 'Andreea',
                'name_last': 'Vissarion',
            }
        ],
    }

database.clear()
        
def test_one_owner():   
    (u_id, token) = auth.auth_register("email@gmail.com", "password", "Hayden", "Jacobs")
    channel_id = channels.channels_create(token, "Channel1", True)
    channel_invite(token, channel_id, u_id) 
    channel_addowner(token, channel_id, u_id)   
    assert channel_details(token, channel_id) == {
        'name': 'Channel1',
        'owner_members': [
            {
                'u_id': 1, # should this be a 0?
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
        'all_members': [
            {
                'u_id': 1, # should this be a 0?
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
    }

def test_one_owner_two_members(): # two members, one of them is an ownr
    (u_id1, token1) = auth.auth_register("email1@gmail.com", "password", "Hayden", "Jacobs")
    (u_id2, token2) = auth.auth_register("email2@gmail.com", "password", "Andreea", "Vissarion")
    channel_id = channels.channels_create(token, "Channel1", True)
    channel_invite(token1, channel_id, u_id1)
    channel_addowner(token1, channel_id, u_id1)
    channel_invite(token1, channel_id, u_id2)
    assert channel_details(token1, channel_id) == {
        'name': 'Channel1',
        'owner_members': [
            {
                'u_id': 1, # should this be a 0?
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
        'all_members': [
            {
                'u_id': 1, # should this be a 0?
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            },
            {
                'u_id': 2, # should this be a 1?
                'name_first': 'Andreea',
                'name_last': 'Vissarion',
            }
        ],
    }

def test_invalid_token(): # invalid token - AccessError
    (u_id, token) = auth.auth_register("user1@gmail.com", "password", "user1", "lastname1")
    channel_id = channels.channels_create(token, "channel1", True)
    with pytest.raises(AccessError):
        channel_details('imalil', channel_id)

def test_not_member(): # user not in channel - AccessError
    (u_id1, token1) = auth.auth_register("user1@gmail.com", "password", "user1", "lastname1")
    (u_id2, token2) = auth.auth_register("user2@gmail.com", "password", "user2", "lastname2")
    channel_id = channels.channels_create(token1, "channel1", True)
    with pytest.raises(AccessError):
        channel_details(token2, channel_id)

def test_missing_channel(): # invalid channel_id - InputError
    (u_id, token) = auth.auth_register("user1@gmail.com", "password", "user1", "lastname1")
    with pytest.raises(InputError):
        channel_details(token, channel_id)
