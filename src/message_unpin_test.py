import pytest
from message import message_unpin, message_pin
from other import clear, search
import channel
import channels
import auth
import message
from error import AccessError, InputError

def test_unpinning_one() :
    clear()
    user = auth.auth_register("jonathon@gmail.com", "password", "John", "Smith")
    token = user['token']
    u_id = user['u_id']
    channel_id = channels.channels_create(token, "Channel1", True)["channel_id"]
    msg_id = message.message_send(token, channel_id, "Hello Comp1531")['message_id']
    msg_time = channel.channel_messages(token, channel_id, msg_id)['messages'][0]['time_created']
    message_pin(token, msg_id)
    message_unpin(token, msg_id)
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

def test_unpinning_one_but_two_messages() :
    clear()
    user = auth.auth_register("jonathon@gmail.com", "password", "John", "Smith")
    token = user['token']
    u_id = user['u_id']
    channel_id = channels.channels_create(token, "Channel1", True)["channel_id"]
    msg_id = message.message_send(token, channel_id, "Hello Comp1531")['message_id']
    msg_id_2 = message.message_send(token, channel_id, "Helloo")['message_id']
    msg_time = channel.channel_messages(token, channel_id, msg_id)['messages'][0]['time_created']
    msg_time_2 = channel.channel_messages(token, channel_id, msg_id_2)['messages'][0]['time_created']
    message_pin(token, msg_id)
    message_unpin(token, msg_id)
    assert search(token, "o") == {
        'messages': [
            {
                'message_id': msg_id,
                'u_id': u_id,
                'message': 'Hello Comp1531',
                'time_created': msg_time,
                'reacts': [{'react_id': 1, 'u_ids': [], 'is_this_user_reacted': False }],
                'is_pinned': False,
            }, {
                'message_id': msg_id_2,
                'u_id': u_id,
                'message': 'Helloo',
                'time_created': msg_time_2,
                'reacts': [{'react_id': 1, 'u_ids': [], 'is_this_user_reacted': False }],
                'is_pinned': False,
            }
        ]
    }
    clear()
    
def test_unpinning_two() :
    clear()
    user = auth.auth_register("jonathon@gmail.com", "password", "John", "Smith")
    token = user['token']
    u_id = user['u_id']
    channel_id = channels.channels_create(token, "Channel1", True)["channel_id"]
    msg_id = message.message_send(token, channel_id, "Hello Comp1531")['message_id']
    msg_id_2 = message.message_send(token, channel_id, "Helloo")['message_id']
    msg_time = channel.channel_messages(token, channel_id, msg_id)['messages'][0]['time_created']
    msg_time_2 = channel.channel_messages(token, channel_id, msg_id_2)['messages'][0]['time_created']
    message_pin(token, msg_id)
    message_unpin(token, msg_id)
    message_pin(token, msg_id_2)
    message_unpin(token, msg_id_2)
    assert search(token, "o") == {
        'messages': [
            {
                'message_id': msg_id,
                'u_id': u_id,
                'message': 'Hello Comp1531',
                'time_created': msg_time,
                'reacts': [{'react_id': 1, 'u_ids': [], 'is_this_user_reacted': False }],
                'is_pinned': False,
            }, {
                'message_id': msg_id_2,
                'u_id': u_id,
                'message': 'Helloo',
                'time_created': msg_time_2,
                'reacts': [{'react_id': 1, 'u_ids': [], 'is_this_user_reacted': False }],
                'is_pinned': False,
            }
        ]
    }
    clear()

def test_not_owner() :
    clear()
    token = auth.auth_register("jonathon@gmail.com", "password", "John", "Smith")['token']
    user_2 = auth.auth_register("sallychampion@gmail.com", "password", "Sally", "Champion") 
    token_2 = user_2['token']
    channel_id = channels.channels_create(token, "Channel1", True)["channel_id"]
    channel.channel_join(token_2, channel_id)
    msg_id = message.message_send(token, channel_id, "Hello Comp1531") ["message_id"]
    message_pin(token, msg_id)
    with pytest.raises(AccessError):
        message_unpin(token_2, msg_id)
    clear()

def test_wrong_channel() :
    clear()
    user = auth.auth_register("jonathon@gmail.com", "password", "John", "Smith")
    token = user['token']
    user_2 = auth.auth_register("sallychampion@gmail.com", "password", "Sally", "Champion") 
    token_2 = user_2['token']
    channel_id = channels.channels_create(token, "Channel1", True)["channel_id"]
    msg_id = message.message_send(token, channel_id, "Hello Comp1531") ["message_id"]
    message_pin(token, msg_id)
    with pytest.raises(AccessError):
        message_unpin(token_2, msg_id)
    clear()


def message_id_already_unpinned() :
    clear()
    user = auth.auth_register("jonathon@gmail.com", "password", "John", "Smith")
    token = user['token']
    channel_id = channels.channels_create(token, "Channel1", True)["channel_id"]
    msg_id = message.message_send(token, channel_id, "Hello Comp1531")["message_id"]
    with pytest.raises(InputError):
        message_unpin(token,msg_id)
    clear()

def message_id_invalid() :
    clear()
    user = auth.auth_register("jonathon@gmail.com", "password", "John", "Smith")
    token = user['token']
    channel_id = channels.channels_create(token, "Channel1", True)["channel_id"]
    msg_id = message.message_send(token, channel_id, "Hello Comp1531")['message_id']
    message_pin(token, msg_id)
    with pytest.raises(InputError):
        message_unpin(token,3)
    clear()

def test_invalid_token(): # wrong user token - accesserror
    clear()
    user = auth.auth_register("jonathon@gmail.com", "password", "John", "Smith")
    token = user['token']
    channel_id = channels.channels_create(token, "Channel1", True)["channel_id"]
    msg_id = message.message_send(token, channel_id, "Hello Comp1531")["message_id"]
    message_pin(token, msg_id)
    with pytest.raises(AccessError):
        message_unpin(4, msg_id)
    clear()
