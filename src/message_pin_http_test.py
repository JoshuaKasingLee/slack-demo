import json
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

def test_pinning_one(url):
    requests.delete(url + 'clear')
    data_in = {
        'email': "user@gmail.com",
        'password': "password",
        'name_first': "John",
        'name_last': "Smith",
    }
    response = requests.post(url + 'auth/register', json = data_in)
    payload = response.json()
    token = payload['token']
    
    data_in = {
        'token': token,
        'name': "Test channel",
        'is_public': True,   
    }
    
    response = requests.post(url + 'channels/create', json = data_in)
    payload = response.json()
    channel_id = payload['channel_id']

    data_in = {
        'token': token,
        'channel_id': channel_id,
        'message': 'Hi!',
    }

    response = requests.post(url + 'message/send', json = data_in)
    payload = response.json()
    message_id = payload['message_id']
    data_in = {
        'token': token,
        'message_id': message_id,
    }
    response = requests.post(url + 'message/pin', json = data_in)
    payload = response.json()
    assert payload == {}
    requests.delete(url + 'clear')

def test_pinning_one_but_two_messages(url):
    requests.delete(url + 'clear')
    data_in = {
        'email': "user@gmail.com",
        'password': "password",
        'name_first': "John",
        'name_last': "Smith",
    }
    response = requests.post(url + 'auth/register', json = data_in)
    payload = response.json()
    token = payload['token']
    
    data_in = {
        'token': token,
        'name': "Test channel",
        'is_public': True,   
    }
    
    response = requests.post(url + 'channels/create', json = data_in)
    payload = response.json()
    channel_id = payload['channel_id']

    data_in = {
        'token': token,
        'channel_id': channel_id,
        'message': 'Hi!',
    }

    response = requests.post(url + 'message/send', json = data_in)
    payload = response.json()
    
    data_in = {
        'token': token,
        'channel_id': channel_id,
        'message': 'Hello!',
    }
    response = requests.post(url + 'message/send', json = data_in)
    payload = response.json()
    message_id_2 = payload['message_id']
    data_in = {
        'token': token,
        'message_id': message_id_2,
    }
    response = requests.post(url + 'message/pin', json = data_in)
    payload = response.json()
    assert payload == {}
    requests.delete(url + 'clear')

def test_pinning_two(url):
    requests.delete(url + 'clear')
    data_in = {
        'email': "user@gmail.com",
        'password': "password",
        'name_first': "John",
        'name_last': "Smith",
    }
    response = requests.post(url + 'auth/register', json = data_in)
    payload = response.json()
    token = payload['token']
    
    data_in = {
        'token': token,
        'name': "Test channel",
        'is_public': True,   
    }
    
    response = requests.post(url + 'channels/create', json = data_in)
    payload = response.json()
    channel_id = payload['channel_id']

    data_in = {
        'token': token,
        'channel_id': channel_id,
        'message': 'Hi!',
    }

    response = requests.post(url + 'message/send', json = data_in)
    payload = response.json()
    message_id = payload['message_id']
    data_in = {
        'token': token,
        'channel_id': channel_id,
        'message': 'Hello!',
    }
    response = requests.post(url + 'message/send', json = data_in)
    payload = response.json()
    message_id_2 = payload['message_id']
    
    data_in = {
        'token': token,
        'message_id': message_id,
    }
    response = requests.post(url + 'message/pin', json = data_in)
    payload = response.json()
    assert payload == {}
    
    data_in = {
        'token': token,
        'message_id': message_id_2,
    }
    response = requests.post(url + 'message/pin', json = data_in)
    payload = response.json()
    assert payload == {}
    requests.delete(url + 'clear')

def test_not_owner(url):
    requests.delete(url + 'clear')
    data_in = {
        'email': "user@gmail.com",
        'password': "password",
        'name_first': "John",
        'name_last': "Smith",
    }
    response = requests.post(url + 'auth/register', json = data_in)
    payload = response.json()
    token = payload['token']
    
    data_in = {
        'token': token,
        'name': "Test channel",
        'is_public': True,   
    }
    
    response = requests.post(url + 'channels/create', json = data_in)
    payload = response.json()
    channel_id = payload['channel_id']

    data_in = {
        'token': token,
        'channel_id': channel_id,
        'message': 'Hi!',
    }

    response = requests.post(url + 'message/send', json = data_in)
    payload = response.json()
    message_id = payload['message_id']

    data_in = {
        'email': "user2@gmail.com",
        'password': "password",
        'name_first': "Sam",
        'name_last': "Smith",
    }
    response = requests.post(url + 'auth/register', json = data_in)
    payload = response.json()
    token_2 = payload['token']
  
    data_in = {
        'token' : token_2,
        'channel_id' : channel_id
    }

    requests.post(url + 'channel/join', json = data_in)
    
    data_in = {
        'token': token_2,
        'message_id': message_id,
    }
    
    response = requests.post(url + 'message/pin', json = data_in)
    assert (response.status_code == 400)
    requests.delete(url + 'clear')

