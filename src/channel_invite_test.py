from channel_invite import channel_invite
from channel_details import channel_details
import channels
import pytest
import database
import auth
from database import clear # to change later

# The creator is added to the channel
def test_invite_success():
    (u_id, token) = auth.auth_register("test1@gmail.com", "password", "John", "Smith")
    # (u_id2, token2) = auth.auth_register("test2@gmail.com", "password", "Kathy", "Jones")
    channel_id = channels.channels_create(token, "Channel1", True)
    (x, y, all_members)  = channel_details(token, channel_id)
    is_in = 0
    for member in all_members:
        if member['u_id'] == u_id:
            is_in = 1
    assert (is_in == 1)
    clear()

# Test a new member is added successfully
def test_add_member():   
    (u_id_1, token_1) = auth.auth_register("email@gmail.com", "password", "Andreea", "Vissarion")
    (u_id_2, token_2) = auth.auth_register("email2@gmail.com", "password", "John", "Smith")
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
    (u_id, token) = auth.auth_register("email@gmail.com", "password", "Andreea", "Vissarion")
    channel_id = 3
    with pytest.raises(InputError):
        channel_invite(token, channel_id, u_id)
    clear()

# Test an invalid channel when one already exists
def test_invalid_channel_1():
    (u_id, token) = auth.auth_register("email@gmail.com", "password", "Andreea", "Vissarion")
    channel_id = channels.channels_create(token, "Channel1", True)
    channel_id_2 = 4
    with pytest.raises(InputError):
        channel_invite(token, channel_id_2, u_id)
    clear()

# Test invalid user
def test_invalid_user():
    (u_id, token) = auth.auth_register("email@gmail.com", "password", "Andreea", "Vissarion")
    fake_id = 10
    channel_id = channels.channels_create(token, "Channel1", True)
    with pytest.raises(InputError):
        channel_invite(token, channel_id, fake_id)
    clear()


# Test user already in the channel
def test_user_in_channel():
    (u_id, token) = auth.auth_register("email@gmail.com", "password", "Andreea", "Vissarion")
    channel_id = channels.channels_create(token, "Channel1", True)
    with pytest.raises(AccessError):
        channel_invite(token, channel_id, u_id)
    clear()

