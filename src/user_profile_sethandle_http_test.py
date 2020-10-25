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

def test_change_valid_handles_http(url):
    requests.delete(url + 'clear')
    # register user
    data_in = {
        'email' : "alphabetnumbers@gmail.com", 
        'password' : "123456",
        'name_first' : "Alphabet",
        'name_last' : "Numbers"
    }
    response = requests.post(url + 'auth/register', json = data_in)
    assert (response.status_code == 200)
    payload = response.json()
    # change user handle multiple times and check user profile
    # change 1
    data_in = {
        'token': payload['token'],
        'handle_str': "numbersalphabet"
    }
    response = requests.put(url + 'user/profile/sethandle', json = data_in)
    data_in = {
        'token': payload['token'],
        'u_id': payload['u_id']
    }
    response = requests.get(url + 'user/profile', json = data_in)
    profile = response.json()
    assert(profile["user"]["handle_str"] == "numbersalphabet")
    # change 2
    data_in = {
        'token': payload['token'],
        'handle_str': "NuMBersAlPhAbeT"
    }
    response = requests.put(url + 'user/profile/sethandle', json = data_in)
    data_in = {
        'token': payload['token'],
        'u_id': payload['u_id']
    }
    response = requests.get(url + 'user/profile', json = data_in)
    profile = response.json()
    assert(profile["user"]["handle_str"] == "NuMBersAlPhAbeT")
    # change 3
    data_in = {
        'token': payload['token'],
        'handle_str': "123456asdfghjkl"
    }
    response = requests.put(url + 'user/profile/sethandle', json = data_in)
    data_in = {
        'token': payload['token'],
        'u_id': payload['u_id']
    }
    response = requests.get(url + 'user/profile', json = data_in)
    profile = response.json()
    assert(profile["user"]["handle_str"] == "123456asdfghjkl")
    # change 4
    data_in = {
        'token': payload['token'],
        'handle_str': "!!  &d# Cn!"
    }
    response = requests.put(url + 'user/profile/sethandle', json = data_in)
    data_in = {
        'token': payload['token'],
        'u_id': payload['u_id']
    }
    response = requests.get(url + 'user/profile', json = data_in)
    profile = response.json()
    assert(profile["user"]["handle_str"] == "!!  &d# Cn!")
    requests.delete(url + 'clear')

def test_change_short_handle_http(url):
    requests.delete(url + 'clear')
    # register user
    data_in = {
        'email' : "example@gmail.com", 
        'password' : "password",
        'name_first' : "Jane",
        'name_last' : "Doe"
    }
    response = requests.post(url + 'auth/register', json = data_in)
    assert (response.status_code == 200)
    payload = response.json()
    # change user handle
    data_in = {
        'token': payload['token'],
        'handle_str': "ab"
    }
    response = requests.put(url + 'user/profile/sethandle', json = data_in)
    assert (response.status_code == 400)
    requests.delete(url + 'clear')

def test_change_long_handle_http(url):
    requests.delete(url + 'clear')
    # register user
    data_in = {
        'email' : "example@gmail.com", 
        'password' : "password",
        'name_first' : "Jane",
        'name_last' : "Doe"
    }
    response = requests.post(url + 'auth/register', json = data_in)
    assert (response.status_code == 200)
    payload = response.json()
    # change user handle
    data_in = {
        'token': payload['token'],
        'handle_str': "janedoeisthebestpersonintheuniverse"
    }
    response = requests.put(url + 'user/profile/sethandle', json = data_in)
    assert (response.status_code == 400)
    requests.delete(url + 'clear')

def test_change_no_handle_http(url):
    requests.delete(url + 'clear')
    # register user
    data_in = {
        'email' : "example@gmail.com", 
        'password' : "password",
        'name_first' : "Jane",
        'name_last' : "Doe"
    }
    response = requests.post(url + 'auth/register', json = data_in)
    assert (response.status_code == 200)
    payload = response.json()
    # change user handle
    data_in = {
        'token': payload['token'],
        'handle_str': ""
    }
    response = requests.put(url + 'user/profile/sethandle', json = data_in)
    assert (response.status_code == 400)
    requests.delete(url + 'clear')

def test_change_handle_taken_http(url):
    requests.delete(url + 'clear')
    # register users
    data_in = {
        'email' : "kellyzhou@gmail.com", 
        'password' : "cats<3",
        'name_first' : "Kelly",
        'name_last' : "Zhou"
    }
    response = requests.post(url + 'auth/register', json = data_in)
    assert (response.status_code == 200)
    data_in = {
        'email' : "joshualee@gmail.com", 
        'password' : "cats<3",
        'name_first' : "Josh",
        'name_last' : "Lee"
    }
    response = requests.post(url + 'auth/register', json = data_in)
    assert (response.status_code == 200)
    user2 = response.json()
    # attempt to change user handle
    data_in = {
        'token': user2['token'],
        'handle_str': 'kellyzhou'
    }
    response = requests.put(url + 'user/profile/sethandle', json = data_in)
    assert (response.status_code == 400)
    requests.delete(url + 'clear')

def test_invalid_token_http(url):
    requests.delete(url + 'clear')
    # register user
    data_in = {
        'email' : "kellyzhou@gmail.com", 
        'password' : "cats<3",
        'name_first' : "Kelly",
        'name_last' : "Zhou"
    }
    response = requests.post(url + 'auth/register', json = data_in)
    assert (response.status_code == 200)
    # change user handle
    data_in = {
        'token': 'badtoken',
        'handle_str': 'validhandle'
    }
    response = requests.put(url + 'user/profile/sethandle', json = data_in)
    assert (response.status_code == 400)
    requests.delete(url + 'clear')