import pytest
import re
from subprocess import Popen, PIPE
import signal
from time import sleep
import requests
from datetime import date

data_in_1 = {
        'email' : "jonathon@gmail.com",
        'password' : "password",
        'name_first' : "John",
        'name_last' : "Smith"
    }

data_in_2 = {
        'email' : "sallychampion@gmail.com",
        'password' : "password",
        'name_first' : "Sally",
        'name_last' : "Champion"
    }

token = {}

@pytest.fixture
def url():
    url_re = re.compile(r' \* Running on ([^ ]*)')
    server = Popen(["python3", "server.py"], stderr=PIPE, stdout=PIPE)
    line = server.stderr.readline()
    local_url = url_re.match(line.decode())
    if local_url:
        yield local_url.group(1)
        # Terminate the server
        server.send_signal(signal.SIGINT)
        waited = 0
        while server.poll() is None and waited < 5:
            sleep(0.1)
            waited += 0.1
        if server.poll() is None:
            server.kill()
    else:
        server.kill()
        raise Exception("Couldn't get URL from local server")    

def test_empty(url):
    requests.delete(url + 'clear')
    response = requests.post(url + 'auth/register', json = data_in_1)
    payload = response.json()
    token['token'] = payload['token']
    data_in = {
        'token' : token['token'],
        'name' : "Channel1",
        'is_public' : True
    }

    response = requests.post(url + 'channels/create', json = data_in)
    info = {
        'token' : token['token'],
        'query_str' : "World",
    }
    response = requests.get(url + 'search', info)
    payload = response.json()
    assert payload == {'messages': []}
    requests.delete(url + 'clear')

def test_one(url) :
    requests.delete(url + 'clear')
    response = requests.post(url + 'auth/register', json = data_in_1)
    payload = response.json()
    token['token'] = payload['token']
    u_id = payload['u_id']
    data_in = {
        'token' : token['token'],
        'name' : "Channel1",
        'is_public' : True
    }

    response = requests.post(url + 'channels/create', json = data_in)
    channel_id = response.json()
    message_input = {
        'token' : token['token'],
        'channel_id' : channel_id['channel_id'],
        'message' : "Hello World",
    }
    response = requests.post(url + 'message/send', json = message_input)
    msg_id_1 = response.json()
    info = {
        'token' : token['token'],
        'channel_id' : channel_id['channel_id'],
        'start' : 0,
    }
    response = requests.get(url + 'channel/messages', info)
    messages = response.json()
    messages = messages['messages']
    time = messages[0]['time_created']
    info = {
        'token' : token['token'],
        'query_str' : "World",
    }
    response = requests.get(url + 'search', info)
    payload = response.json()
    assert payload == {
        'messages': [
            {
                'message_id': msg_id_1['message_id'],
                'u_id': u_id,
                'message': 'Hello World',
                'time_created': time,
            }
        ]
    }
    requests.delete(url + 'clear')
    
def test_two_messages_one_match(url) :
    requests.delete(url + 'clear')
    response = requests.post(url + 'auth/register', json = data_in_1)
    payload = response.json()
    token['token'] = payload['token']
    u_id = payload['u_id']
    data_in = {
        'token' : token['token'],
        'name' : "Channel1",
        'is_public' : True
    }
    response = requests.post(url + 'channels/create', json = data_in)
    channel_id = response.json()
    message_input = {
        'token' : token['token'],
        'channel_id' : channel_id['channel_id'],
        'message' : "Hello World",
    }
    response = requests.post(url + 'message/send', json = message_input)
    msg_id_1 = response.json()
    info = {
        'token' : token['token'],
        'channel_id' : channel_id['channel_id'],
        'start' : 0,
    }
    response = requests.get(url + 'channel/messages', info)
    messages = response.json()
    messages = messages['messages']
    time = messages[0]['time_created']
    info = {
        'token' : token['token'],
        'query_str' : "World",
    }
    message_input = {
        'token' : token['token'],
        'channel_id' : channel_id['channel_id'],
        'message' : "This is a test message",
    }
    response = requests.post(url + 'message/send', json = message_input)
    info = {
        'token' : token['token'],
        'query_str' : "World",
    }
    response = requests.get(url + 'search', info)
    payload = response.json()
    assert payload == {
        'messages': [
            {
                'message_id': msg_id_1['message_id'],
                'u_id': u_id,
                'message': 'Hello World',
                'time_created': time,
            }
        ]
    }
    requests.delete(url + 'clear')

