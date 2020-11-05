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

def test_one_http(url):
    requests.delete(url + 'clear')
    # register users
    data_in = {
        'email' : "email@gmail.com",
        'password' : "password",
        'name_first' : "Andreea",
        'name_last' : "Viss"
    }
    response = requests.post(url + 'auth/register', json = data_in)
    assert (response.status_code == 200)
    payload = response.json()
    token = payload['token']
    # create new channel
    data_in = {
        'token': token,
        'name': 'Channel1',
        'is_public': True
    }
    response = requests.post(url + 'channels/create', json = data_in)
    assert (response.status_code == 200)
    payload = response.json()
    channel_id = payload['channel_id']
    # return all channels
    response = requests.get(url + 'channels/listall', params = {'token': token})
    payload = response.json()
    assert (payload == {
        'channels': [
        	{
        		'channel_id': channel_id,
        		'name': 'Channel1',
        	}
        ],
    })
    requests.delete(url + 'clear')

def test_two_owner_http(url):
    requests.delete(url + 'clear')
    # register users
    data_in = {
        'email' : "email@gmail.com",
        'password' : "password",
        'name_first' : "Andreea",
        'name_last' : "Viss"
    }
    response = requests.post(url + 'auth/register', json = data_in)
    assert (response.status_code == 200)
    payload = response.json()
    token = payload['token']
    # create new channels
    data_in = {
        'token': token,
        'name': 'Channel1',
        'is_public': True
    }
    response = requests.post(url + 'channels/create', json = data_in)
    assert (response.status_code == 200)
    payload = response.json()
    channel_id1 = payload['channel_id']
    data_in = {
        'token': token,
        'name': 'Channel2',
        'is_public': False
    }
    response = requests.post(url + 'channels/create', json = data_in)
    assert (response.status_code == 200)
    payload = response.json()
    channel_id2 = payload['channel_id']
    # return all channels
    response = requests.get(url + 'channels/listall', params = {'token': token})
    payload = response.json()
    assert (payload == {
        'channels': [
        	{
        		'channel_id': channel_id1,
        		'name': 'Channel1',
        	},
        {
        		'channel_id': channel_id2,
        		'name': 'Channel2',
        	}
        ],
    })
    requests.delete(url + 'clear')
        

def test_two_not_owner_http(url):
    requests.delete(url + 'clear')
    # register users
    data_in = {
        'email' : "email1@gmail.com",
        'password' : "password",
        'name_first' : "Andreea1",
        'name_last' : "Viss1"
    }
    response = requests.post(url + 'auth/register', json = data_in)
    assert (response.status_code == 200)
    payload = response.json()
    token1 = payload['token']
    data_in = {
        'email' : "email2@gmail.com",
        'password' : "password",
        'name_first' : "Andreea2",
        'name_last' : "Viss2"
    }
    response = requests.post(url + 'auth/register', json = data_in)
    assert (response.status_code == 200)
    payload = response.json()
    token2 = payload['token']
    # create new channels
    data_in = {
        'token': token1,
        'name': 'Channel1',
        'is_public': True
    }
    response = requests.post(url + 'channels/create', json = data_in)
    assert (response.status_code == 200)
    payload = response.json()
    channel_id1 = payload['channel_id']
    data_in = {
        'token': token2,
        'name': 'Channel2',
        'is_public': False
    }
    response = requests.post(url + 'channels/create', json = data_in)
    assert (response.status_code == 200)
    payload = response.json()
    channel_id2 = payload['channel_id']
    # return all channels
    response = requests.get(url + 'channels/listall', params = {'token': token1})
    payload = response.json()
    assert (payload == {
        'channels': [
        	{
        		'channel_id': channel_id1,
        		'name': 'Channel1',
        	},
        {
        		'channel_id': channel_id2,
        		'name': 'Channel2',
        	}
        ],
    })
    requests.delete(url + 'clear')

  
def test_empty_http(url):
    requests.delete(url + 'clear')
    data_in = {
        'email' : "email@gmail.com",
        'password' : "password",
        'name_first' : "Andreea",
        'name_last' : "Viss"
    }
    response = requests.post(url + 'auth/register', json = data_in)
    assert (response.status_code == 200)
    # return valid user information
    payload = response.json()
    token = payload['token']
    # return all channels
    response = requests.get(url + 'channels/listall', params = {'token': token})
    payload = response.json()
    assert (payload == {
        'channels': [],
    })
    requests.delete(url + 'clear')
    

def test_invalid_token_name_http(url):
    requests.delete(url + 'clear')
    token = "blahblah"
    # return all channels
    response = requests.get(url + 'channels/listall', params = {'token': token})
    assert(response.status_code == 400)
    requests.delete(url + 'clear')
        

def test_invalid_user_http(url):
    requests.delete(url + 'clear')
    data_in = {
        'email' : "email@gmail.com",
        'password' : "password",
        'name_first' : "Andreea",
        'name_last' : "Viss"
    }
    response = requests.post(url + 'auth/register', json = data_in)
    assert (response.status_code == 200)
    # return valid user information
    payload = response.json()
    token = payload['token'] + "1"
    # return all channels
    response = requests.get(url + 'channels/listall', params = {'token': token})
    assert(response.status_code == 400)
    requests.delete(url + 'clear')

