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
        'name': 'Hayden',
        'owner_members': [],
        'all_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
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
        'name': 'Hayden',
        'owner_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
        'all_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
    }
    
    
