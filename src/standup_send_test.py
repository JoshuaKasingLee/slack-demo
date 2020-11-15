import pytest
from error import AccessError
from error import InputError
import channels
import channel
import auth
from other import clear
import standup
#from datetime import datetime
#from datetime import timedelta
import time

def test_standup_send_single():
    clear()
    user = auth.auth_register("jonathon@gmail.com", "password", "John", "Smith")
    token = user['token']
    channel_id = channels.channels_create(token, "Channel1", True)["channel_id"]
    length = 1
    standup.standup_start(token, channel_id, length)
    standup.standup_send(token, channel_id, 'i am john')
    time.sleep(2)
    messages = channel.channel_messages(token, channel_id, 0)
    assert (messages['messages'][0]['message'] == 'John: i am john')
    clear()

def test_standup_send_multiple():
    clear()
    user = auth.auth_register("jonathon@gmail.com", "password", "John", "Smith")
    token = user['token']
    user_2 = auth.auth_register("jofnathon@gmail.com", "password", "Nhoj", "Htims")
    token_2 = user_2['token']
    channel_id = channels.channels_create(token, "Channel1", True)["channel_id"]
    channel.channel_join(token_2, channel_id)
    length = 1
    standup.standup_start(token, channel_id, length)
    standup.standup_send(token, channel_id, 'i am john')
    standup.standup_send(token_2, channel_id, 'i am johns evil twin')
    time.sleep(2)
    messages = channel.channel_messages(token, channel_id, 0)
    assert (messages['messages'][0]['message'] == 'John: i am john\nNhoj: i am johns evil twin')
    clear()

def test_standup_send_empty():
    clear()
    user = auth.auth_register("jonathon@gmail.com", "password", "John", "Smith")
    token = user['token']
    channel_id = channels.channels_create(token, "Channel1", True)["channel_id"]
    length = 1
    standup.standup_start(token, channel_id, length)
    standup.standup_send(token, channel_id, '')
    time.sleep(2)
    messages = channel.channel_messages(token, channel_id, 0)
    assert (messages['messages'][0]['message'] == 'John: ')
    clear()

def test_standup_send_multiple_alone():
    clear()
    user = auth.auth_register("jonathon@gmail.com", "password", "John", "Smith")
    token = user['token']
    channel_id = channels.channels_create(token, "Channel1", True)["channel_id"]
    length = 1
    standup.standup_start(token, channel_id, length)
    standup.standup_send(token, channel_id, 'i am john')
    standup.standup_send(token, channel_id, 'i am johns evil twin, jk')
    time.sleep(2)
    messages = channel.channel_messages(token, channel_id, 0)
    assert (messages['messages'][0]['message'] == 'John: i am john\nJohn: i am johns evil twin, jk')
    clear()

def test_standup_send_inactive_test():
    clear()
    user = auth.auth_register("jonathon@gmail.com", "password", "John", "Smith")
    token = user['token']
    channel_id = channels.channels_create(token, "Channel1", True)["channel_id"]
    with pytest.raises(InputError):
        standup.standup_send(token, channel_id, 'hey')
    clear()

def test_standup_send_long_test():
    clear()
    string = 'lmao'
    for i in range(100):
        string += '0123456789'
    user = auth.auth_register("jonathon@gmail.com", "password", "John", "Smith")
    token = user['token']
    channel_id = channels.channels_create(token, "Channel1", True)["channel_id"]
    standup.standup_start(token, channel_id, 1) # 10 seconds should be long enough
    with pytest.raises(InputError):
        standup.standup_send(token, channel_id, string)
    clear()

def test_standup_send_channel_test():
    clear()
    user = auth.auth_register("jonathon@gmail.com", "password", "John", "Smith")
    token = user['token']
    channel_id = channels.channels_create(token, "Channel1", True)["channel_id"]
    standup.standup_start(token, channel_id, 1)
    with pytest.raises(InputError):
        standup.standup_send(token, 99, 'hey')
    clear()

def test_standup_send_unauthorized_test():
    clear()
    user = auth.auth_register("jonathon@gmail.com", "password", "John", "Smith")
    token = user['token']
    user_2 = auth.auth_register("jofnathon@gmail.com", "password", "Nhoj", "Htims")
    token_2 = user_2['token']
    channel_id = channels.channels_create(token, "Channel1", True)["channel_id"]
    standup.standup_start(token, channel_id, 1)
    with pytest.raises(AccessError):
        standup.standup_send(token_2, channel_id, 'hey')
    clear()

def test_standup_send_token_test():
    clear()
    user = auth.auth_register("jonathon@gmail.com", "password", "John", "Smith")
    token = user['token']
    channel_id = channels.channels_create(token, "Channel1", True)["channel_id"]
    standup.standup_start(token, channel_id, 1)
    with pytest.raises(AccessError):
        standup.standup_send('bad_token', channel_id, 'hey')
    clear()