import pytest
import re
from subprocess import Popen, PIPE
import signal
from time import sleep
import requests

data_in_1 = {
        'email' : "jonathon@gmail.com",
        'password' : "password",
        'name_first' : "John",
        'name_last' : "Smith"
    }

data_in_2 = {
        'email' : "sallychampion@gmail.com",
        'password' : "password",
        'name_first' : "Sally",
        'name_last' : "Champion"
    }

data_in_3 = {
        'email' : "janedoe@gmail.com",
        'password' : "password",
        'name_first' : "Jane",
        'name_last' : "Doe"
    }

token = {}

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
    
def test_not_admin(url) :
    requests.delete(url + 'clear')
    response = requests.post(url + 'auth/register', json = data_in_1)
    payload = response.json()
    token['token'] = payload['token']
    response = requests.post(url + 'auth/register', json = data_in_2)
    payload = response.json()
    token['token_2'] = payload['token']
    data_in = {
        'token' : token['token'],
        'name' : "Channel1",
        'is_public' : False
    }
    response = requests.post(url + 'channels/create', json = data_in)
    channel_id = response.json()['channel_id']
    data_in = {
        'token' : token['token_2'],
        'channel_id' : channel_id,
    }
    response = requests.post(url + 'channel/join', json = data_in)
    assert (response.status_code == 400)
    requests.delete(url + 'clear')

def test_make_admin(url) :
    requests.delete(url + 'clear')
    response = requests.post(url + 'auth/register', json = data_in_1)
    payload = response.json()
    token['token'] = payload['token']
    response = requests.post(url + 'auth/register', json = data_in_2)
    payload = response.json()
    u_id_2 = payload['u_id']
    token['token_2'] = payload['token']
    data_in = {
        'token' : token['token'],
        'name' : "Channel1",
        'is_public' : False
    }
    response = requests.post(url + 'channels/create', json = data_in)
    channel_id = response.json()['channel_id']
    data_in = {
        'token' : token['token'],
        'u_id' : u_id_2,
        'permission_id' : 1
    }    
    response = requests.post(url + 'admin/userpermission/change', json = data_in)
    data_in = {
        'token' : token['token_2'],
        'channel_id' : channel_id,
    }
    response = requests.post(url + 'channel/join', json = data_in)
    payload = response.json()
    assert(payload == {} ) # doesn't 404 error
    requests.delete(url + 'clear')

def test_remove_admin(url) :
    requests.delete(url + 'clear')
    response = requests.post(url + 'auth/register', json = data_in_1)
    payload = response.json()
    token['token'] = payload['token']
    response = requests.post(url + 'auth/register', json = data_in_2)
    payload = response.json()
    u_id_2 = payload['u_id']
    token['token_2'] = payload['token']
    data_in = {
        'token' : token['token'],
        'u_id' : u_id_2,
        'permission_id' : 1
    }    
    response = requests.post(url + 'admin/userpermission/change', json = data_in)   
    data_in = {
        'token' : token['token'],
        'u_id' : u_id_2,
        'permission_id' : 2
    }    
    response = requests.post(url + 'admin/userpermission/change', json = data_in)  
    data_in = {
        'token' : token['token'],
        'name' : "Channel1",
        'is_public' : False
    }
    response = requests.post(url + 'channels/create', json = data_in)
    channel_id = response.json()['channel_id']
    data_in = {
        'token' : token['token_2'],
        'channel_id' : channel_id,
    }
    response = requests.post(url + 'channel/join', json = data_in)
    assert (response.status_code == 400)
    requests.delete(url + 'clear')  
    
def test_invalid_permission_id(url) :
    requests.delete(url + 'clear')
    response = requests.post(url + 'auth/register', json = data_in_1)
    payload = response.json()
    token['token'] = payload['token']
    response = requests.post(url + 'auth/register', json = data_in_2)
    payload = response.json()
    u_id_2 = payload['u_id']
    token['token_2'] = payload['token']
    data_in = {
        'token' : token['token'],
        'u_id' : u_id_2,
        'permission_id' : 4
    }    
    response = requests.post(url + 'admin/userpermission/change', json = data_in)
    assert (response.status_code == 400)
    requests.delete(url + 'clear')  
    
def test_invalid_u_id(url) :
    requests.delete(url + 'clear')
    response = requests.post(url + 'auth/register', json = data_in_1)
    payload = response.json()
    token['token'] = payload['token']
    response = requests.post(url + 'auth/register', json = data_in_2)
    payload = response.json()
    token['token_2'] = payload['token']
    data_in = {
        'token' : token['token'],
        'u_id' : 100,
        'permission_id' : 1
    }    
    response = requests.post(url + 'admin/userpermission/change', json = data_in)
    assert (response.status_code == 400)
    requests.delete(url + 'clear')  

def test_not_admin_not_owner(url) :   
    requests.delete(url + 'clear')
    response = requests.post(url + 'auth/register', json = data_in_1)
    payload = response.json()
    token['token'] = payload['token']
    response = requests.post(url + 'auth/register', json = data_in_2)
    payload = response.json()
    token['token_2'] = payload['token']  
    response = requests.post(url + 'auth/register', json = data_in_3)
    payload = response.json()
    u_id_3 = payload['u_id']  
    data_in = {
        'token' : token['token_2'],
        'u_id' : u_id_3,
        'permission_id' : 1
    }    
    response = requests.post(url + 'admin/userpermission/change', json = data_in)
    assert (response.status_code == 400)
    requests.delete(url + 'clear')  
    

def test_admin_but_not_owner(url) :
    requests.delete(url + 'clear')
    response = requests.post(url + 'auth/register', json = data_in_1)
    payload = response.json()
    token['token'] = payload['token']
    response = requests.post(url + 'auth/register', json = data_in_2)
    payload = response.json()
    u_id_2 = payload['u_id']
    token['token_2'] = payload['token']  
    data_in = {
        'token' : token['token'],
        'u_id' : u_id_2,
        'permission_id' : 1
    }    
    response = requests.post(url + 'admin/userpermission/change', json = data_in)
    response = requests.post(url + 'auth/register', json = data_in_3)
    payload = response.json()
    u_id_3 = payload['u_id']  
    data_in = {
        'token' : token['token_2'],
        'u_id' : u_id_3,
        'permission_id' : 1
    }    
    response = requests.post(url + 'admin/userpermission/change', json = data_in)
    assert (response.status_code == 400)
    requests.delete(url + 'clear')
