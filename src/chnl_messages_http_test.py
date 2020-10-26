import pytest
import re
from subprocess import Popen, PIPE
import signal
from time import sleep
import requests
import json

data_in_1 = {
        'email' : "jonathon@gmail.com",
        'password' : "password",
        'name_first' : "John",
        'name_last' : "Smith"
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

def test_invalid_token_http(url): # invalid token - AccessError
    requests.delete(url + 'clear')
    data_in = {
        'email' : "email2@gmail.com",
        'password' : "password",
        'name_first' : "John",
        'name_last' : "Smith"
    }
    response = requests.post(url + 'auth/register', json = data_in)
    payload = response.json()
    token = payload['token']

    data_in = {
        'token' : token,
        'name' : "Channel1",
        'is_public' : True
    }

    response = requests.post(url + 'channels/create', json = data_in)
    payload = response.json()
    channel_id = payload['channel_id']

    data_in = {
        'token' : 'heyheyhey',
        'channel_id' : channel_id,
        'start' : 1
    }

    response = requests.get(url + 'channel/messages', params = data_in)
    assert(response.status_code == 400)
    requests.delete(url + 'clear')

def test_missing_channel_http(url): # invalid channel_id - InputError (bc of channel_details spec)
    requests.delete(url + 'clear')
    data_in = {
        'email' : "email2@gmail.com",
        'password' : "password",
        'name_first' : "John",
        'name_last' : "Smith"
    }
    response = requests.post(url + 'auth/register', json = data_in)
    payload = response.json()
    token = payload['token']
 
    data_in = {
        'token' : token,
        'channel_id' : 99,
        'start' : 0
    }
    response = requests.get(url + 'channel/messages', params = data_in)
    assert(response.status_code == 400)
    requests.delete(url + 'clear')

def test_missing_user_http(url): # user doesn't exist - AccessError
    requests.delete(url + 'clear')
    data_in = {
        'email' : "email2@gmail.com",
        'password' : "password",
        'name_first' : "John",
        'name_last' : "Smith"
    }
    response = requests.post(url + 'auth/register', json = data_in)
    payload = response.json()
    token = payload['token']

    data_in = {
        'token' : token,
        'name' : "Channel1",
        'is_public' : True
    }

    response = requests.post(url + 'channels/create', json = data_in)
    payload = response.json()
    channel_id = payload['channel_id']

    data_in = {
        'token' : 99,
        'channel_id' : channel_id,
        'start' : 1
    }

    response = requests.get(url + 'channel/messages', params = data_in) # 99 is an arbitrary nonexistent token
    assert(response.status_code == 400)
    requests.delete(url + 'clear')

def test_negative_index(url): # invalid index - InputError
    requests.delete(url + 'clear')
    data_in = {
        'email' : "email2@gmail.com",
        'password' : "password",
        'name_first' : "John",
        'name_last' : "Smith"
    }
    response = requests.post(url + 'auth/register', json = data_in)
    payload = response.json()
    token = payload['token']

    data_in = {
        'token' : token,
        'name' : "Channel1",
        'is_public' : True
    }

    response = requests.post(url + 'channels/create', json = data_in)
    payload = response.json()
    channel_id = payload['channel_id']

    data_in = {
        'token' : token,
        'channel_id' : channel_id,
        'message' : "yes awesome i like it"
        
    }

    requests.post(url + 'message/send', json = data_in)

    data_in = {
        'token' : token,
        'channel_id' : channel_id,
        'start' : -10
    }

    response = requests.get(url + 'channel/messages', params = data_in) # 99 is an arbitrary nonexistent token
    assert(response.status_code == 400)
    requests.delete(url + 'clear')

def test_message_chronology(url):
    requests.delete(url + 'clear')
    response = requests.post(url + 'auth/register', json = data_in_1)
    payload = response.json()
    token = payload['token']
    u_id = payload['u_id']
    data_in = {
        'token' : token,
        'name' : "Channel1",
        'is_public' : True
    }
    response = requests.post(url + 'channels/create', json = data_in)
    channel_id = response.json()

    message_input = {
        'token' : token,
        'channel_id' : channel_id['channel_id'],
        'message' : "first",
    }
    response = requests.post(url + 'message/send', json = message_input)
    payload = response.json()

    message_input = {
        'token' : token,
        'channel_id' : channel_id['channel_id'],
        'message' : "sec0nd",
    }
    response = requests.post(url + 'message/send', json = message_input)
    payload = response.json()

    info = {
        'token' : token,
        'channel_id' : channel_id['channel_id'],
        'start' : 0,
    }
    response = requests.get(url + 'channel/messages', info)
    messages = response.json()
    messages = messages['messages']
    time1 = messages[0]['time_created']
    time2 = messages[1]['time_created']
    assert (time1 > time2)
    requests.delete(url + 'clear')

def test_pagination(url):
    requests.delete(url + 'clear')
    response = requests.post(url + 'auth/register', json = data_in_1)
    payload = response.json()
    token = payload['token']
    data_in = {
        'token' : token,
        'name' : "Channel1",
        'is_public' : True
    }
    response = requests.post(url + 'channels/create', json = data_in)
    channel_id = response.json()
    i = 0
    while i < 55:
        message_to_send = "message " + str(i)
        data_in = {
            'token' : token,
            'channel_id' : channel_id['channel_id'],
            'message' : message_to_send,
        }
        requests.post(url + 'message/send', json = data_in)
        i += 1
    data_in = {
        'token' : token,
        'channel_id' : channel_id['channel_id'],
        'start' : 1,
    }
    response = requests.get(url + 'channel/messages', data_in)
    end = response.json()['end']
    assert (end == 51)
    requests.delete(url + 'clear')