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


def test_change_first_name_http(url):
    requests.delete(url + 'clear')
    # register user
    data_in = {
        'email' : "frankiefort@gmail.com", 
        'password' : "falala",
        'name_first' : "Frankie",
        'name_last' : "Fort"
    }
    response = requests.post(url + 'auth/register', json = data_in)
    assert (response.status_code == 200)
    payload = response.json()
    # change name
    data_in = {
        'token': payload['token'],
        'name_first': 'Frankenstein',
        'name_last': 'Fort'
    }
    response = requests.put(url + 'user/profile/setname', json = data_in)
    # check user profile
    data_in = {
        'token': payload['token'],
        'u_id': payload['u_id']
    }
    response = requests.get(url + 'user/profile', data_in)
    profile = response.json()
    assert(profile["user"]["name_first"] == "Frankenstein")
    assert(profile["user"]["name_last"] == "Fort")
    assert(profile["user"]["handle_str"] == "frankiefort")
    requests.delete(url + 'clear')

def test_change_last_name_http(url):
    requests.delete(url + 'clear')
    # register user
    data_in = {
        'email' : "frankiefort@gmail.com", 
        'password' : "falala",
        'name_first' : "Frankie",
        'name_last' : "Fort"
    }
    response = requests.post(url + 'auth/register', json = data_in)
    assert (response.status_code == 200)
    payload = response.json()
    # change name
    data_in = {
        'token': payload['token'],
        'name_first': 'Frankie',
        'name_last': 'Fantastic'
    }
    response = requests.put(url + 'user/profile/setname', json = data_in)
    # check user profile
    data_in = {
        'token': payload['token'],
        'u_id': payload['u_id']
    }
    response = requests.get(url + 'user/profile', data_in)
    profile = response.json()
    assert(profile["user"]["name_first"] == "Frankie")
    assert(profile["user"]["name_last"] == "Fantastic")
    assert(profile["user"]["handle_str"] == "frankiefort")
    requests.delete(url + 'clear')


def test_change_name_http(url):
    requests.delete(url + 'clear')
    # register user
    data_in = {
        'email' : "moanadisney@gmail.com", 
        'password' : "bluesea",
        'name_first' : "Moana",
        'name_last' : "Disney"
    }
    response = requests.post(url + 'auth/register', json = data_in)
    assert (response.status_code == 200)
    payload = response.json()
    # change name
    data_in = {
        'token': payload['token'],
        'name_first': 'Cinderella',
        'name_last': 'Princess'
    }
    response = requests.put(url + 'user/profile/setname', json = data_in)
    # check user profile
    data_in = {
        'token': payload['token'],
        'u_id': payload['u_id']
    }
    response = requests.get(url + 'user/profile', data_in)
    profile = response.json()
    assert(profile["user"]["name_first"] == "Cinderella")
    assert(profile["user"]["name_last"] == "Princess")
    assert(profile["user"]["handle_str"] == "moanadisney")
    requests.delete(url + 'clear')

def test_change_many_names_http(url):
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
    user2 = response.json()
    # register user 3
    data_in = {
        'email' : "andreeavissarion@hotmail.com", 
        'password' : "coolestshoes!!",
        'name_first' : "Andreea",
        'name_last' : "Vissarion"
    }
    response = requests.post(url + 'auth/register', json = data_in)
    assert (response.status_code == 200)
    user3 = response.json()
    # change names of all users
    data_in = {
        'token': user1['token'],
        'name_first': 'Cyrus Yu Seng',
        'name_last': 'Chow'
    }
    response = requests.put(url + 'user/profile/setname', json = data_in)
    data_in = {
        'token': user2['token'],
        'name_first': 'Kel',
        'name_last': 'Zhou'
    }
    response = requests.put(url + 'user/profile/setname', json = data_in)
    data_in = {
        'token': user3['token'],
        'name_first': 'Andy',
        'name_last': 'Viss'
    }
    response = requests.put(url + 'user/profile/setname', json = data_in)
    # check user profiles
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
    data_in = {
        'token': user3['token'],
        'u_id': user3['u_id']
    }
    response = requests.get(url + 'user/profile', data_in)
    profile3 = response.json()
    correct_profile1 = {"user": {"u_id" : user1['u_id'], "email" : "cyruschow@gmail.com", \
        "name_first": "Cyrus Yu Seng", "name_last": "Chow", "handle_str": "cyruschow"}}
    correct_profile2 = {"user": {"u_id" : user2['u_id'], "email" : "kellyzhou@gmail.com", \
        "name_first": "Kel", "name_last": "Zhou", "handle_str": "kellyzhou"}}
    correct_profile3 = {"user": {"u_id" : user3['u_id'], "email" : "andreeavissarion@hotmail.com", \
        "name_first": "Andy", "name_last": "Viss", "handle_str": "andreeavissarion"}}
    assert(profile1 == correct_profile1)
    assert(profile2 == correct_profile2)
    assert(profile3 == correct_profile3)
    requests.delete(url + 'clear')

