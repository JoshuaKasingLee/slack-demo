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

# test input errors
# check for when img_url returns an HTTP status other than 200

def test_invalid_url_1_http(url):
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
    # get user information
    user_details = response.json()
    # upload photo
    pic = "invalidurl"
    data_in = {
        'token': user_details['token'],
        'img_url': pic,
        'x_start': 1,
        'y_start': 1,
        'x_end': 100,
        'y_end': 100
    }
    response = requests.post(url + 'user/profile/uploadphoto', json = data_in)
    assert (response.status_code == 400)
    requests.delete(url + 'clear')
    

def test_invalid_url_2_http(url):
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
    # get user information
    user_details = response.json()
    # upload photo
    pic = "http://invalidurl.com"
    data_in = {
        'token': user_details['token'],
        'img_url': pic,
        'x_start': 1,
        'y_start': 1,
        'x_end': 100,
        'y_end': 100
    }
    response = requests.post(url + 'user/profile/uploadphoto', json = data_in)
    assert (response.status_code == 400)
    requests.delete(url + 'clear')

# check for non-jpeg images
def test_invalid_image_1_http(url):
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
    # get user information
    user_details = response.json()
    # upload photo
    pic = "http://www.pngall.com/wp-content/uploads/2016/06/Light-Free-Download-PNG.png"
    data_in = {
        'token': user_details['token'],
        'img_url': pic,
        'x_start': 1,
        'y_start': 1,
        'x_end': 100,
        'y_end': 100
    }
    response = requests.post(url + 'user/profile/uploadphoto', json = data_in)
    assert (response.status_code == 400)
    requests.delete(url + 'clear')
    

# check for invalid crop co-ordinates
# using this image: https://www.ikea.com/au/en/images/products/smycka-artificial-flower-rose-pink__0902935_PE596772_S5.JPG?f=xl
# image has dimensions (900, 900)

def test_invalid_coordinates_1_http(url): # negative co-ordinates
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
    # get user information
    user_details = response.json()
    # upload photo
    pic = "https://www.ikea.com/au/en/images/products/smycka-artificial-flower-rose-pink__0902935_PE596772_S5.JPG?f=xl"
    data_in = {
        'token': user_details['token'],
        'img_url': pic,
        'x_start': -100,
        'y_start': -100,
        'x_end': 100,
        'y_end': 100
    }
    response = requests.post(url + 'user/profile/uploadphoto', json = data_in)
    assert (response.status_code == 400)
    requests.delete(url + 'clear')

def test_invalid_coordinates_2_http(url): # negative co-ordinates
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
    # get user information
    user_details = response.json()
    # upload photo
    pic = "https://www.ikea.com/au/en/images/products/smycka-artificial-flower-rose-pink__0902935_PE596772_S5.JPG?f=xl"
    data_in = {
        'token': user_details['token'],
        'img_url': pic,
        'x_start': -100,
        'y_start': -100,
        'x_end': -5,
        'y_end': -5
    }
    response = requests.post(url + 'user/profile/uploadphoto', json = data_in)
    assert (response.status_code == 400)
    requests.delete(url + 'clear')

def test_invalid_coordinates_3_http(url): # start co-ordinates larger end co-ordinates
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
    # get user information
    user_details = response.json()
    # upload photo
    pic = "https://www.ikea.com/au/en/images/products/smycka-artificial-flower-rose-pink__0902935_PE596772_S5.JPG?f=xl"
    data_in = {
        'token': user_details['token'],
        'img_url': pic,
        'x_start': 900,
        'y_start': 900,
        'x_end': 0,
        'y_end': 0
    }
    response = requests.post(url + 'user/profile/uploadphoto', json = data_in)
    assert (response.status_code == 400)
    requests.delete(url + 'clear')

def test_invalid_coordinates_4_http(url): # co-ordinates out of range
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
    # get user information
    user_details = response.json()
    # upload photo
    pic = "https://www.ikea.com/au/en/images/products/smycka-artificial-flower-rose-pink__0902935_PE596772_S5.JPG?f=xl"
    data_in = {
        'token': user_details['token'],
        'img_url': pic,
        'x_start': 100,
        'y_start': 100,
        'x_end': 1000,
        'y_end': 1000
    }
    response = requests.post(url + 'user/profile/uploadphoto', json = data_in)
    assert (response.status_code == 400)
    requests.delete(url + 'clear')

# check for invalid token
def test_invalid_token_http(url):
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
    # upload photo
    pic = "https://www.ikea.com/au/en/images/products/smycka-artificial-flower-rose-pink__0902935_PE596772_S5.JPG?f=xl"
    data_in = {
        'token': "badtoken",
        'img_url': pic,
        'x_start': 100,
        'y_start': 100,
        'x_end': 800,
        'y_end': 800
    }
    response = requests.post(url + 'user/profile/uploadphoto', json = data_in)
    assert (response.status_code == 400)
    requests.delete(url + 'clear')


