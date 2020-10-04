from channel import channel_messages
import channels
import pytest
from error import InputError as InputError
from error import AccessError as AccessError
import auth
from other import clear


'''
def test_one_message():
    (u_id, token) = auth.auth_register("user1@gmail.com", "password", "user1", "lastname1")
    channel_id = channels.channels_create(token, "channel1", True)
    db.channels_and_messages[channel_id] = [
            {
                'message_id': 0,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ]
    assert(channel_messages(token, channel_id, 0) == {
        'messages': [
            {
                'message_id': 0,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
        'start': 0,
        'end': -1,
    }
    )
database.clear()

def test_two_messages():
    (u_id, token) = auth.auth_register("user1@gmail.com", "password", "user1", "lastname1")
    channel_id = channels.channels_create(token, "channel1", True)
    db.channels_and_messages[channel_id] = [
            {
                'message_id': 0,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }, {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426788,
            }

        ]
    assert(channel_messages(token, channel_id, 0) == {
        'messages': [
            {
                'message_id': 0,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }, {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426788,
            }
        ],
        'start': 0,
        'end': -1,
    }
    )
database.clear()

def test_two_messages_start_1():
    (u_id, token) = auth.auth_register("user1@gmail.com", "password", "user1", "lastname1")
    channel_id = channels.channels_create(token, "channel1", True)
    db.channels_and_messages[channel_id] = [
            {
                'message_id': 0,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }, {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426788,
            }, {
                'message_id': 2,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426787,
            }

        ]
    assert(channel_messages(token, channel_id, 1) == {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426788,
            }, {
                'message_id': 2,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426787,
            }
        ],
        'start': 1,
        'end': -1,
    }
    )
database.clear()

def test_return_index(): # so it returns an index that isn't -1
    (u_id, token) = auth.auth_register("user1@gmail.com", "password", "user1", "lastname1")
    channel_id = channels.channels_create(token, "channel1", True)
    messages_list = []
    messages_list_50 = []
    for i in range(52):
        messages_list.append(
            {
                'message_id': i,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426788 - i,
            }
        )
    for i in range(49):
        messages_list_50.append(
            {
                'message_id': i,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426788 - i,
            }
        )
    db.channels_and_messages[channel_id] = messages_list
    assert(channel_messages(token, channel_id, 0) == {
        'messages': messages_list_50,
        'start': 0,
        'end': 50,
    }
    )
database.clear()

def test_no_messages(): # raise InputError
    (u_id, token) = auth.auth_register("user1@gmail.com", "password", "user1", "lastname1")
    channel_id = channels.channels_create(token, "channel1", True)
    db.channels_and_messages[channel_id] = []
    with pytest.raises(InputError):
        channel_messages(token, channel_id, 1)
database.clear()

def test_large_index(): # index too large, raise InputError
    (u_id, token) = auth.auth_register("user1@gmail.com", "password", "user1", "lastname1")
    channel_id = channels.channels_create(token, "channel1", True)
    db.channels_and_messages[channel_id] = [
            {
                'message_id': 0,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ]
    with pytest.raises(InputError):
        channel_messages(token, channel_id, 10)
database.clear()
'''

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
    u_id = user['u_id']
    token = user['token']
    with pytest.raises(InputError):
        channel_messages(token, 99, 0) # 99 is an arbitrary nonexistent channel_id
    clear()

def test_missing_user(): # user doesn't exist - AccessError
    clear()
    user = auth.auth_register("test1@gmail.com", "password", "John", "Smith")
    u_id = user['u_id']
    token = user['token']
    channel_id = channels.channels_create(token, "channel1", True)
    # db.channels_and_messages[channel_id] = []
    with pytest.raises(AccessError):
        channel_messages(99, channel_id, 1) # 99 is an arbitrary nonexistent token
    clear()

def test_negative_index(): # invalid index - InputError
    clear()
    user = auth.auth_register("test1@gmail.com", "password", "John", "Smith")
    u_id = user['u_id']
    token = user['token']
    channel_id = channels.channels_create(token, "channel1", True)
    with pytest.raises(InputError):
        channel_messages(token, channel_id, -10)
    clear()