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

def test_add_member_http(url):
    requests.delete(url + 'clear')

    data_in = {
        'email' : "email1@gmail.com",
        'password' : "password",
        'name_first' : "Andreea",
        'name_last' : "Vissarion"
    }
    response = requests.post(url + 'auth/register', json = data_in)
    payload = response.json()
    token_1 = payload['token']
    data_in = {
        'email' : "email2@gmail.com",
        'password' : "password",
        'name_first' : "John",
        'name_last' : "Smith"
    }
    response = requests.post(url + 'auth/register', json = data_in)
    payload = response.json()
    u_id_2 = payload['u_id']

    data_in = {
        'token' : token_1,
        'name' : "Channel1",
        'is_public' : True
    }

    response = requests.post(url + 'channels/create', json = data_in)
    payload = response.json()
    channel_id = payload['channel_id']
    data_in = {
        'token' : token_1,
        'channel_id' : channel_id,
        'u_id' : u_id_2
    }    
    requests.post(url + 'channel/invite', json = data_in)
    data_in = {
        'token' : token_1,
        'channel_id' : channel_id
    }
    response = requests.get(url + 'channel/details', params = data_in)
    assert( response.status_code == 200)
    payload = response.json()
    all_members = payload['all_members']

    is_in = 0
    for member in all_members:
        if member['u_id'] == u_id_2:
            is_in = 1
    assert (is_in == 1)

    requests.delete(url + 'clear')

# Test an invalid channel when none exist
def test_invalid_channel1_http(url):
    requests.delete(url + 'clear')

    data_in = {
        'email' : "email1@gmail.com",
        'password' : "password",
        'name_first' : "Andreea",
        'name_last' : "Vissarion"
    }
    response = requests.post(url + 'auth/register', json = data_in)
    payload = response.json()
    token = payload['token']
    u_id = payload['u_id']
    channel_id = 3
    
    data_in = {
        'token' : token,
        'channel_id' : channel_id,
        'u_id' : u_id
    }    
    response = requests.post(url + 'channel/invite', json = data_in)
    assert (response.status_code == 400)
    requests.delete(url + 'clear')

def test_invalid_channel2_http(url):
    requests.delete(url + 'clear')
    data_in = {
        'email' : "email1@gmail.com",
        'password' : "password",
        'name_first' : "Andreea",
        'name_last' : "Vissarion"
    }
    response = requests.post(url + 'auth/register', json = data_in)
    payload = response.json()
    token = payload['token']
    fake_id = 10

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
        'u_id' : fake_id
    }    
    response = requests.post(url + 'channel/invite', json = data_in)
    assert (response.status_code == 400)    
    requests.delete(url + 'clear')

def test_invalid_user(url):
    requests.delete(url + 'clear')
    data_in = {
        'email' : "email1@gmail.com",
        'password' : "password",
        'name_first' : "Andreea",
        'name_last' : "Vissarion"
    }
    response = requests.post(url + 'auth/register', json = data_in)
    payload = response.json()
    token = payload['token']
    fake_id = 10

    
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
        'u_id' : fake_id
    }    
    response = requests.post(url + 'channel/invite', json = data_in)
    assert (response.status_code == 400)    
    requests.delete(url + 'clear')