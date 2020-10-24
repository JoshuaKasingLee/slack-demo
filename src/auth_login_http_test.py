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

# Testing an undefined user
def test_invalid_user_http(url):
    requests.delete(url + 'clear')
    data_in = {
        'email' : "randomemail@gmail.com",
        'password' : "123456"
    }
    response = requests.post(url + 'auth/login', json = data_in)
    assert (response.status_code == 400)
    requests.delete(url + 'clear')

# Testing invalid password
def test_invalid_password_http(url):
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
        'password' : "wrongpassword"
    }
    response = requests.post(url + 'auth/login', json = data_in)
    assert (response.status_code == 400)
    requests.delete(url + 'clear')

# Testing successful login attempt !!
def test_login_success_http(url):
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
    requests.delete(url + 'clear')

# Testing that email has not been registered
def test_unregistered(url):
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
    # register another user
    data_in = {
        'email' : "testmail2@gmail.com",
        'password' : "password",
        'name_first' : "John",
        'name_last' : "Smith"
    }
    response = requests.post(url + 'auth/register', json = data_in)
    assert (response.status_code == 200)
    # log another user in
    data_in = {
        'email' : "testmail3@gmail.com",
        'password' : "password"
    }
    response = requests.post(url + 'auth/login', json = data_in)
    assert (response.status_code == 400)
    requests.delete(url + 'clear')


# Testing double login works
def test_login_twice_http(url):
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
    # log the user in again
    data_in = {
        'email' : "testmail@gmail.com",
        'password' : "password"
    }
    response = requests.post(url + 'auth/login', json = data_in)
    assert (response.status_code == 200)
    requests.delete(url + 'clear')