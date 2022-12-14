import pytest
from other import clear
from channel import channel_leave, channel_join, channel_details
import channels
import auth
from error import InputError, AccessError

def test_multiple_leave():
    clear()
    user = auth.auth_register("test1@gmail.com", "password", "John", "Smith")
    token = user['token']
    user_2 = auth.auth_register("email2@gmail.com", "password", "John", "Smith")
    token_2 = user_2['token']
    channel_id = channels.channels_create(token, "Channel1", True)['channel_id']
    channel_join(token_2, channel_id)
    channel_leave(token_2, channel_id)
    channel_leave(token, channel_id)
    with pytest.raises(InputError):
        channel_details(token, channel_id)['all_members']
    clear()

def test_leave():
    clear()
    user = auth.auth_register("test1@gmail.com", "password", "John", "Smith")
    token = user['token']
    user_2 = auth.auth_register("email2@gmail.com", "password", "John", "Smith")
    u_id_2 = user_2['u_id']
    token_2 = user_2['token']
    channel_id = channels.channels_create(token, "Channel1", True)['channel_id']
    channel_join(token_2, channel_id)
    channel_leave(token_2, channel_id)
    all_members = channel_details(token, channel_id)['all_members']
    is_in = 0
    for member in all_members:
        if member['u_id'] == u_id_2:
            is_in = 1
    assert (is_in == 0)
    clear()
 
def test_valid_channel():
    clear()
    user = auth.auth_register("test1@gmail.com", "password", "John", "Smith")
    token = user['token']
    channels.channels_create(token, "Channel1", True)['channel_id']
    channel_id_2 = 999
    with pytest.raises(InputError):
        channel_leave(token, channel_id_2)
    clear()
 
def test_not_a_channel_member():
    clear()
    user = auth.auth_register("test1@gmail.com", "password", "John", "Smith")
    token = user['token']
    user_2 = auth.auth_register("email2@gmail.com", "password", "John", "Smith")
    token_2 = user_2['token']
    channel_id = channels.channels_create(token, "Channel1", True)['channel_id']
    with pytest.raises(AccessError):
        channel_leave(token_2, channel_id)
    clear()
