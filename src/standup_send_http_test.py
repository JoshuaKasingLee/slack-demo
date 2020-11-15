import re
import signal
import time
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
global_user_2 = {
    'email': "jofnathon@gmail.com",
    'password': "password",
    'name_first': "Nhoj",
    'name_last': "Htims",
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

def test_standup_send_single_http(url):
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

    data_in = {
        'token': token,
        'channel_id': channel_id,
        'message': 'i am john',
    }
    requests.post(url + 'standup/send', json = data_in)
    
    time.sleep(1)

    data_in = {
        'token' : token,
        'channel_id' : channel_id,
        'start' : 0,
    }
    response = requests.get(url + 'channel/messages', data_in)
    payload = response.json()

    assert (payload['messages'][0]['message'] == 'John: i am john')
    requests.delete(url + 'clear')

def test_standup_send_multiple_http(url):
    requests.delete(url + 'clear')

    data_in = global_user_1
    response = requests.post(url + 'auth/register', json = data_in)
    payload = response.json()
    token = payload['token']

    data_in = global_user_2
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
        'token': token_2,
        'channel_id': channel_id,
    }
    requests.post(url + 'channel/join', json = data_in)

    data_in = {
        'token': token,
        'channel_id': channel_id,
        'length': 1,
    }
    requests.post(url + 'standup/start', json = data_in)

    data_in = {
        'token': token,
        'channel_id': channel_id,
        'message': 'i am john',
    }
    requests.post(url + 'standup/send', json = data_in)

    data_in = {
        'token': token_2,
        'channel_id': channel_id,
        'message': 'i am johns evil twin',
    }
    requests.post(url + 'standup/send', json = data_in)

    time.sleep(1)

    data_in = {
        'token' : token,
        'channel_id' : channel_id,
        'start' : 0,
    }
    response = requests.get(url + 'channel/messages', data_in)
    payload = response.json()

    assert (payload['messages'][0]['message'] == 'John: i am john\nNhoj: i am johns evil twin')
    requests.delete(url + 'clear')

def test_standup_send_empty_http(url):
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

    data_in = {
        'token': token,
        'channel_id': channel_id,
        'message': '',
    }
    requests.post(url + 'standup/send', json = data_in)
    
    time.sleep(1)

    data_in = {
        'token' : token,
        'channel_id' : channel_id,
        'start' : 0,
    }
    response = requests.get(url + 'channel/messages', data_in)
    payload = response.json()

    assert (payload['messages'][0]['message'] == 'John: ')
    requests.delete(url + 'clear')

def test_standup_send_multiple_alone_http(url):
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

    data_in = {
        'token': token,
        'channel_id': channel_id,
        'message': 'i am john',
    }
    requests.post(url + 'standup/send', json = data_in)
    data_in = {
        'token': token,
        'channel_id': channel_id,
        'message': 'i am johns evil twin, jk',
    }
    requests.post(url + 'standup/send', json = data_in)
    
    time.sleep(1)

    data_in = {
        'token' : token,
        'channel_id' : channel_id,
        'start' : 0,
    }
    response = requests.get(url + 'channel/messages', data_in)
    payload = response.json()

    assert (payload['messages'][0]['message'] == 'John: i am john\nJohn: i am johns evil twin, jk')
    requests.delete(url + 'clear')

def test_standup_send_inactive_http(url):
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
        'message': 'hey',
    }
    response = requests.post(url + 'standup/send', json = data_in)

    assert (response.status_code == 400)
    requests.delete(url + 'clear')

def test_standup_send_long_http(url):
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

    string = 'lmao'
    for i in range(100):
        string += '0123456789'

    data_in = {
        'token': token,
        'channel_id': channel_id,
        'message': string,
    }
    response = requests.post(url + 'standup/send', json = data_in)

    assert (response.status_code == 400)
    requests.delete(url + 'clear')

def test_standup_send_channel_http(url):
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

    data_in = {
        'token': token,
        'channel_id': 99,
        'message': 'hey',
    }
    response = requests.post(url + 'standup/send', json = data_in)

    assert (response.status_code == 400)
    requests.delete(url + 'clear')

def test_standup_send_unauthorized_http(url):
    requests.delete(url + 'clear')

    data_in = global_user_1
    response = requests.post(url + 'auth/register', json = data_in)
    payload = response.json()
    token = payload['token']

    data_in = global_user_2
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
        'length': 1,
    }
    requests.post(url + 'standup/start', json = data_in)

    data_in = {
        'token': token_2,
        'channel_id': channel_id,
        'message': 'hey',
    }
    response = requests.post(url + 'standup/send', json = data_in)

    assert (response.status_code == 400)
    requests.delete(url + 'clear')

def test_standup_send_token_http(url):
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

    data_in = {
        'token': 'bad_token',
        'channel_id': channel_id,
        'message': 'hey',
    }
    response = requests.post(url + 'standup/send', json = data_in)

    assert (response.status_code == 400)
    requests.delete(url + 'clear')
