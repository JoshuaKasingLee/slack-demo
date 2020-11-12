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
from other import clear

def test_standup_start():
    clear()
    user = auth.auth_register("jonathon@gmail.com", "password", "John", "Smith")
    token = user['token']
    channel_id = channels.channels_create(token, "Channel1", True)["channel_id"]
    length = 2
    time_finish = standup.standup_start(token, channel_id, length)
    standup_status = standup.standup_active(token, channel_id)
    assert (standup_status == {'is_active': True, 'time_finish': time_finish['time_finish']})

def test_invalid_channel():
    clear()
    user = auth.auth_register("jonathon@gmail.com", "password", "John", "Smith")
    token = user['token']
    channel_id = 999
    length = 2
    with pytest.raises(InputError):
        standup.standup_start(token, channel_id, length)
    clear()

def test_standup_already_exists():
    clear()
    user = auth.auth_register("jonathon@gmail.com", "password", "John", "Smith")
    token = user['token']
    channel_id = channels.channels_create(token, "Channel1", True)["channel_id"]
    length = 3
    standup.standup_start(token, channel_id, length)
    with pytest.raises(InputError):
        standup.standup_start(token, channel_id, length)
    clear()

def test_standup_ended():
    clear()
    user = auth.auth_register("jonathon@gmail.com", "password", "John", "Smith")
    token = user['token']
    channel_id = channels.channels_create(token, "Channel1", True)["channel_id"]
    length = 1
    standup.standup_start(token, channel_id, length)
    time.sleep(4)
    standup_status = standup.standup_active(token, channel_id)
    
    assert (standup_status == {'is_active': False, 'time_finish': None})
    clear()


def test_standup_mulitple():
    clear()
    user = auth.auth_register("jonathon@gmail.com", "password", "John", "Smith")
    token = user['token']
    channel_id = channels.channels_create(token, "Channel1", True)["channel_id"]
    length = 1
    standup.standup_start(token, channel_id, length)
    time.sleep(4)
    standup_status = standup.standup_active(token, channel_id)
    
    assert (standup_status == {'is_active': False, 'time_finish': None})
    clear()
