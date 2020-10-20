import pytest
import re
from subprocess import Popen, PIPE
import signal
from time import sleep
import requests
import json

import channel
import channels
import auth


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

def test_url(url):
    '''
    A simple sanity test to check that your server is set up properly
    '''
    assert url.startswith("http")

#TESTING OF CHANNEL FUNCTIONS

def test_owner_http(url):
    user = auth.auth_register("test1@gmail.com", "password", "John", "Smith")
    u_id = user['u_id']
    token = user['token']
    channel_id = channels.channels_create(token, "Channel1", True)['channel_id']    
    request = requests.get(url + 'channel/details', params=(token, channel_id))
    payload = request.json()
    assert(payload == {
        'name': 'Channel1',
        'owner_members': [
         {
            'u_id': u_id, 
            'name_first': 'John',
            'name_last': 'Smith',
        }],
        'all_members': [
            {
                'u_id': u_id, 
                'name_first': 'John',
                'name_last': 'Smith',
            }
        ],
    })

def test_one_owner_two_members_http():
    user_1 = auth.auth_register("email1@gmail.com", "password", "Andreea", "Vissarion")
    token_1 = user_1['token']
    u_id_1 = user_1['u_id']
    user_2 = auth.auth_register("email2@gmail.com", "password", "John", "Smith")
    u_id_2 = user_2['u_id']
    channel_id = channels.channels_create(token_1, "Channel1", True)['channel_id']
    channel.channel_invite(token_1, channel_id, u_id_2)
    request = requests.get(url + 'channel/details', params=(token_1, channel_id))
    payload = request.json()
    assert(payload == {
        'name': 'Channel1',
        'owner_members': [
            {
                'u_id': u_id_1,
                'name_first': 'Andreea',
                'name_last': 'Vissarion',
            }
        ],
        'all_members': [
            {
                'u_id': u_id_1,
                'name_first': 'Andreea',
                'name_last': 'Vissarion',
            },
            {
                'u_id': u_id_2,
                'name_first': 'John',
                'name_last': 'Smith',
            }
        ],
    })    

def test_invalid_token_http():
    user = auth.auth_register("test1@gmail.com", "password", "John", "Smith")
    token = user['token']
    channel_id = channels.channels_create(token, "channel1", True)['channel_id']
    request = requests.get(url + 'channel/details', params=('imalil', channel_id))
    payload = request.json()
    assert (payload.status_code == 400)

def test_not_member_http():
    user_1 = auth.auth_register("email1@gmail.com", "password", "Andreea", "Vissarion")
    token_1 = user_1['token']
    user_2 = auth.auth_register("email2@gmail.com", "password", "John", "Smith")
    token_2 = user_2['token']
    channel_id = channels.channels_create(token_1, "channel1", True)['channel_id']
    request = requests.get(url + 'channel/details', params=(token_2, channel_id))
    payload = request.json()
    assert(payload.status_code == 400)

def test_missing_channel_http(): # invalid channel_id - InputError
    user = auth.auth_register("test1@gmail.com", "password", "John", "Smith")
    token = user['token']
    channel_id = 1
    request = requests.get(url + 'channel/details', params=(token, channel_id))
    payload = request.json()
    assert(payload.status_code == 400)