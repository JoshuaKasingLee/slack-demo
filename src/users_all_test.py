import pytest
from other import users_all, clear
import auth
from error import AccessError

def test_one() :
    clear()
    user = auth.auth_register("jonathon@gmail.com", "password", "John", "Smith")
    token = user['token']
    u_id = user['u_id']
    assert users_all(token) == {
        'users': [
            {
                'u_id': u_id,
                'email': 'jonathon@gmail.com',
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
                'handle_str': 'haydenjacobs',
            },
        ],
    }
    clear()
    
def test_two() :
    clear()
    user = auth.auth_register("jonathon@gmail.com", "password", "John", "Smith")
    token = user['token']
    u_id = user['u_id']
    user_2 = auth.auth_register("sallychampion@gmail.com", "password", "Sally", "Champion") 
    u_id2 = user_2['u_id']
    assert users_all(token) == {
        'users': [
            {
                'u_id': u_id,
                'email': 'jonathon@gmail.com',
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
                'handle_str': 'haydenjacobs',
            },
            {
                'u_id': u_id2,
                'email': 'sallychampion@gmail.com',
                'name_first': 'Sally',
                'name_last': 'Champion',
                'handle_str': 'sallychampion',
            },
        ],                
    }
    clear()

def test_invalid_token(): # wrong user token - accesserror
    clear()
    auth.auth_register("kellyzhou@gmail.com", "password", "Kelly", "Zhou")
    with pytest.raises(AccessError):
        users_all(4)
    clear()