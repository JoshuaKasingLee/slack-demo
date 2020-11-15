import pytest
import re
from subprocess import Popen, PIPE
import signal
from time import sleep
import requests

# Use this fixture to get the URL of the server. It starts the server for you,
# so you don't need to.
@pytest.fixture
def url():
    url_re = re.compile(r' \* Running on ([^ ]*)')
    server = Popen(["python3", "src/server.py"], stderr=PIPE, stdout=PIPE)
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

def test_react_one_http(url):
    requests.delete(url + 'clear')
    data_in = {
        'email': "jonathon@gmail.com",
        'password': "password",
        'name_first': "John",
        'name_last': "Smith",
    }
    response = requests.post(url + 'auth/register', json = data_in)
    payload = response.json()
    token = payload['token']
    u_id = payload['u_id']
    data_in = {
        'token': token,
        'name': "Channel1",
        'is_public': True,   
    }
    response = requests.post(url + 'channels/create', json = data_in)
    payload = response.json()
    channel_id = payload['channel_id']

    data_in = {
        'token': token,
        'channel_id': channel_id,
        'message': 'Hello Comp1531',
    }
    response = requests.post(url + 'message/send', json = data_in)
    payload = response.json()
    message_id = payload['message_id']
    
    data_in = {
        'token': token,
        'channel_id': channel_id,
        'start': 0,
    }
    response = requests.get(url + 'channel/messages', params = data_in)
    payload = response.json()
    message_time = payload['messages'][0]['time_created']

    data_in = {
        'token': token,
        'message_id': message_id,
        'react_id': 1,
    }
    response = requests.post(url + 'message/react', json = data_in)

    data_in = {
        'token': token,
        'query_str': 'o',
    }
    response = requests.get(url + 'search', params = data_in)
    payload = response.json()
    assert(payload == {
        'messages': [
            {
                'message_id': message_id,
                'u_id': u_id,
                'message': 'Hello Comp1531',
                'time_created': message_time,
                'reacts': 
                [
                    {
                        'react_id': 1, 'u_ids': [u_id],
                        'is_this_user_reacted': True
                    }
                ],
                'is_pinned': False,
            }
        ]
    })
    requests.delete(url + 'clear')

def test_someone_else_reacted_http_test(url):
    requests.delete(url + 'clear')
    data_in = {
        'email': "jonathon@gmail.com",
        'password': "password",
        'name_first': "John",
        'name_last': "Smith",
    }
    response = requests.post(url + 'auth/register', json = data_in)
    payload = response.json()
    token = payload['token']
    u_id = payload['u_id']
    data_in = {
        'token': token,
        'name': "Channel1",
        'is_public': True,   
    }
    data_in = {
        'email': "alex_jones@gmail.com",
        'password': "password",
        'name_first': "Alex",
        'name_last': "Jones",
    }
    response = requests.post(url + 'auth/register', json = data_in)
    payload = response.json()
    token_2 = payload['token']
    u_id_2 = payload['u_id']
    data_in = {
        'token': token,
        'name': "Channel1",
        'is_public': True,   
    }
    response = requests.post(url + 'channels/create', json = data_in)
    payload = response.json()
    channel_id = payload['channel_id']

    data_in = {
        'token': token_2,
        'channel_id': channel_id,
    }
    response = requests.post(url + 'channel/join', json = data_in)

    data_in = {
        'token': token,
        'channel_id': channel_id,
        'message': 'Hello Comp1531',
    }
    response = requests.post(url + 'message/send', json = data_in)
    payload = response.json()
    message_id = payload['message_id']

    data_in = {
        'token': token_2,
        'channel_id': channel_id,
        'message': 'Helloo',
    }
    response = requests.post(url + 'message/send', json = data_in)
    payload = response.json()
    message_id_2 = payload['message_id']
    
    data_in = {
        'token': token,
        'channel_id': channel_id,
        'start': 0,
    }
    response = requests.get(url + 'channel/messages', params = data_in)
    payload = response.json()
    message_time = payload['messages'][1]['time_created']
    message_time_2 = payload['messages'][0]['time_created']

    data_in = {
        'token': token,
        'message_id': message_id,
        'react_id': 1,
    }
    response = requests.post(url + 'message/react', json = data_in)

    data_in = {
        'token': token_2,
        'message_id': message_id_2,
        'react_id': 1,
    }
    response = requests.post(url + 'message/react', json = data_in)

    data_in = {
        'token': token,
        'query_str': 'o',
    }
    response = requests.get(url + 'search', params = data_in)
    payload = response.json()
    assert(payload == {
        'messages': [
            {
                'message_id': message_id,
                'u_id': u_id,
                'message': 'Hello Comp1531',
                'time_created': message_time,
                'reacts': 
                [
                    {
                        'react_id': 1, 'u_ids': [u_id],
                        'is_this_user_reacted': True
                    }
                ],
                'is_pinned': False,
            }, {
                'message_id': message_id_2,
                'u_id': u_id_2,
                'message': 'Helloo',
                'time_created': message_time_2,
                'reacts': 
                [
                    {
                        'react_id': 1, 'u_ids': [u_id_2],
                        'is_this_user_reacted': False
                    }
                ],
                'is_pinned': False,
            }
        ]
    })
    requests.delete(url + 'clear')

