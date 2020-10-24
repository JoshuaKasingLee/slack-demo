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

# test whether input error is raised when email is invalid
def test_email_invalid_1_http(url):
    requests.delete(url + 'clear')
    data_in = {
        'email' : "email",  # no ampersand or dot
        'password' : "password",
        'name_first' : "first",
        'name_last' : "last"
    }
    response = requests.post(url + 'auth/register', json = data_in)
    assert (response.status_code == 400)
    requests.delete(url + 'clear')

def test_email_invalid_2_http(url):
    requests.delete(url + 'clear')
    data_in = {
        'email' : "email.com",  # no ampersand
        'password' : "password",
        'name_first' : "first",
        'name_last' : "last"
    }
    response = requests.post(url + 'auth/register', json = data_in)
    assert (response.status_code == 400)
    requests.delete(url + 'clear')

def test_email_invalid_3_http(url):
    requests.delete(url + 'clear')
    data_in = {
        'email' : "email@gmail.organisation",  # ending too long
        'password' : "password",
        'name_first' : "first",
        'name_last' : "last"
    }
    response = requests.post(url + 'auth/register', json = data_in)
    assert (response.status_code == 400)
    requests.delete(url + 'clear')

def test_email_invalid_4_http(url):
    requests.delete(url + 'clear')
    data_in = {
        'email' : "email@gmail@organisation.com",  # two ampersands
        'password' : "password",
        'name_first' : "first",
        'name_last' : "last"
    }
    response = requests.post(url + 'auth/register', json = data_in)
    assert (response.status_code == 400)
    requests.delete(url + 'clear')

def test_email_invalid_5_http(url):
    requests.delete(url + 'clear')
    data_in = {
        'email' : "email@gmail.com.org",  # two dots after ampersand
        'password' : "password",
        'name_first' : "first",
        'name_last' : "last"
    }
    response = requests.post(url + 'auth/register', json = data_in)
    assert (response.status_code == 400)
    requests.delete(url + 'clear')

def test_email_invalid_6_http(url):
    requests.delete(url + 'clear')
    data_in = {
        'email' : "EMAIL@GMAIL.COM",  # capitals
        'password' : "password",
        'name_first' : "first",
        'name_last' : "last"
    }
    response = requests.post(url + 'auth/register', json = data_in)
    assert (response.status_code == 400)
    requests.delete(url + 'clear')

# test whether input error is thrown when registering with an already registered email
def test_email_taken_1_http(url):
    requests.delete(url + 'clear')
    data_in = {
        'email' : "icecreamisyummy@gmail.com",
        'password' : "frozen",
        'name_first' : "Ice",
        'name_last' : "Cream"
    }
    response = requests.post(url + 'auth/register', json = data_in)
    data_in = {
        'email' : "icecreamisyummy@gmail.com",
        'password' : "milkduds",
        'name_first' : "Icy",
        'name_last' : "Poles"
    }
    response = requests.post(url + 'auth/register', json = data_in)
    assert (response.status_code == 400)
    requests.delete(url + 'clear')

def test_email_taken_2_http(url):
    requests.delete(url + 'clear')
    # register the user
    data_in = {
        'email' : "ilikesummer@gmail.com",
        'password' : "bestseason",
        'name_first' : "Summer",
        'name_last' : "Days"
    }
    response = requests.post(url + 'auth/register', json = data_in)
    payload = response.json()
    # log the user out
    data_in = {'token': payload['token']}
    response = requests.post(url + 'auth/logout', json = data_in)
    payload = response.json()
    assert(payload == {"is_success": True})
    # register another user with same email
    data_in = {
        'email' : "ilikesummer@gmail.com",
        'password' : "bestseason",
        'name_first' : "Summer",
        'name_last' : "Days"
    }
    response = requests.post(url + 'auth/register', json = data_in)
    assert (response.status_code == 400)
    requests.delete(url + 'clear')

