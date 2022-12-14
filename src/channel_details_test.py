from channel import channel_details, channel_invite
import pytest
import auth
import channels
from other import clear
from error import AccessError, InputError
import database as db

def test_owner(): 
    clear()
    user = auth.auth_register("test1@gmail.com", "password", "John", "Smith")
    u_id = user['u_id']
    token = user['token']
    channel_id = channels.channels_create(token, "Channel1", True)['channel_id']
    assert channel_details(token, channel_id) == {
        'name': 'Channel1',
        'owner_members': [
         {
            'u_id': u_id, 
            'name_first': 'John',
            'name_last': 'Smith',
            'profile_img_url': None
        }],
        'all_members': [
            {
                'u_id': u_id, 
                'name_first': 'John',
                'name_last': 'Smith',
                'profile_img_url': None
            }
        ],
    }
    clear()
def test_one_owner_two_members(): # two members, one of them is an ownr
    clear()
    user_1 = auth.auth_register("email1@gmail.com", "password", "Andreea", "Vissarion")
    token_1 = user_1['token']
    u_id_1 = user_1['u_id']
    user_2 = auth.auth_register("email2@gmail.com", "password", "John", "Smith")
    u_id_2 = user_2['u_id']
    channel_id = channels.channels_create(token_1, "Channel1", True)['channel_id']
    channel_invite(token_1, channel_id, u_id_2)
    assert channel_details(token_1, channel_id) == {
        'name': 'Channel1',
        'owner_members': [
            {
                'u_id': u_id_1,
                'name_first': 'Andreea',
                'name_last': 'Vissarion',
                'profile_img_url': None
            }
        ],
        'all_members': [
            {
                'u_id': u_id_1,
                'name_first': 'Andreea',
                'name_last': 'Vissarion',
                'profile_img_url': None
            },
            {
                'u_id': u_id_2,
                'name_first': 'John',
                'name_last': 'Smith',
                'profile_img_url': None
            }
        ],
    }
    clear()
def test_invalid_token(): # invalid token - AccessError
    clear()
    user = auth.auth_register("test1@gmail.com", "password", "John", "Smith")
    token = user['token']
    channel_id = channels.channels_create(token, "channel1", True)['channel_id']
    with pytest.raises(AccessError):
        channel_details('imalil', channel_id)
    clear()
def test_not_member(): # user not in channel - AccessError
    clear()
    user_1 = auth.auth_register("email1@gmail.com", "password", "Andreea", "Vissarion")
    token_1 = user_1['token']
    user_2 = auth.auth_register("email2@gmail.com", "password", "John", "Smith")
    token_2 = user_2['token']
    channel_id = channels.channels_create(token_1, "channel1", True)['channel_id']
    with pytest.raises(AccessError):
        channel_details(token_2, channel_id)
    clear()
def test_missing_channel(): # invalid channel_id - InputError
    clear()
    user = auth.auth_register("test1@gmail.com", "password", "John", "Smith")
    token = user['token']
    channel_id = 1
    with pytest.raises(InputError):
        channel_details(token, channel_id)
    clear()
