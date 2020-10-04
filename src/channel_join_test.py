import pytest
from other import clear
from channel import channel_join, channel_details
import channels
import auth
from error import InputError, AccessError

def test_join() :
    user = auth.auth_register("test1@gmail.com", "password", "John", "Smith")
    u_id = user['u_id']
    token = user['token']
    user_2 = auth.auth_register("email2@gmail.com", "password", "John", "Smith")
    u_id_2 = user_2['u_id']
    token_2 = user_2['token']   
    channel_id = channels.channels_create(token, "Channel1", True)
    channel_join(token_2, channel_id)
    (name, owner_members, all_members)  = channel_details(token_2, channel_id)
    is_in = 0
    for member in all_members:
        if member['u_id'] == u_id_2:
            is_in = 1
    assert (is_in == 1)
    clear()
 
def test_valid_channel() :
    user = auth.auth_register("test1@gmail.com", "password", "John", "Smith")
    u_id = user['u_id']
    token = user['token']
    user_2 = auth.auth_register("email2@gmail.com", "password", "John", "Smith")
    u_id_2 = user_2['u_id']
    token_2 = user_2['token'] 
    channel_id = channels.channels_create(token, "Channel1", True)
    channel_id_2 = 999
    with pytest.raises(InputError) as e:
        channel_join(token_2, channel_id_2)
    clear()
 
def test_private_access() :
    user = auth.auth_register("test1@gmail.com", "password", "John", "Smith")
    u_id = user['u_id']
    token = user['token']
    user_2 = auth.auth_register("email2@gmail.com", "password", "John", "Smith")
    u_id_2 = user_2['u_id']
    token_2 = user_2['token']   
    channel_id = channels.channels_create(token, "Channel1", False)
    with pytest.raises(AccessError) as e:
        channel_join(token_2, channel_id)
    clear()
 
def test_invalid_token(): # non integer token - accesserror
    user = auth.auth_register("test1@gmail.com", "password", "John", "Smith")
    u_id = user['u_id']
    token = user['token']
    channel_id = channels.channels_create(token, "channel1", True)
    with pytest.raises(AccessError):
        channel_join('heyheyhey', channel_id)
    clear()
 
def test_missing_user(): # wrong user token - accesserror
    user = auth.auth_register("test1@gmail.com", "password", "John", "Smith")
    u_id = user['u_id']
    token = user['token']
    channel_id = channels.channels_create(token, "channel1", True)
    with pytest.raises(AccessError):
        channel_join(39, channel_id)
    clear()