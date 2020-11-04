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

def test_active_standup():
    clear()
    user = auth.auth_register("jonathon@gmail.com", "password", "John", "Smith")
    token = user['token']
    channel_id = channels.channels_create(token, "Channel1", True)["channel_id"]
    length = 60
    time_finish = standup.standup_start(token, channel_id, length)
    standup_status = standup.standup_active(token, channel_id)
    assumed_end_time = datetime.now() + timedelta(seconds=length)
    assert (standup_status == {True, assumed_end_time})

def test_no_standup():
    clear()
    user = auth.auth_register("jonathon@gmail.com", "password", "John", "Smith")
    token = user['token']
    channel_id = channels.channels_create(token, "Channel1", True)["channel_id"]
    length = 60
    standup_status = standup.standup_active(token, channel_id)
    assert (standup_status == {False, None})

def test_invalid_channel():
    clear()
    user = auth.auth_register("jonathon@gmail.com", "password", "John", "Smith")
    token = user['token']
    channel_id = 999
    with pytest.raises(InputError):
        standup_status = standup.standup_active(token, channel_id)
    clear()


def test_inactive_standup(): # unsure how to test
    clear()
    user = auth.auth_register("jonathon@gmail.com", "password", "John", "Smith")
    token = user['token']
    channel_id = channels.channels_create(token, "Channel1", True)["channel_id"]
    length = 60
    time_finish = standup.standup_start(token, channel_id, length)
    assumed_end_time = datetime.now() + timedelta(seconds=length)   
    datetime.now() = datetime.now() + timedelta(seconds=90) # not valid but how to pass time
    standup_status = standup.standup_active(token, channel_id)
    datetime.now() = datetime.now() - timedelta(seconds=90) #similar 
    assert (standup_status == {False, assumed_end_time})
    clear()