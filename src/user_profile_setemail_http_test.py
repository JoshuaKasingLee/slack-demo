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

def test_change_valid_email_http(url):
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
    # change user email
    data_in = {
        'token': payload['token'],
        'email': "numbersalphabet@gmail.com"
    }
    response = requests.put(url + 'user/profile/setemail', json = data_in)
    # check user profile
    data_in = {
        'token': payload['token'],
        'u_id': payload['u_id']
    }
    response = requests.get(url + 'user/profile', data_in)
    profile = response.json()
    assert(profile["user"]["email"] == "numbersalphabet@gmail.com")
    assert(profile["user"]["name_first"] == "Alphabet")
    assert(profile["user"]["handle_str"] == "alphabetnumbers")
    requests.delete(url + 'clear')

def test_change_multiple_emails_http(url):
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
    # change user email multiple times
    data_in = {
        'token': payload['token'],
        'email': "numbersalphabet@gmail.com"
    }
    response = requests.put(url + 'user/profile/setemail', json = data_in)
    data_in = {
        'token': payload['token'],
        'email': "imsuperfunny@gmail.com"
    }
    response = requests.put(url + 'user/profile/setemail', json = data_in)
    data_in = {
        'token': payload['token'],
        'email': "waitimmachangethisagain@gmail.com"
    }
    response = requests.put(url + 'user/profile/setemail', json = data_in)
    data_in = {
        'token': payload['token'],
        'email': "last1iswear@gmail.com"
    }
    response = requests.put(url + 'user/profile/setemail', json = data_in)
    # check user profile
    data_in = {
        'token': payload['token'],
        'u_id': payload['u_id']
    }
    response = requests.get(url + 'user/profile', data_in)
    profile = response.json()
    assert(profile["user"]["email"] == "last1iswear@gmail.com")
    
    requests.delete(url + 'clear')

def test_invalid_regex_email_1_http(url):
    requests.delete(url + 'clear')
    # register user
    data_in = {
        'email' : "example@gmail.com", 
        'password' : "password",
        'name_first' : "First",
        'name_last' : "Last"
    }
    response = requests.post(url + 'auth/register', json = data_in)
    assert (response.status_code == 200)
    payload = response.json()
    # change user email
    data_in = {
        'token': payload['token'],
        'email': "examplegmail.com"
    }
    response = requests.put(url + 'user/profile/setemail', json = data_in)
    assert (response.status_code == 400)
    requests.delete(url + 'clear')

def test_invalid_regex_email_2_http(url):
    requests.delete(url + 'clear')
    # register user
    data_in = {
        'email' : "example@gmail.com", 
        'password' : "password",
        'name_first' : "First",
        'name_last' : "Last"
    }
    response = requests.post(url + 'auth/register', json = data_in)
    assert (response.status_code == 200)
    payload = response.json()
    # change user email
    data_in = {
        'token': payload['token'],
        'email': "e@gmail.community"
    }
    response = requests.put(url + 'user/profile/setemail', json = data_in)
    assert (response.status_code == 400)
    requests.delete(url + 'clear')

def test_invalid_regex_email_3_http(url):
    requests.delete(url + 'clear')
    # register user
    data_in = {
        'email' : "example@gmail.com", 
        'password' : "password",
        'name_first' : "First",
        'name_last' : "Last"
    }
    response = requests.post(url + 'auth/register', json = data_in)
    assert (response.status_code == 200)
    payload = response.json()
    # change user email
    data_in = {
        'token': payload['token'],
        'email': "e@m@gmail.com"
    }
    response = requests.put(url + 'user/profile/setemail', json = data_in)
    assert (response.status_code == 400)
    requests.delete(url + 'clear')

def test_no_email_http(url):
    requests.delete(url + 'clear')
    # register user
    data_in = {
        'email' : "example@gmail.com", 
        'password' : "password",
        'name_first' : "First",
        'name_last' : "Last"
    }
    response = requests.post(url + 'auth/register', json = data_in)
    assert (response.status_code == 200)
    payload = response.json()
    # change user email
    data_in = {
        'token': payload['token'],
        'email': ""
    }
    response = requests.put(url + 'user/profile/setemail', json = data_in)
    assert (response.status_code == 400)
    requests.delete(url + 'clear')

def test_taken_email_http(url):
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
    # attempt to change user email
    data_in = {
        'token': user2['token'],
        'email': 'kellyzhou@gmail.com'
    }
    response = requests.put(url + 'user/profile/setemail', json = data_in)
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
    # change user email
    data_in = {
        'token': 'badtoken',
        'email': 'validemail@gmail.com'
    }
    response = requests.put(url + 'user/profile/setemail', json = data_in)
    assert (response.status_code == 400)
    requests.delete(url + 'clear')