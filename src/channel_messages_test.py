from channel import channel_messages
import channels
import pytest
from error import InputError as InputError
from error import AccessError as AccessError
import auth
from other import clear


def test_invalid_token(): # invalid token - AccessError
    clear()
    user = auth.auth_register("test1@gmail.com", "password", "John", "Smith")
    token = user['token']
    channel_id = channels.channels_create(token, "channel1", True)
    # db.channels_and_messages[channel_id] = []
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
    channel_id = channels.channels_create(token, "channel1", True)
    # db.channels_and_messages[channel_id] = []
    with pytest.raises(AccessError):
        channel_messages(99, channel_id, 1) # 99 is an arbitrary nonexistent token
    clear()

def test_negative_index(): # invalid index - InputError
    clear()
    user = auth.auth_register("test1@gmail.com", "password", "John", "Smith")
    token = user['token']
    channel_id = channels.channels_create(token, "channel1", True)
    with pytest.raises(InputError):
        channel_messages(token, channel_id, -10)
    clear()