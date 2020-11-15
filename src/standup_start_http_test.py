import re
import signal
import time
from datetime import datetime, timedelta
from subprocess import PIPE, Popen
from time import sleep
import auth
import channel
import channels
import pytest
import requests
import standup
from error import AccessError, InputError
from other import clear

global_user_1 = {
    'email': "jonathon@gmail.com",
    'password': "password",
    'name_first': "John",
    'name_last': "Smith",
}

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

def test_standup_start_http(url):
    requests.delete(url + 'clear')

    data_in = global_user_1
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
        'length': 2,
    }
    response = requests.post(url + 'standup/start', json = data_in)
    payload = response.json()
    time_finish = payload['time_finish']

    data_in = {
        'token': token,
        'channel_id': channel_id,
    }
    response = requests.get(url + 'standup/active', json = data_in)
    payload = response.json()
    standup_status = payload

    assert (standup_status == {'is_active': True, 'time_finish': time_finish})
    requests.delete(url + 'clear')

def test_invalid_channel_http(url):
    requests.delete(url + 'clear')

    data_in = global_user_1
    response = requests.post(url + 'auth/register', json = data_in)
    payload = response.json()
    token = payload['token']

    data_in = {
        'token': token,
        'channel_id': 999,
        'length': 2,
    }
    response = requests.post(url + 'standup/start', json = data_in)

    assert (response.status_code == 400)
    requests.delete(url + 'clear')

def test_standup_already_exists_http(url):
    requests.delete(url + 'clear')
    
    data_in = global_user_1
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
        'length': 3,
    }
    requests.post(url + 'standup/start', json = data_in)

    data_in = {
        'token': token,
        'channel_id': channel_id,
        'length': 3,
    }
    response = requests.post(url + 'standup/start', json = data_in)

    assert (response.status_code == 400)
    requests.delete(url + 'clear')

def test_standup_ended_http(url):
    clear()
    user = auth.auth_register("jonathon@gmail.com", "password", "John", "Smith")
    token = user['token']
    channel_id = channels.channels_create(token, "Channel1", True)["channel_id"]
    length = 1
    standup.standup_start(token, channel_id, length)
    time.sleep(4)
    standup_status = standup.standup_active(token, channel_id)
    
    assert (standup_status == {'is_active': False, 'time_finish': None})
    clear()

def test_standup_mulitple_http(url):
    requests.delete(url + 'clear')
    
    data_in = global_user_1
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
        'length': 1,
    }
    requests.post(url + 'standup/start', json = data_in)

    time.sleep(4)

    data_in = {
        'token': token,
        'channel_id': channel_id,
    }
    response = requests.get(url + 'standup/active', json = data_in)
    payload = response.json()
    standup_status = payload
    
    assert (standup_status == {'is_active': False, 'time_finish': None})
    requests.delete(url + 'clear')
