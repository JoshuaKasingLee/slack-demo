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

# Test that an Access Error is raised when user is not a channel owner
def test_user_not_owner_http(url):
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
    token = payload['token']
    
    data_in = {
        'token': token,
        'message_id': message_id,
        'message': 'New Message!',
    }
    
    response = requests.put(url + 'message/edit', json = data_in)
    assert (response.status_code == 400)
    requests.delete(url + 'clear')

# Test that an Input Error is raised when the message does not exist
def test_message_never_existed_http(url):
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

    data_in = {
        'token': token,
        'message_id': 15,
        'message': 'Edited Message!',
    }

    response = requests.put(url + 'message/edit', json = data_in)
    assert (response.status_code == 400)
    requests.delete(url + 'clear')

# Test that an Input Error is raised when the message was deleted
def test_message_already_deleted_http(url):
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

    response = requests.delete(url + 'message/remove', json = data_in)

    data_in = {
        'token': token,
        'message_id': message_id,
        'message': 'Edited Message!',
    }

    response = requests.put(url + 'message/edit', json = data_in)
    assert(response.status_code == 400)
    requests.delete(url + 'clear')
