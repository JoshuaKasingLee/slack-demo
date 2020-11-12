import pytest
import re
from subprocess import Popen, PIPE
import signal
from time import sleep
import requests
import json
import time

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

# Test to make sure that message is sent with the time delay
def test_message_delay(url):
    requests.delete(url + 'clear')
    data_in = {
        'email': "user@gmail.com",
        'password': "password",
        'name_first': "John",
        'name_last': "Smith",
    }
    response = requests.post(url + 'auth/register', json = data_in)
    payload = response.json()
    token = payload['token']

    data_in = {
        'token': token,
        'name': "Test channel",
        'is_public': True,
    }

    response = requests.post(url + 'channels/create', json = data_in)
    payload = response.json()
    channel_id = payload['channel_id']

    curr_time = time.time()
    time_sent = curr_time + 5

    data_in = {
        'token': token,
        'channel_id': channel_id,
        'message': 'Hi!',
        'time_sent': time_sent,
    }

    response = requests.post(url + 'message/sendlater', json = data_in)
    
    data_in = {
        'token': token,
        'channel_id': channel_id,
        'start': 0,
    }

    response = requests.get(url + 'channel/messages', params = data_in)
    payload = response.json()
    channel_messages = payload['messages']
    assert(len(channel_messages) == 0)

    time.sleep(5)

    data_in = {
        'token': token,
        'channel_id': channel_id,
        'start': 0,
    }

    response = requests.get(url + 'channel/messages', params = data_in)
    payload = response.json()
    channel_messages = payload['messages']
    assert(len(channel_messages) == 1)
    requests.delete(url + 'clear')

# Test to make sure test cannot be sent into the past ~ Raise input error
def test_message_to_past(url):
    requests.delete(url + 'clear')
    data_in = {
        'email': "user@gmail.com",
        'password': "password",
        'name_first': "John",
        'name_last': "Smith",
    }
    response = requests.post(url + 'auth/register', json = data_in)
    payload = response.json()
    token = payload['token']

    data_in = {
        'token': token,
        'name': "Test channel",
        'is_public': True,
    }

    response = requests.post(url + 'channels/create', json = data_in)
    payload = response.json()
    channel_id = payload['channel_id']

    curr_time = time.time()
    time_sent = curr_time - 5

    data_in = {
        'token': token,
        'channel_id': channel_id,
        'message': 'Hi!',
        'time_sent': time_sent,
    }

    response = requests.post(url + 'message/sendlater', json = data_in)
    assert(response.status_code == 400)
    requests.delete(url + 'clear')

# Check to make sure message length is > than 1000
def test_message_length_http(url):
    requests.delete(url + 'clear')
    data_in = {
        'email': "user@gmail.com",
        'password': "password",
        'name_first': "John",
        'name_last': "Smith",
    }
    response = requests.post(url + 'auth/register', json = data_in)
    payload = response.json()
    token = payload['token']
    
    data_in = {
        'token': token,
        'name': "Test channel",
        'is_public': True,   
    }
    response = requests.post(url + 'channels/create', json = data_in)
    payload = response.json()
    channel_id = payload['channel_id']

    response = requests.post(url + 'channel/join', json = data_in)

    curr_time = time.time()
    time_sent = curr_time + 5

    data_in = {
        'token': token,
        'channel_id': channel_id,
        'message': 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium. Integer tincidunt. Cras dapibus. Vivamus elementum semper nisi. Aenean vulputate eleifend tellus. Aenean leo ligula, porttitor eu, consequat vitae, eleifend ac, enim. Aliquam lorem ante, dapibus in, viverra quis, feugiat a, tellus. Phasellus viverra nulla ut metus varius laoreet. Quisque rutrum. Aenean imperdiet. Etiam ultricies nisi vel augue. Curabitur ullamcorper ultricies nisi. Nam eget dui. Etiam rhoncus. Maecenas tempus, tellus eget condimentum rhoncus, sem quam semper libero, sit amet adipiscing sem neque sed ipsum. Na',
        'time_sent': time_sent,
    }
    response = requests.post(url + 'message/sendlater', json = data_in)
    assert(response.status_code == 400)
    requests.delete(url + 'clear')

# Make sure user cannot send if they haven't joined the channel they want to join
def test_user_in_channel_http(url):
    requests.delete(url + 'clear')
    data_in = {
        'email': "user@gmail.com",
        'password': "password",
        'name_first': "John",
        'name_last': "Smith",
    }
    response = requests.post(url + 'auth/register', json = data_in)
    payload = response.json()
    token = payload['token']
    
    data_in = {
        'token': token,
        'name': "Test channel",
        'is_public': True,   
    }
    
    response = requests.post(url + 'channels/create', json = data_in)
    payload = response.json()
    channel_id = payload['channel_id']

    data_in = {
        'email': "user2@gmail.com",
        'password': "password",
        'name_first': "Sam",
        'name_last': "Smith",
    }
    response = requests.post(url + 'auth/register', json = data_in)
    payload = response.json()
    token = payload['token']

    curr_time = time.time()
    time_sent = curr_time + 5

    data_in = {
        'token': token,
        'channel_id': channel_id,
        'message': 'Hi!',
        'time_sent': time_sent,
    }

    response = requests.post(url + 'message/sendlater', json = data_in)
    assert(response.status_code == 400)
    requests.delete(url + 'clear')

# Make sure message is correct (payload is correct)
def test_message_success(url):
    requests.delete(url + 'clear')
    data_in = {
        'email': "user@gmail.com",
        'password': "password",
        'name_first': "John",
        'name_last': "Smith",
    }
    response = requests.post(url + 'auth/register', json = data_in)
    payload = response.json()
    token = payload['token']

    data_in = {
        'token': token,
        'name': "Test channel",
        'is_public': True,
    }

    response = requests.post(url + 'channels/create', json = data_in)
    payload = response.json()
    channel_id = payload['channel_id']

    curr_time = time.time()
    time_sent = curr_time + 5

    data_in = {
        'token': token,
        'channel_id': channel_id,
        'message': 'Hi!',
        'time_sent': time_sent,
    }

    response = requests.post(url + 'message/sendlater', json = data_in)
    
    data_in = {
        'token': token,
        'channel_id': channel_id,
        'start': 0,
    }

    response = requests.get(url + 'channel/messages', params = data_in)
    payload = response.json()
    channel_messages = payload['messages']
    assert(len(channel_messages) == 0)

    time.sleep(5)

    data_in = {
        'token': token,
        'channel_id': channel_id,
        'start': 0,
    }

    response = requests.get(url + 'channel/messages', params = data_in)
    payload = response.json()
    channel_messages = payload['messages'][0]['message']
    assert(channel_messages == 'Hi!')
    requests.delete(url + 'clear')