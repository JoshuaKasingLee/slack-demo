from error import InputError, AccessError
import database
import re
import helper
import sys
import urllib.request
from PIL import Image
from auth import auth_register

def user_profile(token, u_id):
    # check if u_id exists in database - if not, return InputError
    found_user = database.check_user_exists(u_id)
    # if u_id exists and input token is valid, return as required
    return {
        'user': {
        	'u_id': found_user["u_id"],
        	'email': found_user["email"],
        	'name_first': found_user["name_first"],
        	'name_last': found_user["name_last"],
        	'handle_str': found_user["handle_str"],
            'profile_img_url': found_user["profile_img_url"]
        }
    }

def user_profile_setname(token, name_first, name_last):
    # check if input token and name lengths are valid
    id = database.token_check(token)
    helper.check_name_length(name_first, name_last)

    # if names are valid, change name in database
    database.update_first_name(id, name_first)
    database.update_last_name(id, name_last)
    return {
    }

def user_profile_setemail(token, email):
    # check if input token and email is valid
    id = database.token_check(token)
    helper.validate_email(email)
    database.auth_check_email_register(email)  

    # update email
    database.update_email(id, email)
    return {
    }

def user_profile_sethandle(token, handle_str):
     # check if input token is valid - if not, return AccessError
    id = database.token_check(token)

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
    database.check_valid_img_url(img_url)
    # download and open the photo locally
    urllib.request.urlretrieve(img_url, "profile_pic.jpg")
    profile_picture = Image.open("profile_pic.jpg")
    # check whether image is a jpg
    database.check_jpg_format(profile_picture.format)
    
    # crop the image
    width, height = profile_picture.size
    database.check_valid_crop_coordinates(x_start, x_end, y_start, y_end, width, height)
    cropped_profile = profile_picture.crop((x_start, y_start, x_end, y_end))

    # save the image
    image_name = str(id) + ".jpg"
    database.check_file_already_exists(image_name)
    cropped_profile.save("src/static/" + image_name)
    database.update_profile_img_url(id, image_name)
    database.update_user_profile_img_url(id, image_name)
    return image_name

