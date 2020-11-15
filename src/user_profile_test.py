import pytest
from auth import auth_register
from user import user_profile
from other import clear
from error import InputError, AccessError

def test_valid_user():
    clear()
    user_details = auth_register("kellyczhou@gmail.com", "cats<3", "Kelly", "Zhou")
    profile = user_profile(user_details['token'], user_details['u_id'])
    correct_profile = {"user": {"u_id": user_details['u_id'], "email": "kellyczhou@gmail.com", \
        "name_first": "Kelly", "name_last": "Zhou", "handle_str": "kellyzhou"}}
    assert(profile == correct_profile)
    clear()

def test_valid_users():
    clear()
    user1 = auth_register("cyruschow@gmail.com", "ilikecookies", "Cyrus", "Chow")
    auth_register("kellyzhou@gmail.com", "pink=bestcolour", "Kelly", "Zhou")
    user2 = auth_register("andreeavissarion@hotmail.com", "coolestshoes!!", "Andreea", "Vissarion")
    auth_register("joshualee@icloud.org", "randypopping", "Josh", "Lee")
    auth_register("nickdodd@gmail.com", "doddthegod", "Nick", "Dodd")
    profile1 = user_profile(user1['token'], user1['u_id'])
    profile2 = user_profile(user2['token'], user2['u_id'])
    correct_profile1 = {"user": {"u_id" : user1['u_id'], "email" : "cyruschow@gmail.com", \
        "name_first": "Cyrus", "name_last": "Chow", "handle_str": "cyruschow"}}
    correct_profile2 = {"user": {"u_id" : user2['u_id'], "email" : "andreeavissarion@hotmail.com", \
        "name_first": "Andreea", "name_last": "Vissarion", "handle_str": "andreeavissarion"}}
    assert(profile1 == correct_profile1)
    assert(profile2 == correct_profile2)
    clear()

def test_invalid_u_id():
    clear()
    token = auth_register("kellyczhou@gmail.com", "cats<3", "Kelly", "Zhou")['token']
    with pytest.raises(InputError):
        user_profile(token, 404)
    clear()

def test_invalid_token():
    clear()
    user_details = auth_register("kellyczhou@gmail.com", "cats<3", "Kelly", "Zhou")
    with pytest.raises(AccessError):
        user_profile('badtoken', user_details['u_id'])
    clear()

# user: Dictionary containing u_id, email, name_first, name_last, handle_str