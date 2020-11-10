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


def test_valid_user_http(url):
    requests.delete(url + 'clear')
    # register user
    data_in = {
        'email' : "kellyzhou@gmail.com", 
        'password' : "pink=bestcolour",
        'name_first' : "Kelly",
        'name_last' : "Zhou"
    }
    response = requests.post(url + 'auth/register', json = data_in)
    assert (response.status_code == 200)
    # return valid user information
    payload = response.json()
    u_id = payload['u_id']
    data_in = {
        'token': payload['token'],
        'u_id': payload['u_id']
    }
    response = requests.get(url + 'user/profile', data_in)
    payload = response.json()
    correct_profile = {"user": {"u_id": u_id, "email": "kellyzhou@gmail.com", \
        "name_first": "Kelly", "name_last": "Zhou", "handle_str": "kellyzhou"}}
    assert(payload == correct_profile)
    requests.delete(url + 'clear')

def test_valid_users_http(url):
    requests.delete(url + 'clear')
    # register user 1
    data_in = {
        'email' : "cyruschow@gmail.com", 
        'password' : "ilikecookies",
        'name_first' : "Cyrus",
        'name_last' : "Chow"
    }
    response = requests.post(url + 'auth/register', json = data_in)
    assert (response.status_code == 200)
    user1 = response.json()
    # register user 2
    data_in = {
        'email' : "kellyzhou@gmail.com", 
        'password' : "pink=bestcolour",
        'name_first' : "Kelly",
        'name_last' : "Zhou"
    }
    response = requests.post(url + 'auth/register', json = data_in)
    assert (response.status_code == 200)
    # register user 3
    data_in = {
        'email' : "andreeavissarion@hotmail.com", 
        'password' : "coolestshoes!!",
        'name_first' : "Andreea",
        'name_last' : "Vissarion"
    }
    response = requests.post(url + 'auth/register', json = data_in)
    assert (response.status_code == 200)
    user2 = response.json()
    # register user 4
    data_in = {
        'email' : "joshualee@icloud.org", 
        'password' : "randypopping",
        'name_first' : "Josh",
        'name_last' : "Lee"
    }
    response = requests.post(url + 'auth/register', json = data_in)
    assert (response.status_code == 200)
    # register user 5
    data_in = {
        'email' : "nickdodd@gmail.com", 
        'password' : "doddthegod",
        'name_first' : "Nick",
        'name_last' : "Dodd"
    }
    response = requests.post(url + 'auth/register', json = data_in)
    assert (response.status_code == 200)
    # return valid users information
    data_in = {
        'token': user1['token'],
        'u_id': user1['u_id']
    }
    response = requests.get(url + 'user/profile', data_in)
    profile1 = response.json()
    data_in = {
        'token': user2['token'],
        'u_id': user2['u_id']
    }
    response = requests.get(url + 'user/profile', data_in)
    profile2 = response.json()
    correct_profile1 = {"user": {"u_id" : user1['u_id'], "email" : "cyruschow@gmail.com", \
        "name_first": "Cyrus", "name_last": "Chow", "handle_str": "cyruschow"}}
    correct_profile2 = {"user": {"u_id" : user2['u_id'], "email" : "andreeavissarion@hotmail.com", \
        "name_first": "Andreea", "name_last": "Vissarion", "handle_str": "andreeavissarion"}}
    assert(profile1 == correct_profile1)
    assert(profile2 == correct_profile2)
    requests.delete(url + 'clear')

def test_invalid_u_id_http(url):
    requests.delete(url + 'clear')
    data_in = {
        'token': '404',
        'u_id': 404
    }
    response = requests.get(url + 'user/profile', data_in)
    assert (response.status_code == 400)
    requests.delete(url + 'clear')

def test_invalid_token_http(url):
    # register user
    data_in = {
        'email' : "kellyzhou@gmail.com", 
        'password' : "pink=bestcolour",
        'name_first' : "Kelly",
        'name_last' : "Zhou"
    }
    response = requests.post(url + 'auth/register', json = data_in)
    assert (response.status_code == 200)
    payload = response.json()
    u_id = payload['u_id']
    # attempt to return user profile
    data_in = {
        'token': 'badtoken',
        'u_id': u_id
    }
    response = requests.get(url + 'user/profile', data_in)
    assert (response.status_code == 400)
    requests.delete(url + 'clear')