# test successful uploads
def test_successful_upload_http(url):
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
    user_details = response.json()
    # upload image
    pic = "https://www.ikea.com/au/en/images/products/smycka-artificial-flower-rose-pink__0902935_PE596772_S5.JPG?f=xl"
    data_in = {
        'token': user_details['token'],
        'img_url': pic,
        'x_start': 0,
        'y_start': 0,
        'x_end': 500,
        'y_end': 500
    }
    response = requests.post(url + 'user/profile/uploadphoto', json = data_in)
    assert (response.status_code == 200)
    payload = response.json()
    assert(payload == {})
    requests.delete(url + 'clear')

def test_successful_uploads_http(url):
    requests.delete(url + 'clear')
    # register users
    data_in = {
        'email' : "sallysmith@gmail.com", 
        'password' : "ilikecats",
        'name_first' : "Sally",
        'name_last' : "Smith"
    }
    response = requests.post(url + 'auth/register', json = data_in)
    assert (response.status_code == 200)
    user1 = response.json()
    data_in = {
        'email' : "bobbybrown@gmail.com", 
        'password' : "ilikedogs",
        'name_first' : "Bobby",
        'name_last' : "Brownn"
    }
    response = requests.post(url + 'auth/register', json = data_in)
    assert (response.status_code == 200)
    user2 = response.json()
    data_in = {
        'email' : "janedoe@gmail.com", 
        'password' : "plainjane",
        'name_first' : "Jane",
        'name_last' : "Doe"
    }
    response = requests.post(url + 'auth/register', json = data_in)
    assert (response.status_code == 200)
    user3 = response.json()
    # upload image
    pic1 = "https://www.ikea.com/au/en/images/products/smycka-artificial-flower-rose-pink__0902935_PE596772_S5.JPG?f=xl"
    pic2 = "https://media1.popsugar-assets.com/files/thumbor/AdWAzZcYorwwjTjy61NV1GvYutQ/fit-in/550x550/filters:format_auto-!!-:strip_icc-!!-/2020/06/03/054/n/1922794/0558421c5ed83df6c616e0.70966458_19_32121_30W/i/Best-Indoor-Flower-Plants-Beginners.jpg"
    pic3 = "https://cdn.shopify.com/s/files/1/1277/9299/products/49d218ea5593ef559e816745480c0f9c89c5dd83_1024x1024.jpg?v=1529903943"
    data_in = {
        'token': user1['token'],
        'img_url': pic1,
        'x_start': 0,
        'y_start': 0,
        'x_end': 500,
        'y_end': 500
    }
    response = requests.post(url + 'user/profile/uploadphoto', json = data_in)
    assert (response.status_code == 200)
    data_in = {
        'token': user2['token'],
        'img_url': pic2,
        'x_start': 0,
        'y_start': 0,
        'x_end': 500,
        'y_end': 500
    }
    response = requests.post(url + 'user/profile/uploadphoto', json = data_in)
    assert (response.status_code == 200)
    data_in = {
        'token': user3['token'],
        'img_url': pic3,
        'x_start': 0,
        'y_start': 0,
        'x_end': 500,
        'y_end': 500
    }
    response = requests.post(url + 'user/profile/uploadphoto', json = data_in)
    assert (response.status_code == 200)
    requests.delete(url + 'clear')

def test_change_profilepic_twice_http(url):
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
    user_details = response.json()
    # upload image
    pic1 = "https://www.ikea.com/au/en/images/products/smycka-artificial-flower-rose-pink__0902935_PE596772_S5.JPG?f=xl"
    data_in = {
        'token': user_details['token'],
        'img_url': pic1,
        'x_start': 0,
        'y_start': 0,
        'x_end': 500,
        'y_end': 500
    }
    response = requests.post(url + 'user/profile/uploadphoto', json = data_in)
    assert (response.status_code == 200)
    # upload another image
    pic2 = "https://media1.popsugar-assets.com/files/thumbor/AdWAzZcYorwwjTjy61NV1GvYutQ/fit-in/550x550/filters:format_auto-!!-:strip_icc-!!-/2020/06/03/054/n/1922794/0558421c5ed83df6c616e0.70966458_19_32121_30W/i/Best-Indoor-Flower-Plants-Beginners.jpg"
    data_in = {
        'token': user_details['token'],
        'img_url': pic2,
        'x_start': 0,
        'y_start': 0,
        'x_end': 300,
        'y_end': 300
    }
    payload = response.json()
    assert(payload == {})
    requests.delete(url + 'clear')
