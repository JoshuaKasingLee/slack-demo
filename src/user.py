from error import InputError, AccessError
import database
import re
import helper
import sys
import urllib.request
from PIL import Image

def user_profile(token, u_id):
    # check if u_id exists in database - if not, return InputError
    found_user = database.check_token_u_id_match(token, u_id)
    # if u_id exists and input token is valid, return as required
    return {
        'user': {
        	'u_id': found_user["u_id"],
        	'email': found_user["email"],
        	'name_first': found_user["name_first"],
        	'name_last': found_user["name_last"],
        	'handle_str': found_user["handle_str"]
        }
    }

def user_profile_setname(token, name_first, name_last):
    # check if input token and name lengths are valid
    id = database.return_token_u_id(token)
    helper.check_name_length(name_first, name_last)

    # if names are valid, change name in database
    database.update_first_name(id, name_first)
    database.update_last_name(id, name_last)
    return {
    }

def user_profile_setemail(token, email):
    # check if input token and email is valid
    id = database.return_token_u_id(token)
    helper.validate_email(email)
    database.auth_check_email_register(email)  

    # update email
    database.update_email(id, email)
    return {
    }

def user_profile_sethandle(token, handle_str):
     # check if input token is valid - if not, return AccessError
    id = database.return_token_u_id(token)

    # check whether handle is too long or short
    helper.check_handle_length(handle_str)
    
    # check whether handle has been taken
    database.check_handle(handle_str)

    # update handle
    database.update_handle(id, handle_str)

    return {
    }

# saves photo to local server and crops it
# see server.py for serving the image
def user_profile_uploadphoto(token, img_url, x_start, y_start, x_end, y_end):
    # check whether token is valid
    id = database.return_token_u_id(token)
    # check whether img_url is valid
    try:
        response = urllib.request.urlopen(img_url)
    except:
        raise InputError("Image URL is invalid")
    # download the photo locally
    urllib.request.urlretrieve(img_url, "profile_pic")
    # open the image
    profile_picture = Image.open("profile_pic")
    # check whether image is a jpg
    image_type = profile_picture.format
    print(image_type)
    if image_type != "JPEG":
        raise InputError("Image is not of JPEG type")
    # check for crop co-ordinate errors
    if x_start > x_end or y_start > y_end:
        raise InputError("Crop co-ordinates must be directed from upper left to lower right")
    width, height = profile_picture.size
    print(width, height)
    if x_start > width or x_start < 0 or x_end > width or x_end < 0:
        raise InputError("x crop co-ordinates are not within image range")
    if y_start > height or y_start < 0 or y_end > height or y_end < 0:
        raise InputError("y crop co-ordinates are not within image range")
    # crop and save the image
    cropped_profile = profile_picture.crop((x_start, y_start, x_end, y_end))
    cropped_profile.save("profile_pic.jpg")
    return {}

#user_profile_uploadphoto("x", "https://www.ikea.com/au/en/images/products/smycka-artificial-flower-rose-pink__0902935_PE596772_S5.JPG?f=xl", 1, 1, 100, 100)
#user_profile_uploadphoto("x", "http://invalidurl", 1, 2, 2, 2)
#user_profile_uploadphoto("x", "http://www.pngall.com/wp-content/uploads/2016/06/Light-Free-Download-PNG.png", 1, 1, 100, 100)