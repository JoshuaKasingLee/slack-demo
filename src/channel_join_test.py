import pytest
import database
from channel_invite import channel_invite
import channels
import auth
import error

def test_join() :
    (u_id, token) = auth.auth_register("email@gmail.com", "password", "Joshua", "Lee")
    channel_id = channels.channels_create(token, "Channel1", True)
    channel_join(token, channel_id)
    assert channels_and_members[f"{channel_id}"][1][0]['u_id'] == token
    database.clear()
def test_valid_channel() :
    (u_id, token) = auth.auth_register("email@gmail.com", "password", "Joshua", "Lee")
    channel_id = 999
    with pytest.raises(InputError) as e:
        assert channel_join(token, channel_id)