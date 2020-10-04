from channel import channel_details, channel_invite, channel_addowner
import pytest
import database
import auth
import channels
from other import clear
 
def test_no_owner():   
    user = auth.auth_register("test1@gmail.com", "password", "John", "Smith")
    u_id = user['u_id']
    token = user['token']
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
    clear()
        
def test_one_owner():   
    user = auth.auth_register("test1@gmail.com", "password", "John", "Smith")
    u_id = user['u_id']
    token = user['token']
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
    clear()
 
def test_one_owner_two_members(): # two members, one of them is an ownr
    user_1 = auth.auth_register("email1@gmail.com", "password", "Andreea", "Vissarion")
    u_id_1 = user_1['u_id']
    token_1 = user_1['token']
    user_2 = auth.auth_register("email2@gmail.com", "password", "John", "Smith")
    u_id_2 = user_2['u_id']
    token_2 = user_2['token']
    channel_id = channels.channels_create(token, "Channel1", True)
    channel_invite(token_1, channel_id, u_id_1)
    channel_addowner(token_1, channel_id, u_id_1)
    channel_invite(token_1, channel_id, u_id_2)
    assert channel_details(token_1, channel_id) == {
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
    clear()
 
def test_invalid_token(): # invalid token - AccessError
    user = auth.auth_register("test1@gmail.com", "password", "John", "Smith")
    u_id = user['u_id']
    token = user['token']
    channel_id = channels.channels_create(token, "channel1", True)
    with pytest.raises(AccessError):
        channel_details('imalil', channel_id)
    clear()
 
def test_not_member(): # user not in channel - AccessError
    user_1 = auth.auth_register("email1@gmail.com", "password", "Andreea", "Vissarion")
    u_id_1 = user_1['u_id']
    token_1 = user_1['token']
    user_2 = auth.auth_register("email2@gmail.com", "password", "John", "Smith")
    u_id_2 = user_2['u_id']
    token_2 = user_2['token']
    channel_id = channels.channels_create(token_1, "channel1", True)
    with pytest.raises(AccessError):
        channel_details(token_2, channel_id)
    clear()
 
def test_missing_channel(): # invalid channel_id - InputError
    user = auth.auth_register("test1@gmail.com", "password", "John", "Smith")
    u_id = user['u_id']
    token = user['token']
    with pytest.raises(InputError):
        channel_details(token, channel_id)
    clear()