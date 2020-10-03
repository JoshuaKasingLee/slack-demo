import pytest
import database
import channel_messages
import error

def test_no_messages():
    (u_id, token) = auth.auth_register("user1@gmail.com", "password", "user1", "lastname1")
    channel_id = channels.channels_create(token, "channel1", True)
    db.channels_and_messages[channel_id] = [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ]
    assert(channel_messages(token, channel_id, 0) == {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
        'start': 0,
        'end': 0,
    })