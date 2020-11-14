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
    user_details = auth_register("kellyczhou@gmail.com", "cats<3", "Kelly", "Zhou")
    pic = "https://www.ikea.com/au/en/images/products/smycka-artificial-flower-rose-pink__0902935_PE596772_S5.JPG?f=xl"
    with pytest.raises(AccessError):
        user_profile_uploadphoto("badtoken", pic, 100, 100, 800, 800)
    clear()

# test successful uploads
# white box tests - see http tests for blackbox successful upload testing
def test_successful_upload():
    clear()
    user_details = auth_register("kellyczhou@gmail.com", "cats<3", "Kelly", "Zhou")
    pic = "https://www.ikea.com/au/en/images/products/smycka-artificial-flower-rose-pink__0902935_PE596772_S5.JPG?f=xl"
    correct_img = str(user_details['u_id']) + ".jpg"
    assert(user_profile_uploadphoto(user_details['token'], pic, 0, 0, 500, 500) == correct_img)
    clear()

def test_successful_uploads():
    clear()
    user1 = auth_register("sallysmith@gmail.com", "ilikecats", "Sally", "Smith")
    user2 = auth_register("bobbybrown@gmail.com", "ilikedogs", "Bobby", "Brown")
    user3 = auth_register("janedoe@gmail.com", "plainjane", "Jane", "Doe")
    pic1 = "https://www.ikea.com/au/en/images/products/smycka-artificial-flower-rose-pink__0902935_PE596772_S5.JPG?f=xl"
    pic2 = "https://media1.popsugar-assets.com/files/thumbor/AdWAzZcYorwwjTjy61NV1GvYutQ/fit-in/550x550/filters:format_auto-!!-:strip_icc-!!-/2020/06/03/054/n/1922794/0558421c5ed83df6c616e0.70966458_19_32121_30W/i/Best-Indoor-Flower-Plants-Beginners.jpg"
    pic3 = "https://cdn.shopify.com/s/files/1/1277/9299/products/49d218ea5593ef559e816745480c0f9c89c5dd83_1024x1024.jpg?v=1529903943"
    correct_img1 = str(user1['u_id']) + ".jpg"
    correct_img2 = str(user2['u_id']) + ".jpg"
    correct_img3 = str(user3['u_id']) + ".jpg"
    assert(user_profile_uploadphoto(user1['token'], pic1, 0, 0, 500, 500) == correct_img1)
    assert(user_profile_uploadphoto(user2['token'], pic2, 0, 0, 500, 500) == correct_img2)
    assert(user_profile_uploadphoto(user3['token'], pic3, 0, 0, 500, 500) == correct_img3)
    clear()

def test_change_profilepic_twice():
    clear()
    user_details = auth_register("kellyczhou@gmail.com", "cats<3", "Kelly", "Zhou")
    pic = "https://www.ikea.com/au/en/images/products/smycka-artificial-flower-rose-pink__0902935_PE596772_S5.JPG?f=xl"
    correct_img = str(user_details['u_id']) + ".jpg"
    assert(user_profile_uploadphoto(user_details['token'], pic, 0, 0, 500, 500) == correct_img)
    pic = "https://media1.popsugar-assets.com/files/thumbor/AdWAzZcYorwwjTjy61NV1GvYutQ/fit-in/550x550/filters:format_auto-!!-:strip_icc-!!-/2020/06/03/054/n/1922794/0558421c5ed83df6c616e0.70966458_19_32121_30W/i/Best-Indoor-Flower-Plants-Beginners.jpg"
    assert(user_profile_uploadphoto(user_details['token'], pic, 0, 0, 300, 300) == correct_img)
    clear()

