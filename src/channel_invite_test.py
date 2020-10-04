from channel import channel_invite, channel_details
import channels
import pytest
import database
import auth
from other import clear # to change later

# The creator is added to the channel
def test_invite_success():
    user = auth.auth_register("test1@gmail.com", "password", "John", "Smith")
    u_id = user['u_id']
    token = user['token']
    channel_id = channels.channels_create(token, "Channel1", True)
    channel_info = channel_details(token, channel_id)
    all_members = channel_info['all_members']
    is_in = 0
    for member in all_members:
        if member['u_id'] == u_id:
            is_in = 1
    assert (is_in == 1)
    clear()
 
# Test a new member is added successfully
def test_add_member():   
    user_1 = auth.auth_register("email1@gmail.com", "password", "Andreea", "Vissarion")
    u_id_1 = user_1['u_id']
    token_1 = user_1['token']
    user_2 = auth.auth_register("email2@gmail.com", "password", "John", "Smith")
    u_id_2 = user_2['u_id']
    token_2 = user_2['token']
    channel_id = channels.channels_create(token_1, "Channel1", True)
    channel_invite(token_2, channel_id, u_id_2)  
    (x, y, all_members)  = channel_details(token_1, channel_id)
    is_in = 0
    for member in all_members:
        if member['u_id'] == u_id_2:
            is_in = 1
    assert (is_in == 1)
    clear()
    
# Test an invalid channel when none exist
def test_invalid_channel_1():
    user = auth.auth_register("email1@gmail.com", "password", "Andreea", "Vissarion")
    u_id = user['u_id']
    token = user['token']
    channel_id = 3
    with pytest.raises(InputError):
        channel_invite(token, channel_id, u_id)
    clear()
 
# Test an invalid channel when one already exists
def test_invalid_channel_1():
    user = auth.auth_register("email1@gmail.com", "password", "Andreea", "Vissarion")
    u_id = user['u_id']
    token = user['token']
    channel_id = channels.channels_create(token, "Channel1", True)
    channel_id_2 = 4
    with pytest.raises(InputError):
        channel_invite(token, channel_id_2, u_id)
    clear()
 
# Test invalid user
def test_invalid_user():
    user = auth.auth_register("email1@gmail.com", "password", "Andreea", "Vissarion")
    u_id = user['u_id']
    token = user['token']
    fake_id = 10
    channel_id = channels.channels_create(token, "Channel1", True)
    with pytest.raises(InputError):
        channel_invite(token, channel_id, fake_id)
    clear()
 
# Test user already in the channel
def test_user_in_channel():
    user = auth.auth_register("email1@gmail.com", "password", "Andreea", "Vissarion")
    u_id = user['u_id']
    token = user['token']
    channel_id = channels.channels_create(token, "Channel1", True)
    with pytest.raises(AccessError):
        channel_invite(token, channel_id, u_id)
    clear()