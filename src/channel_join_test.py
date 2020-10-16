import pytest
from other import clear
from channel import channel_join, channel_details
import channels
import auth
from error import InputError, AccessError

def test_join() :
    clear()
    user = auth.auth_register("jonathon@gmail.com", "password", "John", "Smith")
    token = user['token']
    user_2 = auth.auth_register("sallychampion@gmail.com", "password", "Sally", "Champion")
    u_id_2 = user_2['u_id']
    token_2 = user_2['token']   
    channel_id = channels.channels_create(token, "Channel1", True)["channel_id"]
    channel_join(token_2, channel_id)
    all_members  = channel_details(token_2, channel_id)["all_members"]
    is_in = 0
    for member in all_members:
        if member['u_id'] == u_id_2:
            is_in = 1
    assert (is_in == 1)
    clear()
 
def test_valid_channel() :
    clear()
    user = auth.auth_register("jonathon@gmail.com", "password", "John", "Smith")
    token = user['token']
    user_2 = auth.auth_register("sallychampion@gmail.com", "password", "Sally", "Champion")
    token_2 = user_2['token']
    channel_id_2 = 999
    with pytest.raises(InputError):
        channel_join(token_2, channel_id_2)
    clear()
 
def test_private_access() :
    clear()
    user = auth.auth_register("test1@gmail.com", "password", "John", "Smith")
    token = user['token']
    user_2 = auth.auth_register("email2@gmail.com", "password", "John", "Smith")
    token_2 = user_2['token']   
    channel_id = channels.channels_create(token, "Channel1", False)["channel_id"]
    with pytest.raises(AccessError):
        channel_join(token_2, channel_id)
    clear()
 
def test_invalid_token(): # non integer token - accesserror
    clear()
    user = auth.auth_register("cyruschow@gmail.com", "password", "Cyrus", "Chow")
    token = user['token']
    channel_id = channels.channels_create(token, "channel1", True)["channel_id"]
    with pytest.raises(AccessError):
        channel_join('heyheyhey', channel_id)
    clear()
 
def test_missing_user(): # wrong user token - accesserror
    clear()
    user = auth.auth_register("kellyzhou@gmail.com", "password", "Kelly", "Zhou")
    token = user['token']
    channel_id = channels.channels_create(token, "channel1", True)["channel_id"]
    with pytest.raises(AccessError):
        channel_join(39, channel_id)
    clear()