def test_two_reacts_http_test(url):
    requests.delete(url + 'clear')
    data_in = {
        'email': "jonathon@gmail.com",
        'password': "password",
        'name_first': "John",
        'name_last': "Smith",
    }
    response = requests.post(url + 'auth/register', json = data_in)
    payload = response.json()
    token = payload['token']
    u_id = payload['u_id']
    data_in = {
        'token': token,
        'name': "Channel1",
        'is_public': True,   
    }
    data_in = {
        'email': "alex_jones@gmail.com",
        'password': "password",
        'name_first': "Alex",
        'name_last': "Jones",
    }
    response = requests.post(url + 'auth/register', json = data_in)
    payload = response.json()
    token_2 = payload['token']
    u_id_2 = payload['u_id']
    data_in = {
        'token': token,
        'name': "Channel1",
        'is_public': True,   
    }
    response = requests.post(url + 'channels/create', json = data_in)
    payload = response.json()
    channel_id = payload['channel_id']

    data_in = {
        'token': token_2,
        'channel_id': channel_id,
    }
    response = requests.post(url + 'channel/join', json = data_in)

    data_in = {
        'token': token,
        'channel_id': channel_id,
        'message': 'Hello Comp1531',
    }
    response = requests.post(url + 'message/send', json = data_in)
    payload = response.json()
    message_id = payload['message_id']

    data_in = {
        'token': token_2,
        'channel_id': channel_id,
        'message': 'Helloo',
    }
    response = requests.post(url + 'message/send', json = data_in)
    payload = response.json()
    message_id_2 = payload['message_id']
    
    data_in = {
        'token': token,
        'channel_id': channel_id,
        'start': 0,
    }
    response = requests.get(url + 'channel/messages', params = data_in)
    payload = response.json()
    message_time = payload['messages'][1]['time_created']
    message_time_2 = payload['messages'][0]['time_created']

    data_in = {
        'token': token,
        'message_id': message_id_2,
        'react_id': 1,
    }
    response = requests.post(url + 'message/react', json = data_in)

    data_in = {
        'token': token_2,
        'message_id': message_id_2,
        'react_id': 1,
    }
    response = requests.post(url + 'message/react', json = data_in)

    data_in = {
        'token': token,
        'query_str': 'o',
    }
    response = requests.get(url + 'search', params = data_in)
    payload = response.json()
    assert(payload == {
        'messages': [
            {
                'message_id': message_id,
                'u_id': u_id,
                'message': 'Hello Comp1531',
                'time_created': message_time,
                'reacts': 
                [
                    {
                        'react_id': 1, 'u_ids': [],
                        'is_this_user_reacted': False
                    }
                ],
                'is_pinned': False,
            }, {
                'message_id': message_id_2,
                'u_id': u_id_2,
                'message': 'Helloo',
                'time_created': message_time_2,
                'reacts': 
                [
                    {
                        'react_id': 1, 'u_ids': [u_id, u_id_2],
                        'is_this_user_reacted': True
                    }
                ],
                'is_pinned': False,
            }
        ]
    })
    requests.delete(url + 'clear')

def test_wrong_channel_http_test(url):
    requests.delete(url + 'clear')
    data_in = {
        'email': "jonathon@gmail.com",
        'password': "password",
        'name_first': "John",
        'name_last': "Smith",
    }
    response = requests.post(url + 'auth/register', json = data_in)
    payload = response.json()
    token = payload['token']
    data_in = {
        'email': "alex_jones@gmail.com",
        'password': "password",
        'name_first': "Alex",
        'name_last': "Jones",
    }
    response = requests.post(url + 'auth/register', json = data_in)
    payload = response.json()
    token_2 = payload['token']
    data_in = {
        'token': token,
        'name': "Channel1",
        'is_public': True,   
    }
    response = requests.post(url + 'channels/create', json = data_in)
    payload = response.json()
    channel_id = payload['channel_id']
    data_in = {
        'token': token,
        'channel_id': channel_id,
        'message': 'Hello Comp1531',
    }
    response = requests.post(url + 'message/send', json = data_in)
    payload = response.json()
    message_id = payload['message_id']

    data_in = {
        'token': token_2,
        'message_id': message_id,
        'react_id': 1,
    }
    response = requests.post(url + 'message/react', json = data_in)
    assert(response.status_code == 400)
    requests.delete(url + 'clear')

