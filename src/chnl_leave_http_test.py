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

def leave_http_test(url):
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
        'email' : "email2@gmail.com",
        'password' : "password",
        'name_first' : "John",
        'name_last' : "Smith"
    }
    response = requests.post(url + 'auth/register', json = data_in)
    payload = response.json()
    token_2 = payload['token']
    u_id_2 = payload['u_id']

    data_in = {
        'token' : token,
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

    requests.post(url + 'channel/join', json = data_in)
    requests.delete(url + 'channel/leave', json = data_in)

    response = requests.get(url + 'channel/details', params=(token, channel_id))
    payload = response.json()
    all_members = payload['all_members']
    is_in = 0
    for member in all_members:
        if member['u_id'] == u_id_2:
            is_in = 1
    assert (is_in == 0)

    requests.delete(url + 'clear')

def valid_channel_http_test(url):
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

    data_in = {
        'token' : token,
        'channel_id' : 999
    }
    response = requests.delete(url + 'channel/leave', json = data_in)
    assert (response.status_code == 400)
    requests.delete(url + 'clear')

def not_a_channel_mem_http_test(url):

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
        'email' : "email2@gmail.com",
        'password' : "password",
        'name_first' : "John",
        'name_last' : "Smith"
    }
    response = requests.post(url + 'auth/register', json = data_in)
    payload = response.json()
    token_2 = payload['token']

    data_in = {
        'token' : token,
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
    response = requests.delete(url + 'channel/leave', json = data_in)
    assert (response.status_code == 400)
    requests.delete(url + 'clear')