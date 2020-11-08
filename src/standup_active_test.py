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
import time


def test_standup_active_single():
    clear()
    user = auth.auth_register("jonathon@gmail.com", "password", "John", "Smith")
    token = user['token']
    channel_id = channels.channels_create(token, "Channel1", True)["channel_id"]
    length = 60
    time_finish = standup.standup_start(token, channel_id, length)
    standup_status = standup.standup_active(token, channel_id)
    assert (standup_status == {'is_active': True, 'time_finish': time_finish['time_finish']})

def test_standup_active_single_time_passed():
    clear()
    user = auth.auth_register("jonathon@gmail.com", "password", "John", "Smith")
    token = user['token']
    channel_id = channels.channels_create(token, "Channel1", True)["channel_id"]
    length = 60
    time_finish = standup.standup_start(token, channel_id, length)
    time.sleep(2)
    standup_status = standup.standup_active(token, channel_id)
    assert (standup_status == {'is_active': True, 'time_finish': time_finish['time_finish']})

def test_standup_active_mulitple():
    clear()
    user = auth.auth_register("jonathon@gmail.com", "password", "John", "Smith")
    token = user['token']
    channel_id = channels.channels_create(token, "Channel1", True)["channel_id"]
    channel_id_2 = channels.channels_create(token, "Channel2", True)["channel_id"]
    length = 60
    time_finish = standup.standup_start(token, channel_id, length)
    time_finish_2 = standup.standup_start(token, channel_id_2, length)
    standup_status = standup.standup_active(token, channel_id)
    standup_status_2 = standup.standup_active(token, channel_id_2)
    assert (standup_status == {'is_active': True, 'time_finish': time_finish['time_finish']})
    assert (standup_status_2 == {'is_active': True, 'time_finish': time_finish_2['time_finish']})

def test_no_standup():
    clear()
    user = auth.auth_register("jonathon@gmail.com", "password", "John", "Smith")
    token = user['token']
    channel_id = channels.channels_create(token, "Channel1", True)["channel_id"]
    standup_status = standup.standup_active(token, channel_id)
    assert (standup_status == {'is_active': False, 'time_finish': None})

def test_invalid_channel():
    clear()
    user = auth.auth_register("jonathon@gmail.com", "password", "John", "Smith")
    token = user['token']
    channel_id = 999
    with pytest.raises(InputError):
        standup.standup_active(token, channel_id)
    clear()