def test_change_short_name_1_http(url):
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
    payload = response.json()
    # change user name
    data_in = {
        'token': payload['token'],
        'name_first': '',
        'name_last': 'Chow'
    }
    response = requests.put(url + 'user/profile/setname', json = data_in)
    assert (response.status_code == 400)
    requests.delete(url + 'clear')

def test_change_short_name_2_http(url):
    requests.delete(url + 'clear')
    # register user
    data_in = {
        'email' : "andreeavissarion@hotmail.com", 
        'password' : "coolestshoes!!",
        'name_first' : "Andreea",
        'name_last' : "Vissarion"
    }
    response = requests.post(url + 'auth/register', json = data_in)
    assert (response.status_code == 200)
    payload = response.json()
    # change user name
    data_in = {
        'token': payload['token'],
        'name_first': 'Andreea',
        'name_last': ''
    }
    response = requests.put(url + 'user/profile/setname', json = data_in)
    assert (response.status_code == 400)
    requests.delete(url + 'clear')


def test_change_long_name_1_http(url):
    requests.delete(url + 'clear')
    # register user
    data_in = {
        'email' : "joshualee@icloud.org", 
        'password' : "randypopping",
        'name_first' : "Josh",
        'name_last' : "Lee"
    }
    response = requests.post(url + 'auth/register', json = data_in)
    assert (response.status_code == 200)
    payload = response.json()
    # change user name
    data_in = {
        'token': payload['token'],
        'name_first': 'Lee',
        'name_last': 'JoshuaJoshuaJoshuaJoshuaJoshuaJoshuaJoshuaJoshuaJoshua'
    }
    response = requests.put(url + 'user/profile/setname', json = data_in)
    assert (response.status_code == 400)
    requests.delete(url + 'clear')

def test_change_long_name_2_http(url):
    requests.delete(url + 'clear')
    # register user
    data_in = {
        'email' : "nickdodd@gmail.com", 
        'password' : "doddthegod",
        'name_first' : "Nick",
        'name_last' : "Dodd"
    }
    response = requests.post(url + 'auth/register', json = data_in)
    assert (response.status_code == 200)
    payload = response.json()
    # change user name
    data_in = {
        'token': payload['token'],
        'name_first': 'NicholasIsTheGreatestNicholasIsTheGreatestNicholasIsTheGreatest',
        'name_last': 'Dodd'
    }
    response = requests.put(url + 'user/profile/setname', json = data_in)
    assert (response.status_code == 400)
    requests.delete(url + 'clear')

def test_change_no_name_http(url):
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
    payload = response.json()
    # change user name
    data_in = {
        'token': payload['token'],
        'name_first': '',
        'name_last': ''
    }
    response = requests.put(url + 'user/profile/setname', json = data_in)
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
    # change user name
    data_in = {
        'token': 'badtoken',
        'name_first': 'Valid',
        'name_last': 'Name'
    }
    response = requests.put(url + 'user/profile/setname', json = data_in)
    assert (response.status_code == 400)
    requests.delete(url + 'clear')