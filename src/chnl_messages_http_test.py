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

    response = requests.get(url + 'channel/messages', params=('heyheyhey', channel_id, 1))
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
 
    response = requests.get(url + 'channel/messages', params=(token, 99, 0))
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

    response = requests.get(url + 'channel/messages', params=(99, channel_id, 1)) # 99 is an arbitrary nonexistent token
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

    response = requests.get(url + 'channel/messages', params=(token, channel_id, -10)) # 99 is an arbitrary nonexistent token
    assert(response.status_code == 400)
    requests.delete(url + 'clear')
