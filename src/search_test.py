import pytest
from other import search, clear
import channel
import channels
import auth
import message
from error import AccessError
from datetime import date

def test_empty():
    clear()
    user = auth.auth_register("jonathon@gmail.com", "password", "John", "Smith")
    token = user['token']
    channels.channels_create(token, "Channel1", True)["channel_id"]
    assert search(token, "World") == {'messages': []}

def test_one() :
    clear()
    user = auth.auth_register("jonathon@gmail.com", "password", "John", "Smith")
    token = user['token']
    u_id = user['u_id']
    channel_id = channels.channels_create(token, "Channel1", True)["channel_id"]
    msg_id_1 = message.message_send(token, channel_id, "Hello World")['message_id']
    msg_time_1 = channel.channel_messages(token, channel_id, 0)['messages'][0]['time_created']
    assert search(token, "World") == {
        'messages': [
            {
                'message_id': msg_id_1,
                'u_id': u_id,
                'message': 'Hello World',
                'time_created': msg_time_1,
            }
        ]
    }

    clear()
    
def test_two_messages_one_match() :
    clear()
    user = auth.auth_register("jonathon@gmail.com", "password", "John", "Smith")
    token = user['token']
    u_id = user['u_id']
    channel_id = channels.channels_create(token, "Channel1", True)["channel_id"]
    msg_id_1 = message.message_send(token, channel_id, "Hello World")['message_id']
    msg_time_1 = channel.channel_messages(token, channel_id, 0)['messages'][0]['time_created']
    message.message_send(token, channel_id, "This is a test message")
    assert search(token, "World") == {
        'messages': [
            {
                'message_id': msg_id_1,
                'u_id': u_id,
                'message': 'Hello World',
                'time_created': msg_time_1,
            }
        ]
    }
    clear()

def test_two_messages_two_match() :
    clear()
    user = auth.auth_register("jonathon@gmail.com", "password", "John", "Smith")
    token = user['token']
    u_id = user['u_id']
    channel_id = channels.channels_create(token, "Channel1", True)["channel_id"]
    msg_id_1 = message.message_send(token, channel_id, "Hello World")['message_id']
    msg_id_2 = message.message_send(token, channel_id, "Hello, this is a test message")['message_id']
    msg_time_1 = channel.channel_messages(token, channel_id, 0)['messages'][1]['time_created']
    msg_time_2 = channel.channel_messages(token, channel_id, 0)['messages'][0]['time_created']
    assert search(token, "Hello") == {
        'messages': [
            {
                'message_id': msg_id_1,
                'u_id': u_id,
                'message': 'Hello World',
                'time_created': msg_time_1,
            }, {
                'message_id': msg_id_2,
                'u_id': u_id,
                'message': 'Hello, this is a test message',
                'time_created': msg_time_2,
            }
        ]
    }
    clear()

def test_three_messages_two_match() :
    clear()
    user = auth.auth_register("jonathon@gmail.com", "password", "John", "Smith")
    token = user['token']
    u_id = user['u_id']
    channel_id = channels.channels_create(token, "Channel1", True)["channel_id"]
    message.message_send(token, channel_id, "Hello World")
    msg_id_1 = message.message_send(token, channel_id, "This is a test message")['message_id']
    msg_id_2 = message.message_send(token, channel_id, "then he said to test")['message_id']
    msg_time_1 = channel.channel_messages(token, channel_id, 0)['messages'][1]['time_created']
    msg_time_2 = channel.channel_messages(token, channel_id, 0)['messages'][0]['time_created']
    assert search(token, "test") == {
        'messages': [
            {
                'message_id': msg_id_1,
                'u_id': u_id,
                'message': 'This is a test message',
                'time_created': msg_time_1,
            }, {
                'message_id': msg_id_2,
                'u_id': u_id,
                'message': 'then he said to test',
                'time_created': msg_time_2,
            }
        ]
    }
    clear()

def test_mult_match_messages_but_diff_channels() :
    clear()
    user = auth.auth_register("jonathon@gmail.com", "password", "John", "Smith")
    token = user['token']
    u_id = user['u_id']
    user_2 = auth.auth_register("sallychampion@gmail.com", "password", "Sally", "Champion") 
    token_2 = user_2['token']
    channel_id = channels.channels_create(token, "Channel1", True)["channel_id"]
    channel_id_2 = channels.channels_create(token_2, "Channel1", True)["channel_id"]
    channel.channel_join(token, channel_id_2)
    message.message_send(token, channel_id, "Hello Comp1531")
    msg_id_1 = message.message_send(token, channel_id_2, 'Comp1531 is fun')['message_id']
    msg_time_1 = channel.channel_messages(token, channel_id_2, 0)['messages'][0]['time_created']
    message.message_send(token, channel_id, "i do Comp1531")
    assert search(token_2, "1531") == {
        'messages': [
            {
                'message_id': msg_id_1,
                'u_id': u_id,
                'message': 'Comp1531 is fun',
                'time_created': msg_time_1,
            }
        ]
    }
    clear()

def test_matching_letter() :
    clear()
    user = auth.auth_register("jonathon@gmail.com", "password", "John", "Smith")
    token = user['token']
    u_id = user['u_id']
    channel_id = channels.channels_create(token, "Channel1", True)["channel_id"]
    msg_id_1 = message.message_send(token, channel_id, "Hello Comp1531")['message_id']
    message.message_send(token, channel_id, "Hi abcdefg")
    msg_id_2 = message.message_send(token, channel_id, "i do Comp1531")['message_id']
    msg_time_1 = channel.channel_messages(token, channel_id, 0)['messages'][2]['time_created']
    msg_time_2 = channel.channel_messages(token, channel_id, 0)['messages'][0]['time_created']
    assert search(token, "o") == {
        'messages': [
            {
                'message_id': msg_id_1,
                'u_id': u_id,
                'message': 'Hello Comp1531',
                'time_created': msg_time_1,
            }, {
                'message_id': msg_id_2,
                'u_id': u_id,
                'message': 'i do Comp1531',
                'time_created': msg_time_2,
            }
        ]
    }
    clear()

def test_not_part_of_channel() :
    clear()
    user = auth.auth_register("jonathon@gmail.com", "password", "John", "Smith")
    token = user['token']
    channel_id = channels.channels_create(token, "Channel1", True)["channel_id"]
    user_2 = auth.auth_register("sallychampion@gmail.com", "password", "Sally", "Champion") 
    token_2 = user_2['token']
    message.message_send(token, channel_id, "Hello Comp1531")
    message.message_send(token, channel_id, "Hi abcdefg")
    message.message_send(token, channel_id, "i do Comp1531")
    assert search(token_2, "o") == {
        'messages': []
    }
    clear()

def test_invalid_token(): # wrong user token - accesserror
    clear()
    auth.auth_register("kellyzhou@gmail.com", "password", "Kelly", "Zhou")
    with pytest.raises(AccessError):
        search(4, "test")
    clear()
