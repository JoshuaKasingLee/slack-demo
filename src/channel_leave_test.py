import pytest
import database
import other
from channel_leave import channel_leave
from channel_join import channel_join
from channel_details import channel_details
import channels
import auth
from error import InputError
from error import AccessError

def test_leave() :
    (u_id, token) = auth.auth_register("email@gmail.com", "password", "Joshua", "Lee")
    (u_id_2 token_2) = auth.auth_register("email2@gmail.com", "password2", "Kelly", "Zhou") 
    channel_id = channels.channels_create(token, "Channel1", True)
    channel_join(token_2, channel_id)
    channel_leave(token_2, channel_id)
    (name, owner_members, all_members)  = channel_details(token, channel_id)
    is_in = 0
    for member in all_members:
        if member['u_id'] == u_id_2:
            is_in = 1
    assert (is_in == 0)
    other.clear()

def test_valid_channel() :
    (u_id, token) = auth.auth_register("email@gmail.com", "password", "Joshua", "Lee")
    channel_id = channels.channels_create(token, "Channel1", True)
    channel_id_2 = 999
    with pytest.raises(InputError) as e:
        channel_leave(token, channel_id_2)
    other.clear()

def test_not_a_channel_member() :
    (u_id, token) = auth.auth_register("email@gmail.com", "password", "Joshua", "Lee")
    (u_id_2 token_2) = auth.auth_register("email2@gmail.com", "password2", "Kelly", "Zhou") 
    channel_id = channels.channels_create(token, "Channel1", True)
    with pytest.raises(AccessError) as e:
        channel_leave(token_2, channel_id)
    other.clear()