import pytest
from message import message_react, message_unreact
from other import clear, search
import channel
import channels
import auth
import message
from error import AccessError, InputError

def test_unreact_one() :
    clear()
    user = auth.auth_register("jonathon@gmail.com", "password", "John", "Smith")
    token = user['token']
    u_id = user['u_id']
    channel_id = channels.channels_create(token, "Channel1", True)["channel_id"]
    msg_id = message.message_send(token, channel_id, "Hello Comp1531")['message_id']
    msg_time = channel.channel_messages(token, channel_id, 0)['messages'][0]['time_created']
    message_react(token, msg_id, 1)
    message_unreact(token, msg_id, 1)
    assert search(token, "o") == {
        'messages': [
            {
                'message_id': msg_id,
                'u_id': u_id,
                'message': 'Hello Comp1531',
                'time_created': msg_time,
                'reacts': [{'react_id': 1, 'u_ids': [], 'is_this_user_reacted': False }],
                'is_pinned': False,
            }
        ]
    }
    clear()

def test_remove_react_keep_one() :
    clear()
    user = auth.auth_register("jonathon@gmail.com", "password", "John", "Smith")
    token = user['token']
    u_id = user['u_id']
    user_2 = auth.auth_register("alexjones@gmail.com", "password", "Alex", "Jones")
    token_2 = user_2['token']
    u_id_2 = user_2['u_id']
    channel_id = channels.channels_create(token, "Channel1", True)["channel_id"]
    channel.channel_join(token_2, channel_id)
    msg_id = message.message_send(token, channel_id, "Hello Comp1531")['message_id']
    msg_id_2 = message.message_send(token, channel_id, "Helloo")['message_id']
    msg_time = channel.channel_messages(token, channel_id, 0)['messages'][1]['time_created']
    msg_time_2 = channel.channel_messages(token, channel_id, 0)['messages'][0]['time_created']
    message_react(token, msg_id)
    message_unreact(token, msg_id, 1)
    message_react(token_2, msg_id_2)
    assert search(token, "o") == {
        'messages': [
            {
                'message_id': msg_id,
                'u_id': u_id,
                'message': 'Hello Comp1531',
                'time_created': msg_time,
                'reacts': [{'react_id': 1, 'u_ids': [], 'is_this_user_reacted': False }],
                'is_pinned': True,
            }, {
                'message_id': msg_id_2,
                'u_id': u_id,
                'message': 'Helloo',
                'time_created': msg_time_2,
                'reacts': [{'react_id': 1, 'u_ids': [u_id_2], 'is_this_user_reacted': False }],
                'is_pinned': False,
            }
        ]
    }
    clear()
    
def test_two_reacts() :
    clear()
    user = auth.auth_register("jonathon@gmail.com", "password", "John", "Smith")
    token = user['token']
    u_id = user['u_id']
    user_2 = auth.auth_register("alexjones@gmail.com", "password", "Alex", "Jones")
    token_2 = user_2['token']
    u_id_2 = user_2['u_id']
    channel_id = channels.channels_create(token, "Channel1", True)["channel_id"]
    channel.channel_join(token_2, channel_id)
    msg_id = message.message_send(token, channel_id, "Hello Comp1531")['message_id']
    msg_id_2 = message.message_send(token, channel_id, "Helloo")['message_id']
    msg_time = channel.channel_messages(token, channel_id, 0)['messages'][1]['time_created']
    msg_time_2 = channel.channel_messages(token, channel_id, 0)['messages'][0]['time_created']
    message_react(token, msg_id_2)
    message_react(token_2, msg_id_2)
    message_unreact(token, msg_id, 1)
    assert search(token_2, "o") == {
        'messages': [
            {
                'message_id': msg_id,
                'u_id': u_id,
                'message': 'Hello Comp1531',
                'time_created': msg_time,
                'reacts': [{'react_id': 1, 'u_ids': [], 'is_this_user_reacted': False }],
                'is_pinned': True,
            }, {
                'message_id': msg_id_2,
                'u_id': u_id,
                'message': 'Helloo',
                'time_created': msg_time_2,
                'reacts': [{'react_id': 1, 'u_ids': [u_id_2], 'is_this_user_reacted': True }],
                'is_pinned': True,
            }
        ]
    }
    clear()

def test_wrong_channel() :
    clear()
    user = auth.auth_register("jonathon@gmail.com", "password", "John", "Smith")
    token = user['token']
    user_2 = auth.auth_register("sallychampion@gmail.com", "password", "Sally", "Champion") 
    token_2 = user_2['token']
    channel_id = channels.channels_create(token, "Channel1", True)["channel_id"]
    channel.channel_join(token_2,channel_id)
    msg_id = message.message_send(token, channel_id, "Hello Comp1531") ["message_id"]
    message_react(token_2, msg_id, 1)
    channel.channel_leave(token_2,channel_id)
    with pytest.raises(AccessError):
        message_unreact(token_2, msg_id, 1)
    clear()


def test_message_already_unreacted() :
    clear()
    user = auth.auth_register("jonathon@gmail.com", "password", "John", "Smith")
    token = user['token']
    channel_id = channels.channels_create(token, "Channel1", True)["channel_id"]
    msg_id = message.message_send(token, channel_id, "Hello Comp1531")["message_id"]
    with pytest.raises(InputError):
        message_unreact(token,msg_id, 1)
    clear()

def test_message_id_invalid() :
    clear()
    user = auth.auth_register("jonathon@gmail.com", "password", "John", "Smith")
    token = user['token']
    channel_id = channels.channels_create(token, "Channel1", True)["channel_id"]
    msg_id = message.message_send(token, channel_id, "Hello Comp1531")['message_id']
    message_react(token, msg_id, 1)
    with pytest.raises(InputError):
        message_unreact(token,3, 1)
    clear()

def test_invalid_token():
    clear()
    user = auth.auth_register("jonathon@gmail.com", "password", "John", "Smith")
    token = user['token']
    channel_id = channels.channels_create(token, "Channel1", True)["channel_id"]
    msg_id = message.message_send(token, channel_id, "Hello Comp1531")["message_id"]
    message_react(token, msg_id, 1)
    with pytest.raises(AccessError):
        message_unreact(4, msg_id, 1)
    clear()

def test_react_id_invalid() :
    clear()
    user = auth.auth_register("jonathon@gmail.com", "password", "John", "Smith")
    token = user['token']
    channel_id = channels.channels_create(token, "Channel1", True)["channel_id"]
    msg_id = message.message_send(token, channel_id, "Hello Comp1531")['message_id']
    message_react(token, msg_id, 1)
    with pytest.raises(InputError):
        message_unreact(token, msg_id, 3)
    clear()