# test whether input error is raised when password is < 6 characters
def test_password_short_1_http(url):
    requests.delete(url + 'clear')
    data_in = {
        'email' : "email@gmail.com", 
        'password' : "cat",
        'name_first' : "first",
        'name_last' : "last"
    }
    response = requests.post(url + 'auth/register', json = data_in)
    assert (response.status_code == 400)
    requests.delete(url + 'clear')

def test_password_short_2_http(url):
    requests.delete(url + 'clear')
    data_in = {
        'email' : "email@gmail.com", 
        'password' : "short",
        'name_first' : "first",
        'name_last' : "last"
    }
    response = requests.post(url + 'auth/register', json = data_in)
    assert (response.status_code == 400)
    requests.delete(url + 'clear')

def test_password_short_3_http(url):
    requests.delete(url + 'clear')
    data_in = {
        'email' : "email@gmail.com", 
        'password' : "a",
        'name_first' : "first",
        'name_last' : "last"
    }
    response = requests.post(url + 'auth/register', json = data_in)
    assert (response.status_code == 400)
    requests.delete(url + 'clear')

# test whether input error is raised when first name is < 1 character
def test_first_name_short_http(url):
    requests.delete(url + 'clear')
    data_in = {
        'email' : "email@gmail.com", 
        'password' : "password",
        'name_first' : "",
        'name_last' : "last"
    }
    response = requests.post(url + 'auth/register', json = data_in)
    assert (response.status_code == 400)
    requests.delete(url + 'clear')

# test whether input error is raised when last name is < 1 character
def test_last_name_short_http(url):
    requests.delete(url + 'clear')
    data_in = {
        'email' : "email@gmail.com", 
        'password' : "password",
        'name_first' : "first",
        'name_last' : ""
    }
    response = requests.post(url + 'auth/register', json = data_in)
    assert (response.status_code == 400)
    requests.delete(url + 'clear')

# test whether input error is raised when first name is > 50 characters
def test_first_name_long_1_http(url): # very long name
    requests.delete(url + 'clear')
    data_in = {
        'email' : "email@gmail.com", 
        'password' : "password",
        'name_first' : "extremelylongfirstnamebecauseiamsuperdupertroopercool",
        'name_last' : "last"
    }
    response = requests.post(url + 'auth/register', json = data_in)
    assert (response.status_code == 400)
    requests.delete(url + 'clear')

def test_first_name_long_2_http(url): # only characters
    requests.delete(url + 'clear')
    data_in = {
        'email' : "email@gmail.com", 
        'password' : "password",
        'name_first' : ".....................................................",
        'name_last' : "last"
    }
    response = requests.post(url + 'auth/register', json = data_in)
    assert (response.status_code == 400)
    requests.delete(url + 'clear')

def test_first_name_long_3_http(url): # name with spaces
    requests.delete(url + 'clear')
    data_in = {
        'email' : "email@gmail.com", 
        'password' : "password",
        'name_first' : "Adolph Blaine Charles David Earl Frederick Gerald Hubert",
        'name_last' : "last"
    }
    response = requests.post(url + 'auth/register', json = data_in)
    assert (response.status_code == 400)
    requests.delete(url + 'clear')

# test whether input error is raised when last name is > 50 characters
def test_last_name_long_http(url):
    requests.delete(url + 'clear')
    data_in = {
        'email' : "email@gmail.com", 
        'password' : "password",
        'name_first' : "first",
        'name_last' : "extremelylonglastnamebecauseiamsuperdupertroopercool"
    }
    response = requests.post(url + 'auth/register', json = data_in)
    assert (response.status_code == 400)
    requests.delete(url + 'clear')


# # 2. TEST OUTPUT

