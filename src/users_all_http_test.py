import pytest
import re
from subprocess import Popen, PIPE
import signal
from time import sleep
import requests

data_in_1 = {
        'email' : "jonathon@gmail.com",
        'password' : "password",
        'name_first' : "John",
        'name_last' : "Smith"
    }

data_in_2 = {
        'email' : "sallychampion@gmail.com",
        'password' : "password",
        'name_first' : "Sally",
        'name_last' : "Champion"
    }

token = {}

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


def test_one(url) :
    requests.delete(url + 'clear')
    response = requests.post(url + 'auth/register', json = data_in_1)
    payload = response.json()
    u_id = payload['u_id']
    response = requests.get(url + 'users/all', payload)
    payload = response.json()
    assert payload == {
        'users': [
            {
                'u_id': u_id,
                'email': 'jonathon@gmail.com',
                'name_first': 'John',
                'name_last': 'Smith',
                'handle_str': 'johnsmith',
            },
        ],
    }
    requests.delete(url + 'clear')
    
def test_two(url) :
    requests.delete(url + 'clear')
    response = requests.post(url + 'auth/register', json = data_in_1)
    payload = response.json()
    token['token'] = payload['token']
    u_id = payload['u_id']
    response = requests.post(url + 'auth/register', json = data_in_2)
    payload = response.json()
    u_id_2 = payload['u_id']
    response = requests.get(url + 'users/all', token)
    payload = response.json()
    assert payload == {
        'users': [
            {
                'u_id': u_id,
                'email': 'jonathon@gmail.com',
                'name_first': 'John',
                'name_last': 'Smith',
                'handle_str': 'johnsmith',
            },
            {
                'u_id': u_id_2,
                'email': 'sallychampion@gmail.com',
                'name_first': 'Sally',
                'name_last': 'Champion',
                'handle_str': 'sallychampion',
            },
        ],                
    }
    requests.delete(url + 'clear')

def test_invalid_token(url): # wrong user token - accesserror
    requests.delete(url + 'clear')
    response = requests.post(url + 'auth/register', json = data_in_1)
    token['token'] = 100
    response = requests.get(url + 'users/all', token)
    assert (response.status_code == 400)
    requests.delete(url + 'clear')