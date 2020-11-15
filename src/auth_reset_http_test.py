import pytest
import re
from subprocess import Popen, PIPE
import signal
from time import sleep
import requests
import email

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

# def test_password_short_1_http(url):
#     requests.delete(url + 'clear')
#     # register user
#     data_in = {
#         'email' : "cyruschow@gmail.com", 
#         'password' : "ilikecookies",
#         'name_first' : "Cyrus",
#         'name_last' : "Chow"
#     }
#     response = requests.post(url + 'auth/register', json = data_in)
#     assert (response.status_code == 200)
#     # return valid user information
#     payload = response.json()
#     u_id = payload['u_id']
#     token = payload['token']
#     data_in = {
#         'token': token,
#         'u_id': u_id
#     }
#     response = requests.get(url + 'user/profile', data_in)
#     payload = response.json()
#     email = payload['user']['email']
#     # log the user out
#     data_in = {'token': token}
#     response = requests.post(url + 'auth/logout', json = data_in)
#     payload = response.json()
#     assert(payload == {"is_success": True})
#     # attempt to reset password
#     data_in = {'email': email}
#     response = requests.post(url + 'auth/passwordreset/reset', json = data_in)
#     code = response.json()
#     data_in = {
#         'reset_code': code,
#         'new_password': '123'
#     }
#     response = requests.post(url + 'auth/passwordreset/reset', json = data_in)
#     assert (response.status_code == 400)


#     # user = auth_register("cyruschow@gmail.com", "ilikecookies", "Cyrus", "Chow")
#     # profile = user_profile(user['token'], user['u_id'])
#     # auth_logout(user['token'])
#     # code = database.auth_passwordreset_return(profile['user']['email'])
#     # with pytest.raises(InputError):
#     #     auth_passwordreset_reset(code, "123")
#     requests.delete(url + 'clear')

# def test_password_short_2():
#     clear()
#     user = auth_register("joshualee@icloud.org", "randypopping", "Josh", "Lee")
#     profile = user_profile(user['token'], user['u_id'])
#     auth_logout(user['token'])
#     code = database.auth_passwordreset_return(profile['user']['email'])
#     with pytest.raises(InputError):
#         auth_passwordreset_reset(code, "short")
#     clear()

# def test_password_short_3():
#     clear()
#     user = auth_register("nickdodd@gmail.com", "doddthegod", "Nick", "Dodd")
#     profile = user_profile(user['token'], user['u_id'])
#     auth_logout(user['token'])
#     code = database.auth_passwordreset_return(profile['user']['email'])
#     with pytest.raises(InputError):
#         auth_passwordreset_reset(code, "")
#     clear()

def test_password_reset_success_http(url):
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
        'token': payload['token'],
        'u_id': payload['u_id']
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
    # reset password
    data_in = {
        'reset_code': "code",
        'new_password': "password123"
    }
    response = requests.post(url + 'auth/passwordreset/reset', json = data_in)
    assert (response.status_code == 400)
    requests.delete(url + 'clear')

    data_in = {
        'email' : "cyruschow@gmail.com",
        'password' : "password123"
    }
    requests.post(url + 'auth/login', json = data_in)
    requests.delete(url + 'clear')
    # clear()
    
# def test_multiple_reset_success():
#     clear()
#     # register users
#     user1 = auth_register("sallysmith@gmail.com", "ilikecats", "Sally", "Smith")
#     user2 = auth_register("bobbybrown@gmail.com", "ilikedogs", "Bobby", "Brown")
#     user3 = auth_register("janedoe@gmail.com", "plainjane", "Jane", "Doe")
#     # change password
#     profile3 = user_profile(user3['token'], user3['u_id'])
#     auth_logout(user3['token'])
#     code3 = database.auth_passwordreset_return(profile3['user']['email'])
#     auth_passwordreset_reset(code3, "imcool")
#     auth_login("janedoe@gmail.com", "imcool")
#     # with logout
#     profile1 = user_profile(user1['token'], user1['u_id'])
#     auth_logout(user1['token'])
#     code1 = database.auth_passwordreset_return(profile1['user']['email'])
#     auth_passwordreset_reset(code1, "password123")
#     auth_login("sallysmith@gmail.com", "password123")
#     # without logout
#     profile2 = user_profile(user2['token'], user2['u_id'])
#     code2 = database.auth_passwordreset_return(profile2['user']['email'])
#     auth_passwordreset_reset(code2, "bobbyis thebest!")
#     auth_login("bobbybrown@gmail.com", "bobbyis thebest!")
#     # update password again
#     code2 = database.auth_passwordreset_return(profile2['user']['email'])
#     auth_passwordreset_reset(code2, "bobbyis thebestest!")
#     auth_login("bobbybrown@gmail.com", "bobbyis thebestest!")
#     clear()

# def test_reset_correct_password():
#     clear()
#     user1 = auth_register("sallysmith@gmail.com", "ilikecats", "Sally", "Smith")
#     user2 = auth_register("bobbybrown@gmail.com", "ilikedogs", "Bobby", "Brown")
#     profile1 = user_profile(user1['token'], user1['u_id'])
#     auth_logout(user1['token'])
#     code1 = database.auth_passwordreset_return(profile1['user']['email'])
#     auth_passwordreset_reset(code1, "password123")
#     auth_login("sallysmith@gmail.com", "password123")
#     with pytest.raises(InputError):
#         auth_login("bobbybrown@gmail.com", "password123")
#     clear()