# test valid registrations are successful
def test_valid_rego_http(url):
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
    payload = response.json()
    u_id1 = payload['u_id']
    # register user 2
    data_in = {
        'email' : "kellyzhou@gmail.com", 
        'password' : "pink=bestcolour",
        'name_first' : "Kelly",
        'name_last' : "Zhou"
    }
    response = requests.post(url + 'auth/register', json = data_in)
    assert (response.status_code == 200)
    payload = response.json()
    u_id2 = payload['u_id']
    # register user 3
    data_in = {
        'email' : "andreeavissarion@hotmail.com", 
        'password' : "coolestshoes!!",
        'name_first' : "Andreea",
        'name_last' : "Vissarion"
    }
    response = requests.post(url + 'auth/register', json = data_in)
    assert (response.status_code == 200)
    payload = response.json()
    u_id3 = payload['u_id']
    # register user 4
    data_in = {
        'email' : "joshualee@icloud.org", 
        'password' : "randypopping",
        'name_first' : "Josh",
        'name_last' : "Lee"
    }
    response = requests.post(url + 'auth/register', json = data_in)
    assert (response.status_code == 200)
    payload = response.json()
    u_id4 = payload['u_id']
    # register user 5
    data_in = {
        'email' : "nickdodd@gmail.com", 
        'password' : "doddthegod",
        'name_first' : "Nick",
        'name_last' : "Dodd"
    }
    response = requests.post(url + 'auth/register', json = data_in)
    assert (response.status_code == 200)
    payload = response.json()
    u_id5 = payload['u_id']
    data_in = {'token': payload['token']}
    response = requests.get(url + 'users/all', data_in)
    payload = response.json()
    assert payload == {
        'users': [
            {
                'u_id': u_id1,
                'email' : "cyruschow@gmail.com", 
                'name_first' : "Cyrus",
                'name_last' : "Chow",
                'handle_str': "cyruschow"
            },
            {
                'u_id': u_id2,
                'email' : "kellyzhou@gmail.com", 
                'name_first' : "Kelly",
                'name_last' : "Zhou",
                'handle_str': "kellyzhou"
            },
            {
                'u_id': u_id3,
                'email' : "andreeavissarion@hotmail.com", 
                'name_first' : "Andreea",
                'name_last' : "Vissarion",
                'handle_str': "andreeavissarion"
            },
            {
                'u_id': u_id4,
                'email' : "joshualee@icloud.org", 
                'name_first' : "Josh",
                'name_last' : "Lee",
                'handle_str': "joshlee"
            },
            {
                'u_id': u_id5,
                'email' : "nickdodd@gmail.com", 
                'name_first' : "Nick",
                'name_last' : "Dodd",
                'handle_str': "nickdodd"
            }
        ],                
    }
    requests.delete(url + 'clear')

# test whether unique ids are generated
def test_unique_u_id_http(url):
    requests.delete(url + 'clear')
    # register user 1
    data_in = {
        'email' : "sallysmith@gmail.com", 
        'password' : "ilikecats",
        'name_first' : "Sally",
        'name_last' : "Smith"
    }
    response = requests.post(url + 'auth/register', json = data_in)
    assert (response.status_code == 200)
    payload = response.json()
    u_id1 = payload['u_id']
    # register user 2
    data_in = {
        'email' : "bobbybrown@gmail.com", 
        'password' : "ilikedogs",
        'name_first' : "Bobby",
        'name_last' : "Brown"
    }
    response = requests.post(url + 'auth/register', json = data_in)
    assert (response.status_code == 200)
    payload = response.json()
    u_id2 = payload['u_id']
    # register user 3
    data_in = {
        'email' : "janedoe@gmail.com", 
        'password' : "plainjane",
        'name_first' : "Jane",
        'name_last' : "Doe"
    }
    response = requests.post(url + 'auth/register', json = data_in)
    assert (response.status_code == 200)
    payload = response.json()
    u_id3 = payload['u_id']
    # check u_ids generated are different
    assert(u_id1 != u_id2)
    assert(u_id1 != u_id3)
    assert(u_id2 != u_id3)
    requests.delete(url + 'clear')

# test whether registered user can log in and logout
def test_registered_login_http(url):
    requests.delete(url + 'clear')
    # register a user
    data_in = {
        'email' : "email@gmail.com", 
        'password' : "password",
        'name_first' : "first",
        'name_last' : "last"
    }
    response = requests.post(url + 'auth/register', json = data_in)
    assert (response.status_code == 200)
    # ensure user can log in
    data_in = {
        'email' : "email@gmail.com", 
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

