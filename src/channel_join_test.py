import pytest
import database
from channel_join import channel_join
import channels
import auth
from error import InputError
from error import AccessError

def test_join() :
    (u_id, token) = auth.auth_register("email@gmail.com", "password", "Joshua", "Lee")
    channel_id = channels.channels_create(token, "Channel1", True)
    channel_join(token, channel_id)
    assert database.channels_and_members[channel_id][1][0]['u_id'] == token
    database.clear()

def test_valid_channel() :
    (u_id, token) = auth.auth_register("email@gmail.com", "password", "Joshua", "Lee")
    channel_id = 999
    with pytest.raises(InputError) as e:
        assert channel_join(token, channel_id)
    database.clear()

def test_private_access() :
    (u_id, token) = auth.auth_register("email@gmail.com", "password", "Joshua", "Lee")
    channel_id = channels.channels_create(token, "Channel1", False)
    channel_join(token, channel_id)
    with pytest.raises(AccessError) as e:
        assert channel_join(token, channel_id)
    database.clear()