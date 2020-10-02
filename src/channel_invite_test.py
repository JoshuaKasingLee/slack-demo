from channel_invite import channel_invite
from channel_details import channel_details
import pytest
import database
import auth

def test_add_member():   
    (u_id, token) = auth.auth_register("email@gmail.com", "password", "Andreea", "Vissarion")
    channel_id = 1
    channel_invite(token, channel_id, u_id)  
    (x, y, all_members)  = channel_details(token, channel_id)
    is_in = 0
    for member in all_members:
        if member['u_id'] == u_id:
            is_in = 1
    assert (is_in == 1)
    