# there are no channels
def test_no_channels_http(url):
    requests.delete(url + 'clear')
    data_in = {
        'email' : "user1@example.com",
        'password' : "password",
        'name_first' : "user1",
        'name_last' : "name"
    }
    response = requests.post(url + 'auth/register', json = data_in)
    assert (response.status_code == 200)
    # return valid user information
    payload = response.json()
    user1_token = payload['token']
    # return all channels
    response = requests.get(url + 'channels/listall', params = {'token': user1_token})
    payload = response.json()
    assert(payload == {'channels': []})
    requests.delete(url + 'clear')


# there is one public channel
def test_one_public_http(url):
    requests.delete(url + 'clear')
    data_in = {
        'email' : "user1@example.com",
        'password' : "password",
        'name_first' : "user1",
        'name_last' : "name"
    }
    response = requests.post(url + 'auth/register', json = data_in)
    assert (response.status_code == 200)
    # return valid user information
    payload = response.json()
    user1_token = payload['token']
    # create new channel
    data_in = {
        'token': user1_token,
        'name': 'channel1',
        'is_public': True
    }
    response = requests.post(url + 'channels/create', json = data_in)
    assert (response.status_code == 200)
    # return all channels
    response = requests.get(url + 'channels/listall', params = {'token': user1_token})
    payload = response.json()
    assert(payload == {'channels': [ {'channel_id': 0, 'name': 'channel1' }]})
    requests.delete(url + 'clear')


# there is one private channel
def test_one_private_http(url):
    requests.delete(url + 'clear')
    data_in = {
        'email' : "user1@example.com",
        'password' : "password",
        'name_first' : "user1",
        'name_last' : "name"
    }
    response = requests.post(url + 'auth/register', json = data_in)
    assert (response.status_code == 200)
    # return valid user information
    payload = response.json()
    user1_token = payload['token']
    # create new channel
    data_in = {
        'token': user1_token,
        'name': 'channel1',
        'is_public': False
    }
    response = requests.post(url + 'channels/create', json = data_in)
    assert (response.status_code == 200)
    # return all channels
    response = requests.get(url + 'channels/listall', params = {'token': user1_token})
    payload = response.json()
    assert(payload == {'channels': [ {'channel_id': 0, 'name': 'channel1' }],})
    requests.delete(url + 'clear')

    
# there are two channels
def test_two_channels_http(url):
    requests.delete(url + 'clear')
    data_in = {
        'email' : "user1@example.com",
        'password' : "password",
        'name_first' : "user1",
        'name_last' : "name"
    }
    response = requests.post(url + 'auth/register', json = data_in)
    assert (response.status_code == 200)
    # return valid user information
    payload = response.json()
    user1_token = payload['token']
    # create new channels
    data_in = {
        'token': user1_token,
        'name': 'channel1',
        'is_public': True
    }
    response = requests.post(url + 'channels/create', json = data_in)
    assert (response.status_code == 200)
    data_in = {
        'token': user1_token,
        'name': 'channel2',
        'is_public': False
    }
    response = requests.post(url + 'channels/create', json = data_in)
    assert (response.status_code == 200)
    # return all channels
    response = requests.get(url + 'channels/listall', params = {'token': user1_token})
    payload = response.json()
    assert(payload == {'channels': [ {'channel_id': 0, 'name': 'channel1' }, { 'channel_id': 1, 'name': 'channel2' }],})
    requests.delete(url + 'clear')


# INVALID TOKEN
def test_invalid_token_http(url):
    requests.delete(url + 'clear')
    data_in = {
        'email' : "user1@example.com",  # no ampersand or dot
        'password' : "password",
        'name_first' : "user1",
        'name_last' : "name"
    }
    response = requests.post(url + 'auth/register', json = data_in)
    assert (response.status_code == 200)
    # return valid user information
    payload = response.json()
    user1_token = payload['token']
    # create new channel
    data_in = {
        'token': user1_token,
        'name': 'channel1',
        'is_public': True
    }
    response = requests.post(url + 'channels/create', json = data_in)
    assert (response.status_code == 200)
    # return all channels
    response = requests.get(url + 'channels/listall', json = {'token': 'bad_tokenn'})
    assert (response.status_code == 400)
    requests.delete(url + 'clear')

# user does not exist
def test_missing_user_http(url):
    requests.delete(url + 'clear')
    data_in = {
        'email' : "user1@example.com",  # no ampersand or dot
        'password' : "password",
        'name_first' : "user1",
        'name_last' : "name"
    }
    response = requests.post(url + 'auth/register', json = data_in)
    assert (response.status_code == 200)
    # return valid user information
    payload = response.json()
    user1_token = payload['token']
    # create new channel
    data_in = {
        'token': user1_token,
        'name': 'channel1',
        'is_public': True
    }
    response = requests.post(url + 'channels/create', json = data_in)
    assert (response.status_code == 200)
    # return all channels
    response = requests.get(url + 'channels/listall', json = {'token': 996})
    assert (response.status_code == 400)
    requests.delete(url + 'clear')