def test_message_already_reacted_http_test(url):
    requests.delete(url + 'clear')
    data_in = {
        'email': "jonathon@gmail.com",
        'password': "password",
        'name_first': "John",
        'name_last': "Smith",
    }
    response = requests.post(url + 'auth/register', json = data_in)
    payload = response.json()
    token = payload['token']
    data_in = {
        'token': token,
        'name': "Channel1",
        'is_public': True,   
    }
    response = requests.post(url + 'channels/create', json = data_in)
    payload = response.json()
    channel_id = payload['channel_id']
    data_in = {
        'token': token,
        'channel_id': channel_id,
        'message': 'Hello Comp1531',
    }
    response = requests.post(url + 'message/send', json = data_in)
    payload = response.json()
    message_id = payload['message_id']
    data_in = {
        'token': token,
        'message_id': message_id,
        'react_id': 1,
    }
    response = requests.post(url + 'message/react', json = data_in)
    response = requests.post(url + 'message/react', json = data_in)
    assert(response.status_code == 400)
    requests.delete(url + 'clear')

def test_message_id_invalid_http_test(url):
    requests.delete(url + 'clear')
    data_in = {
        'email': "jonathon@gmail.com",
        'password': "password",
        'name_first': "John",
        'name_last': "Smith",
    }
    response = requests.post(url + 'auth/register', json = data_in)
    payload = response.json()
    token = payload['token']
    data_in = {
        'token': token,
        'name': "Channel1",
        'is_public': True,   
    }
    response = requests.post(url + 'channels/create', json = data_in)
    payload = response.json()
    channel_id = payload['channel_id']
    data_in = {
        'token': token,
        'channel_id': channel_id,
        'message': 'Hello Comp1531',
    }
    response = requests.post(url + 'message/send', json = data_in)
    payload = response.json()
    data_in = {
        'token': token,
        'message_id': 3,
        'react_id': 1,
    }
    response = requests.post(url + 'message/react', json = data_in)
    assert(response.status_code == 400)
    requests.delete(url + 'clear')

def test_invalid_token_http_test(url):
    requests.delete(url + 'clear')
    data_in = {
        'email': "jonathon@gmail.com",
        'password': "password",
        'name_first': "John",
        'name_last': "Smith",
    }
    response = requests.post(url + 'auth/register', json = data_in)
    payload = response.json()
    token = payload['token']
    data_in = {
        'token': token,
        'name': "Channel1",
        'is_public': True,   
    }
    response = requests.post(url + 'channels/create', json = data_in)
    payload = response.json()
    channel_id = payload['channel_id']
    data_in = {
        'token': token,
        'channel_id': channel_id,
        'message': 'Hello Comp1531',
    }
    response = requests.post(url + 'message/send', json = data_in)
    payload = response.json()
    message_id = payload['message_id']
    data_in = {
        'token': 4,
        'message_id': message_id,
        'react_id': 1,
    }
    response = requests.post(url + 'message/react', json = data_in)
    assert(response.status_code == 400)
    requests.delete(url + 'clear')

def test_invalid_react_id_http_test(url):
    requests.delete(url + 'clear')
    data_in = {
        'email': "jonathon@gmail.com",
        'password': "password",
        'name_first': "John",
        'name_last': "Smith",
    }
    response = requests.post(url + 'auth/register', json = data_in)
    payload = response.json()
    token = payload['token']
    data_in = {
        'token': token,
        'name': "Channel1",
        'is_public': True,   
    }
    response = requests.post(url + 'channels/create', json = data_in)
    payload = response.json()
    channel_id = payload['channel_id']
    data_in = {
        'token': token,
        'channel_id': channel_id,
        'message': 'Hello Comp1531',
    }
    response = requests.post(url + 'message/send', json = data_in)
    payload = response.json()
    message_id = payload['message_id']
    data_in = {
        'token': token,
        'message_id': message_id,
        'react_id': 3,
    }
    response = requests.post(url + 'message/react', json = data_in)
    assert(response.status_code == 400)
    requests.delete(url + 'clear')