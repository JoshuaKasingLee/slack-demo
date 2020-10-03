from channel_messages import channel_messages
import pytest
import database
import error
import auth
## idk what to put here

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
clear()

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
clear()

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
clear()

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


def test_no_messages(): # raise InputError
    (u_id, token) = auth.auth_register("user1@gmail.com", "password", "user1", "lastname1")
    channel_id = channels.channels_create(token, "channel1", True)
    db.channels_and_messages[channel_id] = []
    with pytest.raises(InputError):
        channel_messages(token, channel_id, 1)

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

def test_invalid_token(): # invalid token - AccessError
    channel_id = channels.channels_create(token, "channel1", True)
    db.channels_and_messages[channel_id] = []
    with pytest.raises(AccessError):
        channel_messages('heyheyhey', channel_id, 0)

def test_missing_channel(): # invalid channel_id - InputError (bc of channel_details spec)
    (u_id, token) = auth.auth_register("user1@gmail.com", "password", "user1", "lastname1")
    with pytest.raises(InputError):
        channel_messages(token, channel_id, 0)

def test_missing_user(): # user doesn't exist - AccessError
    channel_id = channels.channels_create(token, "channel1", True)
    db.channels_and_messages[channel_id] = []
    with pytest.raises(AccessError):
        channel_messages(22, channel_id, 0)