def test_two_messages_two_match(url) :
    requests.delete(url + 'clear')
    response = requests.post(url + 'auth/register', json = data_in_1)
    payload = response.json()
    token['token'] = payload['token']
    u_id = payload['u_id']
    data_in = {
        'token' : token['token'],
        'name' : "Channel1",
        'is_public' : True
    }

    response = requests.post(url + 'channels/create', json = data_in)
    channel_id = response.json()
    message_input = {
        'token' : token['token'],
        'channel_id' : channel_id['channel_id'],
        'message' : "Hello World",
    }
    response = requests.post(url + 'message/send', json = message_input)
    msg_id_1 = response.json()
    info = {
        'token' : token['token'],
        'channel_id' : channel_id['channel_id'],
        'start' : 0,
    }
    response = requests.get(url + 'channel/messages', info)
    messages = response.json()
    messages = messages['messages']
    time1 = messages[0]['time_created']
    info = {
        'token' : token['token'],
        'query_str' : "World",
    }
    message_input = {
        'token' : token['token'],
        'channel_id' : channel_id['channel_id'],
        'message' : "Hello, this is a test message",
    }
    response = requests.post(url + 'message/send', json = message_input)
    msg_id_2 = response.json()
    info = {
        'token' : token['token'],
        'channel_id' : channel_id['channel_id'],
        'start' : 0,
    }
    response = requests.get(url + 'channel/messages', info)
    messages = response.json()
    messages = messages['messages']
    time2 = messages[1]['time_created']
    info = {
        'token' : token['token'],
        'query_str' : "World",
    }
    info = {
        'token' : token['token'],
        'query_str' : "Hello",
    }
    response = requests.get(url + 'search', info)
    payload = response.json()
    assert payload == {
        'messages': [
            {
                'message_id': msg_id_1['message_id'],
                'u_id': u_id,
                'message': 'Hello World',
                'time_created': time1,
            }, {
                'message_id': msg_id_2['message_id'],
                'u_id': u_id,
                'message': 'Hello, this is a test message',
                'time_created': time2,
            }
        ]
    }
    requests.delete(url + 'clear')

def test_three_messages_two_match(url) :
    requests.delete(url + 'clear')
    response = requests.post(url + 'auth/register', json = data_in_1)
    payload = response.json()
    token['token'] = payload['token']
    u_id = payload['u_id']
    data_in = {
        'token' : token['token'],
        'name' : "Channel1",
        'is_public' : True
    }

    response = requests.post(url + 'channels/create', json = data_in)
    channel_id = response.json()
    message_input = {
        'token' : token['token'],
        'channel_id' : channel_id['channel_id'],
        'message' : "Hello World",
    }
    response = requests.post(url + 'message/send', json = message_input)
    message_input = {
        'token' : token['token'],
        'channel_id' : channel_id['channel_id'],
        'message' : "Hello, this is a test message",
    }
    response = requests.post(url + 'message/send', json = message_input)
    msg_id_1 = response.json()
    info = {
        'token' : token['token'],
        'channel_id' : channel_id['channel_id'],
        'start' : 0,
    }
    response = requests.get(url + 'channel/messages', info)
    messages = response.json()
    messages = messages['messages']
    time1 = messages[1]['time_created']
    info = {
        'token' : token['token'],
        'query_str' : "World",
    }
    message_input = {
        'token' : token['token'],
        'channel_id' : channel_id['channel_id'],
        'message' : "then he said to test",
    }
    response = requests.post(url + 'message/send', json = message_input)
    msg_id_2 = response.json()
    info = {
        'token' : token['token'],
        'channel_id' : channel_id['channel_id'],
        'start' : 0,
    }
    response = requests.get(url + 'channel/messages', info)
    messages = response.json()
    messages = messages['messages']
    time2 = messages[2]['time_created']
    info = {
        'token' : token['token'],
        'query_str' : "World",
    }
    info = {
        'token' : token['token'],
        'query_str' : "test",
    }
    response = requests.get(url + 'search', info)
    payload = response.json()
    assert payload == {
        'messages': [
            {
                'message_id': msg_id_1['message_id'],
                'u_id': u_id,
                'message': 'Hello, this is a test message',
                'time_created': time1,
            }, {
                'message_id': msg_id_2['message_id'],
                'u_id': u_id,
                'message': 'then he said to test',
                'time_created': time2,
            }
        ]
    }
    requests.delete(url + 'clear')

def test_mult_match_messages_but_diff_channels(url) :
    requests.delete(url + 'clear')
    response = requests.post(url + 'auth/register', json = data_in_1)
    payload = response.json()
    token['token'] = payload['token']
    u_id = payload['u_id']
    response = requests.post(url + 'auth/register', json = data_in_2)
    payload = response.json()
    token['token_2'] = payload['token']
    data_in = {
        'token' : token['token'],
        'name' : "Channel1",
        'is_public' : True
    }

    response = requests.post(url + 'channels/create', json = data_in)
    channel_id = response.json()['channel_id']
    data_in = {
        'token' : token['token_2'],
        'name' : "Channel2",
        'is_public' : True
    }
    response = requests.post(url + 'channels/create', json = data_in)
    channel_id_2 = response.json()['channel_id']
    data_in = {
        'token' : token['token'],
        'channel_id' : channel_id_2,
    }
    response = requests.post(url + 'channel/join', json = data_in)
    message_input = {
        'token' : token['token'],
        'channel_id' : channel_id,
        'message' : "Hello Comp1531",
    }
    response = requests.post(url + 'message/send', json = message_input)
    message_input = {
        'token' : token['token'],
        'channel_id' : channel_id_2,
        'message' : "Comp1531 is fun",
    }
    response = requests.post(url + 'message/send', json = message_input)
    msg_id_1 = response.json()['message_id']
    info = {
        'token' : token['token'],
        'channel_id' : channel_id_2,
        'start' : 0,
    }
    response = requests.get(url + 'channel/messages', info)
    messages = response.json()
    messages = messages['messages']
    time = messages[0]['time_created']
    info = {
        'token' : token['token'],
        'query_str' : "World",
    }
    message_input = {
        'token' : token['token'],
        'channel_id' : channel_id,
        'message' : "i do Comp1531",
    }
    response = requests.post(url + 'message/send', json = message_input)

    info = {
        'token' : token['token_2'],
        'query_str' : "1531",
    }
    response = requests.get(url + 'search', info)
    payload = response.json()
    assert payload == {
        'messages': [
            {
                'message_id': msg_id_1,
                'u_id': u_id,
                'message': 'Comp1531 is fun',
                'time_created': time,
            }
        ]
    }
    requests.delete(url + 'clear')

