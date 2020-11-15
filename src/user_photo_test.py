import pytest
from auth import auth_register
from user import user_profile
from other import clear
from error import InputError, AccessError
from user import user_profile_uploadphoto

# check for when img_url returns an HTTP status other than 200
def test_invalid_url_1():
    clear()
    user_details = auth_register("kellyczhou@gmail.com", "cats<3", "Kelly", "Zhou")
    pic = "invalidurl"
    with pytest.raises(InputError):
        user_profile_uploadphoto(user_details['token'], pic, 1, 1, 100, 100)
    clear()

def test_invalid_url_2():
    clear()
    user_details = auth_register("kellyczhou@gmail.com", "cats<3", "Kelly", "Zhou")
    pic = "http://invalidurl.com"
    with pytest.raises(InputError):
        user_profile_uploadphoto(user_details['token'], pic, 1, 1, 100, 100)
    clear()

# check for non-jpeg images
def test_invalid_image_1():
    clear()
    user_details = auth_register("kellyczhou@gmail.com", "cats<3", "Kelly", "Zhou")
    pic = "http://www.pngall.com/wp-content/uploads/2016/06/Light-Free-Download-PNG.png"
    with pytest.raises(InputError):
        user_profile_uploadphoto(user_details['token'], pic, 1, 1, 100, 100)
    clear()

# check for invalid crop co-ordinates
# using this image: https://www.ikea.com/au/en/images/products/smycka-artificial-flower-rose-pink__0902935_PE596772_S5.JPG?f=xl
# image has dimensions (900, 900)

def test_invalid_coordinates_1(): # negative co-ordinates
    clear()
    user_details = auth_register("kellyczhou@gmail.com", "cats<3", "Kelly", "Zhou")
    pic = "https://www.ikea.com/au/en/images/products/smycka-artificial-flower-rose-pink__0902935_PE596772_S5.JPG?f=xl"
    with pytest.raises(InputError):
        user_profile_uploadphoto(user_details['token'], pic, -100, -100, 100, 100)
    clear()

def test_invalid_coordinates_2(): # negative co-ordinates
    clear()
    user_details = auth_register("kellyczhou@gmail.com", "cats<3", "Kelly", "Zhou")
    pic = "https://www.ikea.com/au/en/images/products/smycka-artificial-flower-rose-pink__0902935_PE596772_S5.JPG?f=xl"
    with pytest.raises(InputError):
        user_profile_uploadphoto(user_details['token'], pic, -100, -100, -5, -5)
    clear()

def test_invalid_coordinates_3(): # start co-ordinates larger end co-ordinates
    clear()
    user_details = auth_register("kellyczhou@gmail.com", "cats<3", "Kelly", "Zhou")
    pic = "https://www.ikea.com/au/en/images/products/smycka-artificial-flower-rose-pink__0902935_PE596772_S5.JPG?f=xl"
    with pytest.raises(InputError):
        user_profile_uploadphoto(user_details['token'], pic, 900, 900, 0, 0)
    clear()

def test_invalid_coordinates_4(): # co-ordinates out of range
    clear()
    user_details = auth_register("kellyczhou@gmail.com", "cats<3", "Kelly", "Zhou")
    pic = "https://www.ikea.com/au/en/images/products/smycka-artificial-flower-rose-pink__0902935_PE596772_S5.JPG?f=xl"
    with pytest.raises(InputError):
        user_profile_uploadphoto(user_details['token'], pic, 100, 100, 1000, 1000)
    clear()

# check for invalid token
def test_invalid_token():
    clear()
    auth_register("kellyczhou@gmail.com", "cats<3", "Kelly", "Zhou")
    pic = "https://www.ikea.com/au/en/images/products/smycka-artificial-flower-rose-pink__0902935_PE596772_S5.JPG?f=xl"
    with pytest.raises(AccessError):
        user_profile_uploadphoto("badtoken", pic, 100, 100, 800, 800)
    clear()
