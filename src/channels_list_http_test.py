import pytest
import re
from subprocess import Popen, PIPE
import signal
from time import sleep
import requests
import json

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

# Testing a successful list
def test_success_http(url):
    requests.delete(url + 'clear')
    data_in = {
        'email': 'email@example.com',
        'password': 'password',
        'name_first': 'Andreea',
        'name_last': 'Viss',
    }
    response = requests.post(url + 'auth/register', json = data_in)
    payload = response.json()
    token = payload['token']

    data_in = {
        'token': token,
        'name': 'Channel1',
        'is_public': True,
    }
    response = requests.post(url + 'channels/create', json = data_in)
    payload = response.json()
    channel_id = payload['channel_id']
    
    data_in = {
        'token': token,
    }

    response = requests.get(url + 'channels/list', params = data_in)
    payload = response.json()
    assert(payload == {
        'channels': [
            {
                'channel_id': channel_id,
                'name': 'Channel1',
            }
        ]
    })
    requests.delete(url + 'clear')

# Test multiple channels under a user
def test_several_success_http(url):
    requests.delete(url + 'clear')
    data_in = {
        'email': 'email@example.com',
        'password': 'password',
        'name_first': 'Andreea',
        'name_last': 'Viss',
    }
    response = requests.post(url + 'auth/register', json = data_in)
    payload = response.json()
    token = payload['token']
    
    data_in = {
        'token': token,
        'name': 'Channel1',
        'is_public': True,
    }
    response = requests.post(url + 'channels/create', json = data_in)
    payload = response.json()
    channel_id = payload['channel_id']

    data_in = {
        'token': token,
        'name': 'Channel2',
        'is_public': False,
    }
    response = requests.post(url + 'channels/create', json = data_in)
    payload = response.json()
    channel_id2 = payload['channel_id']

    data_in = {
        'token': token,
    }

    response = requests.get(url + 'channels/list', params = data_in)
    payload = response.json()
    assert(payload == {
        'channels': [
            {
                'channel_id': channel_id,
                'name': 'Channel1'
            },
            {
                'channel_id': channel_id2,
                'name': 'Channel2'
            }
        ]
    })
    requests.delete(url + 'clear')

# Test channels allocated to separate owners
def test_two_not_owner_http(url):
    requests.delete(url + 'clear')
    data_in = {
        'email': 'email@example.com',
        'password': 'password',
        'name_first': 'Andreea',
        'name_last': 'Viss',
    }
    response = requests.post(url + 'auth/register', json = data_in)
    payload = response.json()
    token = payload['token']
    
    data_in = {
        'token': token,
        'name': 'Channel1',
        'is_public': True,
    }
    response = requests.post(url + 'channels/create', json = data_in)
    payload = response.json()
    channel_id = payload['channel_id']

    data_in = {
        'email': 'email2@example.com',
        'password': 'password',
        'name_first': 'Andreea2',
        'name_last': 'Viss2',
    }
    response = requests.post(url + 'auth/register', json = data_in)
    payload = response.json()
    token2 = payload['token']

    data_in = {
        'token': token2,
        'name': 'Channel2',
        'is_public': False,
    }
    response = requests.post(url + 'channels/create', json = data_in)
    payload = response.json()
    channel_id2 = payload['channel_id']

    data_in = {
        'token': token,
    }

    response = requests.get(url + 'channels/list', params = data_in)
    payload = response.json()
    assert(payload == {
        'channels': [
            {
                'channel_id': channel_id,
                'name': 'Channel1'
            }
        ]
    })
    requests.delete(url + 'clear')

# Test owner once member joins channel
def test_two_member_http(url):
    requests.delete(url + 'clear')
    data_in = {
        'email': 'email@example.com',
        'password': 'password',
        'name_first': 'Andreea',
        'name_last': 'Viss',
    }
    response = requests.post(url + 'auth/register', json = data_in)
    payload = response.json()
    token = payload['token']
    
    data_in = {
        'token': token,
        'name': 'Channel1',
        'is_public': True,
    }
    response = requests.post(url + 'channels/create', json = data_in)
    payload = response.json()
    channel_id = payload['channel_id']

    data_in = {
        'email': 'email2@example.com',
        'password': 'password',
        'name_first': 'Andreea2',
        'name_last': 'Viss2',
    }
    response = requests.post(url + 'auth/register', json = data_in)
    payload = response.json()
    token2 = payload['token']

    data_in = {
        'token': token2,
        'name': 'Channel2',
        'is_public': False,
    }
    response = requests.post(url + 'channels/create', json = data_in)
    payload = response.json()
    channel_id2 = payload['channel_id']

    data_in = {
        'token': token,
        'channel_id': channel_id2,
    }

    response = requests.post(url + 'channel/join', json = data_in)

    data_in = {
        'token': token,
    }

    response = requests.get(url + 'channels/list', params = data_in)
    payload = response.json()
    assert(payload == {
        'channels': [
            {
                'channel_id': channel_id,
                'name': 'Channel1'
            },
            {
                'channel_id': channel_id2,
                'name': 'Channel2'
            }
        ]
    })
    requests.delete(url + 'clear')

# Test empty channel list
def test_empty_http(url):
    requests.delete(url + 'clear')
    data_in = {
        'email': 'email@example.com',
        'password': 'password',
        'name_first': 'Andreea',
        'name_last': 'Viss',
    }
    response = requests.post(url + 'auth/register', json = data_in)
    payload = response.json()
    token = payload['token']

    data_in = {
        'token': token,
    }

    response = requests.get(url + 'channels/list', params = data_in)
    payload = response.json()
    assert(payload == {'channels': []})
    requests.delete(url + 'clear')

# Test error with invalid token
def test_error_invalid_token_http(url):
    requests.delete(url + 'clear')
    data_in = {
        'token': 'blahblah',
    }

    response = requests.get(url + 'channels/list', params = data_in)
    assert(response.status_code == 400)
    requests.delete(url + 'clear')

# Test an invalid user
def test_invalid_user_http(url):
    requests.delete(url + 'clear')
    data_in = {
        'email': 'email@example.com',
        'password': 'password',
        'name_first': 'Andreea',
        'name_last': 'Viss',
    }
    response = requests.post(url + 'auth/register', json = data_in)
    payload = response.json()
    token = payload['token'] + "1"

    data_in = {
        'token': token,
    }

    response = requests.get(url + 'channels/list', params = data_in)
    assert(response.status_code == 400)
    requests.delete(url + 'clear')