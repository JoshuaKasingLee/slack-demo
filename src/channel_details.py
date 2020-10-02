from channel_details import channel_details
from channel_invite import channel_invite
from channel_addowner import channel_addowner
import pytest
import database
import auth
import channels


def channel_details(token, channel_id):
    
    
    
    
    
    
    
    return {
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