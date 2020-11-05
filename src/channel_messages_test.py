from channel import channel_messages
import channel
import channels
import message
import pytest
from error import InputError as InputError
from error import AccessError as AccessError
import auth
from other import clear


def test_invalid_token(): # invalid token - AccessError
    clear()
    user = auth.auth_register("test1@gmail.com", "password", "John", "Smith")
    token = user['token']
    channel_id = channels.channels_create(token, "channel1", True)['channel_id']

    with pytest.raises(AccessError):
        channel_messages('heyheyhey', channel_id, 1)
    clear()

def test_missing_channel(): # invalid channel_id - InputError (bc of channel_details spec)
    clear()
    user = auth.auth_register("test1@gmail.com", "password", "John", "Smith")
    token = user['token']
    with pytest.raises(InputError):
        channel_messages(token, 99, 0) # 99 is an arbitrary nonexistent channel_id
    clear()

def test_missing_user(): # user doesn't exist - AccessError
    clear()
    user = auth.auth_register("test1@gmail.com", "password", "John", "Smith")
    token = user['token']
    channel_id = channels.channels_create(token, "channel1", True)['channel_id']

    with pytest.raises(AccessError):
        channel_messages(99, channel_id, 1) # 99 is an arbitrary nonexistent token
    clear()

def test_negative_index(): # invalid index - InputError
    clear()
    user = auth.auth_register("test1@gmail.com", "password", "John", "Smith")
    token = user['token']
    channel_id = channels.channels_create(token, "channel1", True)['channel_id']
    with pytest.raises(InputError):
        channel_messages(token, channel_id, -10)
    clear()

def test_message_chronology():
    clear()
    user = auth.auth_register("jonathon@gmail.com", "password", "John", "Smith")
    token = user['token']
    channel_id = channels.channels_create(token, "Channel1", True)["channel_id"]
    message.message_send(token, channel_id, "first")['message_id']
    message.message_send(token, channel_id, "second")['message_id']
    msg_time_1 = channel.channel_messages(token, channel_id, 0)['messages'][1]['time_created']
    msg_time_2 = channel.channel_messages(token, channel_id, 0)['messages'][0]['time_created']
    assert (msg_time_2 > msg_time_1)

def test_pagination():
    clear()
    user = auth.auth_register("jonathon@gmail.com", "password", "John", "Smith")
    token = user['token']
    channel_id = channels.channels_create(token, "Channel1", True)["channel_id"]
    i = 0
    while i < 55:
        message_to_send = "message " + str(i)
        message.message_send(token, channel_id, message_to_send)
        i += 1
    end = channel.channel_messages(token, channel_id, 1)['end']
    assert (end == 51)

