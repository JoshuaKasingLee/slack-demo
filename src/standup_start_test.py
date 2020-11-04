import pytest
from error import AccessError
from error import InputError
import channels
import channel
import auth
from other import clear
import standup
from datetime import datetime
from datetime import timedelta

def test_standup_start():
    clear()
    user = auth.auth_register("jonathon@gmail.com", "password", "John", "Smith")
    token = user['token']
    channel_id = channels.channels_create(token, "Channel1", True)["channel_id"]
    length = 60
    time_finish = standup.standup_start(token, channel_id, length)
    standup_status = standup.standup_active(token, channel_id)
    assumed_end_time = datetime.now() + timedelta(seconds=length)
    assert (standup_status == {True, assumed_end_time})

def test_invalid_channel():
    clear()
    user = auth.auth_register("jonathon@gmail.com", "password", "John", "Smith")
    token = user['token']
    channel_id = 999
    length = 60
    with pytest.raises(InputError):
        time_finish = standup.standup_start(token, channel_id, length)
    clear()

def test_standup_already_exists():
    clear()
    user = auth.auth_register("jonathon@gmail.com", "password", "John", "Smith")
    token = user['token']
    channel_id = channels.channels_create(token, "Channel1", True)["channel_id"]
    length = 60
    time_finish = standup.standup_start(token, channel_id, length)
    with pytest.raises(InputError):
        time_finish = standup.standup_start(token, channel_id, length)
    clear()