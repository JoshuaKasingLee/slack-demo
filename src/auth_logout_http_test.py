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

# Tests a successful log-out
def test_successful_logout_http(url):
    requests.delete(url + 'clear')
    # register a user
    data_in = {
        'email' : "testmail@gmail.com",
        'password' : "password",
        'name_first' : "John",
        'name_last' : "Smith"
    }
    response = requests.post(url + 'auth/register', json = data_in)
    assert (response.status_code == 200)
    # log the user in
    data_in = {
        'email' : "testmail@gmail.com",
        'password' : "password"
    }
    response = requests.post(url + 'auth/login', json = data_in)
    assert (response.status_code == 200)
    payload = response.json()
    # log the user out
    data_in = {'token': payload['token']}
    response = requests.post(url + 'auth/logout', json = data_in)
    payload = response.json()
    assert(payload == {"is_success": True})
    requests.delete(url + 'clear')

def test_failed_no_token_http(url):
    requests.delete(url + 'clear')
    data_in = {'token': ""}
    response = requests.post(url + 'auth/logout', json = data_in)
    payload = response.json()
    assert(payload == {"is_success": False})
    requests.delete(url + 'clear')


def test_failed_bad_taken_http(url):
    requests.delete(url + 'clear')
    # register a user
    data_in = {
        'email' : "testmail@gmail.com",
        'password' : "password",
        'name_first' : "John",
        'name_last' : "Smith"
    }
    response = requests.post(url + 'auth/register', json = data_in)
    assert (response.status_code == 200)
    # log the user in
    data_in = {
        'email' : "testmail@gmail.com",
        'password' : "password"
    }
    response = requests.post(url + 'auth/login', json = data_in)
    assert (response.status_code == 200)
    # attempt to log user out
    data_in = {'token': "Bad Token"}
    response = requests.post(url + 'auth/logout', json = data_in)
    payload = response.json()
    assert(payload == {"is_success": False})
    requests.delete(url + 'clear')

def test_mixed_order_http(url):
    requests.delete(url + 'clear')
    # register a user
    data_in = {
        'email' : "testmail1@gmail.com",
        'password' : "password",
        'name_first' : "John",
        'name_last' : "Smith"
    }
    response = requests.post(url + 'auth/register', json = data_in)
    assert (response.status_code == 200)
    payload = response.json()
    token1 = payload['token']
    # register another user
    data_in = {
        'email' : "testmail2@gmail.com",
        'password' : "password",
        'name_first' : "John",
        'name_last' : "Smith"
    }
    response = requests.post(url + 'auth/register', json = data_in)
    assert (response.status_code == 200)
    payload = response.json()
    token2 = payload['token']
    # register another user
    data_in = {
        'email' : "testmail3@gmail.com",
        'password' : "password",
        'name_first' : "John",
        'name_last' : "Smith"
    }
    response = requests.post(url + 'auth/register', json = data_in)
    assert (response.status_code == 200)
    payload = response.json()
    token3 = payload['token']
    # log user 3 out
    response = requests.post(url + 'auth/logout', json = {'token': token3})
    payload = response.json()
    assert(payload == {"is_success": True})
    # log user 1 out
    response = requests.post(url + 'auth/logout', json = {'token': token1})
    payload = response.json()
    assert(payload == {"is_success": True})
    # log user 2 out
    response = requests.post(url + 'auth/logout', json = {'token': token2})
    payload = response.json()
    assert(payload == {"is_success": True})
    requests.delete(url + 'clear')

def test_logout_twice_http(url):
    requests.delete(url + 'clear')
    # register a user
    data_in = {
        'email' : "testmail1@gmail.com",
        'password' : "password",
        'name_first' : "John",
        'name_last' : "Smith"
    }
    response = requests.post(url + 'auth/register', json = data_in)
    assert (response.status_code == 200)
    payload = response.json()
    token = payload['token']
    # log user out
    response = requests.post(url + 'auth/logout', json = {'token': token})
    payload = response.json()
    assert(payload == {"is_success": True})
    # attempt to log user out again
    response = requests.post(url + 'auth/logout', json = {'token': token})
    payload = response.json()
    assert(payload == {"is_success": False})
    requests.delete(url + 'clear')