def test_matching_letter(url) :  
    requests.delete(url + 'clear')
    response = requests.post(url + 'auth/register', json = data_in_1)
    payload = response.json()
    token['token'] = payload['token']
    u_id = payload['u_id']
    data_in = {
        'token' : token['token'],
        'name' : "Channel1",
        'is_public' : True
    }

    response = requests.post(url + 'channels/create', json = data_in)
    channel_id = response.json()
    message_input = {
        'token' : token['token'],
        'channel_id' : channel_id['channel_id'],
        'message' : "Hello Comp1531",
    }
    response = requests.post(url + 'message/send', json = message_input)
    msg_id_1 = response.json()['message_id']
    info = {
        'token' : token['token'],
        'channel_id' : channel_id['channel_id'],
        'start' : 0,
    }
    response = requests.get(url + 'channel/messages', info)
    messages = response.json()
    messages = messages['messages']
    time1 = messages[0]['time_created']
    info = {
        'token' : token['token'],
        'query_str' : "World",
    }
    message_input = {
        'token' : token['token'],
        'channel_id' : channel_id['channel_id'],
        'message' : "Hi abcdefg",
    }
    response = requests.post(url + 'message/send', json = message_input)
    message_input = {
        'token' : token['token'],
        'channel_id' : channel_id['channel_id'],
        'message' : "i do Comp1531",
    }
    response = requests.post(url + 'message/send', json = message_input)
    msg_id_2 = response.json()['message_id']
    info = {
        'token' : token['token'],
        'channel_id' : channel_id['channel_id'],
        'start' : 0,
    }
    response = requests.get(url + 'channel/messages', info)
    messages = response.json()
    messages = messages['messages']
    time2 = messages[2]['time_created']
    info = {
        'token' : token['token'],
        'query_str' : "World",
    }
    info = {
        'token' : token['token'],
        'query_str' : "o",
    }
    response = requests.get(url + 'search', info)
    payload = response.json()
    assert payload == {
        'messages': [
            {
                'message_id': msg_id_1,
                'u_id': u_id,
                'message': 'Hello Comp1531',
                'time_created': time1,
            }, {
                'message_id': msg_id_2,
                'u_id': u_id,
                'message': 'i do Comp1531',
                'time_created': time2,
            }
        ]
    }
    requests.delete(url + 'clear')

def test_not_part_of_channel(url) :
    requests.delete(url + 'clear')
    response = requests.post(url + 'auth/register', json = data_in_1)
    payload = response.json()
    token['token'] = payload['token']
    data_in = {
        'token' : token['token'],
        'name' : "Channel1",
        'is_public' : True
    }
    response = requests.post(url + 'channels/create', json = data_in)
    channel_id = response.json()    
    response = requests.post(url + 'auth/register', json = data_in_2)
    payload = response.json()
    token['token_2'] = payload['token']    
    message_input = {
        'token' : token['token'],
        'channel_id' : channel_id['channel_id'],
        'message' : "Hello Comp1531",
    }
    response = requests.post(url + 'message/send', json = message_input)
    message_input = {
        'token' : token['token'],
        'channel_id' : channel_id['channel_id'],
        'message' : "Hi abcdefg",
    }
    response = requests.post(url + 'message/send', json = message_input)
    message_input = {
        'token' : token['token'],
        'channel_id' : channel_id['channel_id'],
        'message' : "i do Comp1531",
    }
    response = requests.post(url + 'message/send', json = message_input)
    info = {
        'token' : token['token_2'],
        'query_str' : "o",
    }
    response = requests.get(url + 'search', info)
    payload = response.json()
    assert payload == {
        'messages': []
    }
    requests.delete(url + 'clear')


def test_invalid_token(url): # wrong user token - accesserror
    requests.delete(url + 'clear')
    response = requests.post(url + 'auth/register', json = data_in_1)
    info = {
        'token' : 100,
        'query_str' : "World",
    }
    response = requests.get(url + 'search', info)
    assert (response.status_code == 400)
    requests.delete(url + 'clear')

