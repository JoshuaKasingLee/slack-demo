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

# Successfully create a channel
def test_first_channel_http(url):
    requests.delete(url + 'clear')
    data_in = {
        'email': 'user1@example.com',
        'password': 'password',
        'name_first': 'user1',
        'name_last': 'name',
    }
    response = requests.post(url + 'auth/register', json = data_in)
    payload = response.json()
    token = payload['token']

    data_in = {
        'token': token,
        'name': 'exceptionalll',
        'is_public': True,
    }
    response = requests.post(url + 'channels/create', json = data_in)
    payload = response.json()
    assert(payload == {
        'channel_id': 0,
    })
    requests.delete(url + 'clear')

# Successfully create two channels
def test_second_channel_http(url):
    requests.delete(url + 'clear')
    data_in = {
        'email': 'user1@example.com',
        'password': 'password',
        'name_first': 'user1',
        'name_last': 'name',
    }
    response = requests.post(url + 'auth/register', json = data_in)
    payload = response.json()
    token = payload['token']

    data_in = {
        'token': token,
        'name': 'exceptionalll',
        'is_public': True,
    }
    response = requests.post(url + 'channels/create', json = data_in)

    data_in = {
        'token': token,
        'name': 'exceptionalll_2',
        'is_public': True,
    }
    response = requests.post(url + 'channels/create', json = data_in)
    payload = response.json()
    assert(payload == {
        'channel_id': 1,
    })
    requests.delete(url + 'clear')

# Testing a repeated channel name
def test_repeat_name_http(url):
    requests.delete(url + 'clear')
    data_in = {
        'email': 'user1@example.com',
        'password': 'password',
        'name_first': 'user1',
        'name_last': 'name',
    }
    response = requests.post(url + 'auth/register', json = data_in)
    payload = response.json()
    token = payload['token']

    data_in = {
        'token': token,
        'name': 'duplicate',
        'is_public': True,
    }
    response = requests.post(url + 'channels/create', json = data_in)
    
    data_in = {
        'email': 'user2@example.com',
        'password': 'password',
        'name_first': 'user2',
        'name_last': 'name',
    }
    response = requests.post(url + 'auth/register', json = data_in)
    payload = response.json()
    token = payload['token']

    data_in = {
        'token': token,
        'name': 'duplicate',
        'is_public': True,
    }
    response = requests.post(url + 'channels/create', json = data_in)
    payload = response.json()
    assert(payload == {
        'channel_id': 1,
    })
    requests.delete(url + 'clear')

# Test error given an invalid token
def test_invalid_token_http(url):
    requests.delete(url + 'clear')
    data_in = {
        'token': 'bad token',
        'name': 'channel1',
        'is_public': True,
    }
    response = requests.post(url + 'channels/create', json = data_in)
    assert(response.status_code == 400)
    requests.delete(url + 'clear')

# Test user does not exist
def test_user_missing_http(url):
    requests.delete(url + 'clear')
    data_in = {
        'token': 996,
        'name': 'channel1',
        'is_public': True,
    }
    response = requests.post(url + 'channels/create', json = data_in)
    assert(response.status_code == 400)
    requests.delete(url + 'clear')

# Test error when name is too long
def test_invalid_name_long_http(url):
    requests.delete(url + 'clear')
    data_in = {
        'email': 'user1@example.com',
        'password': 'password',
        'name_first': 'user1',
        'name_last': 'name',
    }
    response = requests.post(url + 'auth/register', json = data_in)
    payload = response.json()
    token = payload['token']
    
    data_in = {
        'token': token,
        'name': 'hahahahahahahahahahaaaa',
        'is_public': True,
    }
    response = requests.post(url + 'channels/create', json = data_in)
    assert(response.status_code == 400)
    requests.delete(url + 'clear')

# Test invalid when a name is of length 0 characters
def test_invalid_name_empty_http(url):
    requests.delete(url + 'clear')
    data_in = {
        'email': 'user1@example.com',
        'password': 'password',
        'name_first': 'user1',
        'name_last': 'name',
    }
    response = requests.post(url + 'auth/register', json = data_in)
    payload = response.json()
    token = payload['token']
    
    data_in = {
        'token': token,
        'name': '',
        'is_public': True,
    }
    response = requests.post(url + 'channels/create', json = data_in)
    assert(response.status_code == 400)
    requests.delete(url + 'clear')
