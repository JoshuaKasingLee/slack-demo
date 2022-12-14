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


#TESTING OF CHANNEL FUNCTIONS

def test_owner_http(url):
    requests.delete(url + 'clear')

    data_in = {
        'email' : "test1@gmail.com",
        'password' : "password",
        'name_first' : "John",
        'name_last' : "Smith"
    }

    response = requests.post(url + 'auth/register', json = data_in)
    payload = response.json()
    u_id = payload['u_id']
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
        'channel_id' : channel_id
    }
    response = requests.get(url + 'channel/details', params = data_in)
    payload = response.json()
    assert(payload == {
        'name': 'Channel1',
        'owner_members': [
         {
            'u_id': u_id, 
            'name_first': 'John',
            'name_last': 'Smith',
            'profile_img_url': None
        }],
        'all_members': [
            {
                'u_id': u_id, 
                'name_first': 'John',
                'name_last': 'Smith',
                'profile_img_url': None
            }
        ],
    })
    requests.delete(url + 'clear')

def test_one_owner_two_members_http(url):
    requests.delete(url + 'clear')

    data_in = {
        'email' : "email1@gmail.com",
        'password' : "password",
        'name_first' : "Andreea",
        'name_last' : "Vissarion"
    }

    response = requests.post(url + 'auth/register', json = data_in)
    payload = response.json()
    u_id_1 = payload['u_id']
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
    payload = response.json()
    assert(payload == {
        'name': 'Channel1',
        'owner_members': [
            {
                'u_id': u_id_1,
                'name_first': 'Andreea',
                'name_last': 'Vissarion',
                'profile_img_url': None
            }
        ],
        'all_members': [
            {
                'u_id': u_id_1,
                'name_first': 'Andreea',
                'name_last': 'Vissarion',
                'profile_img_url': None
            },
            {
                'u_id': u_id_2,
                'name_first': 'John',
                'name_last': 'Smith',
                'profile_img_url': None
            }
        ],
    })
    requests.delete(url + 'clear')    

def test_invalid_token_http(url):
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

    data_in = {
        'token' : token,
        'name' : "Channel1",
        'is_public' : True
    }

    response = requests.post(url + 'channels/create', json = data_in)
    payload = response.json()
    channel_id = payload['channel_id']

    data_in = {
        'token' : 'imalil',
        'channel_id' : channel_id
    }

    response = requests.get(url + 'channel/details', params=data_in)
    assert (response.status_code == 400)
    requests.delete(url + 'clear')

def test_not_member_http(url):
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
    token_2 = payload['token']

    data_in = {
        'token' : token_1,
        'name' : "Channel1",
        'is_public' : True
    }

    response = requests.post(url + 'channels/create', json = data_in)
    payload = response.json()
    channel_id = payload['channel_id']

    data_in = {
        'token' : token_2,
        'channel_id' : channel_id
    }
    response = requests.get(url + 'channel/details', params = data_in)

    assert(response.status_code == 400)
    requests.delete(url + 'clear')

def test_missing_channel_http(url): # invalid channel_id - InputError
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

    channel_id = 1
    
    data_in = {
        'token' : token,
        'channel_id' : channel_id
    }
    response = requests.get(url + 'channel/details', params = data_in)

    assert(response.status_code == 400)
    requests.delete(url + 'clear')