def test_wrong_channel(url):
    requests.delete(url + 'clear')
    data_in = {
        'email': "user@gmail.com",
        'password': "password",
        'name_first': "John",
        'name_last': "Smith",
    }
    response = requests.post(url + 'auth/register', json = data_in)
    payload = response.json()
    token = payload['token']
    
    data_in = {
        'token': token,
        'name': "Test channel",
        'is_public': True,   
    }
    
    response = requests.post(url + 'channels/create', json = data_in)
    payload = response.json()
    channel_id = payload['channel_id']

    data_in = {
        'token': token,
        'channel_id': channel_id,
        'message': 'Hi!',
    }

    response = requests.post(url + 'message/send', json = data_in)
    payload = response.json()
    message_id = payload['message_id']

    data_in = {
        'email': "user2@gmail.com",
        'password': "password",
        'name_first': "Sam",
        'name_last': "Smith",
    }
    response = requests.post(url + 'auth/register', json = data_in)
    payload = response.json()
    token_2 = payload['token']
    
    data_in = {
        'token': token_2,
        'message_id': message_id,
    }
    
    response = requests.post(url + 'message/pin', json = data_in)
    assert (response.status_code == 400)
    requests.delete(url + 'clear')

def test_already_pinned(url):
    requests.delete(url + 'clear')
    data_in = {
        'email': "user@gmail.com",
        'password': "password",
        'name_first': "John",
        'name_last': "Smith",
    }
    response = requests.post(url + 'auth/register', json = data_in)
    payload = response.json()
    token = payload['token']
    
    data_in = {
        'token': token,
        'name': "Test channel",
        'is_public': True,   
    }
    
    response = requests.post(url + 'channels/create', json = data_in)
    payload = response.json()
    channel_id = payload['channel_id']

    data_in = {
        'token': token,
        'channel_id': channel_id,
        'message': 'Hi!',
    }

    response = requests.post(url + 'message/send', json = data_in)
    payload = response.json()
    message_id = payload['message_id']
    data_in = {
        'token': token,
        'message_id': message_id,
    }
    response = requests.post(url + 'message/pin', json = data_in)
    payload = response.json()
    data_in = {
        'token': token,
        'message_id': message_id,
    }
    response = requests.post(url + 'message/pin', json = data_in)
    payload = response.json()
    assert (response.status_code == 400)
    requests.delete(url + 'clear')

def test_message_id_invalid(url):
    requests.delete(url + 'clear')
    data_in = {
        'email': "user@gmail.com",
        'password': "password",
        'name_first': "John",
        'name_last': "Smith",
    }
    response = requests.post(url + 'auth/register', json = data_in)
    payload = response.json()
    token = payload['token']
    
    data_in = {
        'token': token,
        'name': "Test channel",
        'is_public': True,   
    }
    
    response = requests.post(url + 'channels/create', json = data_in)
    payload = response.json()
    channel_id = payload['channel_id']

    data_in = {
        'token': token,
        'channel_id': channel_id,
        'message': 'Hi!',
    }

    response = requests.post(url + 'message/send', json = data_in)
    payload = response.json()
    data_in = {
        'token': token,
        'message_id': 3,
    }
    response = requests.post(url + 'message/pin', json = data_in)
    assert (response.status_code == 400)
    requests.delete(url + 'clear')
    
def test_invalid_token(url):
    requests.delete(url + 'clear')
    data_in = {
        'email': "user@gmail.com",
        'password': "password",
        'name_first': "John",
        'name_last': "Smith",
    }
    response = requests.post(url + 'auth/register', json = data_in)
    payload = response.json()
    token = payload['token']
    
    data_in = {
        'token': token,
        'name': "Test channel",
        'is_public': True,   
    }
    
    response = requests.post(url + 'channels/create', json = data_in)
    payload = response.json()
    channel_id = payload['channel_id']

    data_in = {
        'token': token,
        'channel_id': channel_id,
        'message': 'Hi!',
    }

    response = requests.post(url + 'message/send', json = data_in)
    payload = response.json()
    message_id = payload['message_id']
    data_in = {
        'token': 4,
        'message_id': message_id,
    }
    response = requests.post(url + 'message/pin', json = data_in)
    assert (response.status_code == 400)
    requests.delete(url + 'clear')
    
    
    
    
    
    
    
    
    
    
    