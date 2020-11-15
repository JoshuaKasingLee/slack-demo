import pytest
import re
from subprocess import Popen, PIPE
import signal
from time import sleep
import requests
from database import master_users

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

# check that request for a valid email works
def test_valid_email_http(url):
    requests.delete(url + 'clear')
    # register user
    data_in = {
        'email' : "cyruschow@gmail.com", 
        'password' : "ilikecookies",
        'name_first' : "Cyrus",
        'name_last' : "Chow"
    }
    response = requests.post(url + 'auth/register', json = data_in)
    assert (response.status_code == 200)
    # return valid user information
    payload = response.json()
    u_id = payload['u_id']
    token = payload['token']
    data_in = {
        'token': token,
        'u_id': u_id
    }
    response = requests.get(url + 'user/profile', data_in)
    assert (response.status_code == 200)
    payload = response.json()
    email = payload['user']['email']
    # log the user out
    data_in = {'token': token}
    response = requests.post(url + 'auth/logout', json = data_in)
    payload = response.json()
    assert(payload == {"is_success": True})
    # request forgotten password
    data_in = {'email' : email}
    response = requests.post(url + 'auth/passwordreset/request', json = data_in)
    assert (response.status_code == 200)
    payload = response.json()
    assert(payload == {})
    requests.delete(url + 'clear')

# check that request for a non-registered email still processes
def test_invalid_email_http(url):
    requests.delete(url + 'clear')
    # register user
    data_in = {
        'email' : "cyruschow@gmail.com", 
        'password' : "ilikecookies",
        'name_first' : "Cyrus",
        'name_last' : "Chow"
    }
    response = requests.post(url + 'auth/register', json = data_in)
    assert (response.status_code == 200)
    # return valid user information
    payload = response.json()
    u_id = payload['u_id']
    token = payload['token']
    data_in = {
        'token': token,
        'u_id': u_id
    }
    response = requests.get(url + 'user/profile', data_in)
    payload = response.json()
    email = payload['user']['email']
    # log the user out
    data_in = {'token': token}
    response = requests.post(url + 'auth/logout', json = data_in)
    payload = response.json()
    assert(payload == {"is_success": True})
    # request forgotten password
    data_in = {'email' : email}
    response = requests.post(url + 'auth/passwordreset/request', json = data_in)
    assert (response.status_code == 200)
    requests.delete(url + 'clear')