import pytest
import database
import other
from channel_addowner import channel_addowner
from channel_join import channel_join
import channels
import auth
from error import InputError
from error import AccessError

#need to test a few things: 
# valid channel (input error), u_id is already owner (input error). 
# access error if token is not global owner OR owner of channel
# regular testing: token is owner AND, u_id is not part of channel at all. case 2: token is owner AND u_id is already regular member

def test_valid_channel() :
    (u_id, token) = auth.auth_register("email@gmail.com", "password", "Joshua", "Lee")
    channel_id = 999
    with pytest.raises(InputError) as e:
        channel_addowner(token, channel_id, u_id)
    other.clear()

def test_already_channel_owner() :
    (u_id, token) = auth.auth_register("email@gmail.com", "password", "Joshua", "Lee")
    channel_id = channels.channels_create(token, "Channel1", True)
    with pytest.raises(InputError) as e:
        channel_addowner(token, channel_id, u_id)
    other.clear()

def test_not_global_or_local_owner() :
    (u_id, token) = auth.auth_register("email@gmail.com", "password", "Joshua", "Lee")
    (u_id_2 token_2) = auth.auth_register("email2@gmail.com", "password2", "Kelly", "Zhou")   
    channel_id = channels.channels_create(token, "Channel1", True)
    with pytest.raises(AccessError) as e:
        channel_addowner(token_2, channel_id, u_id)
    other.clear()   

def test_global_but_not_local_owner() :
    (u_id, token) = auth.auth_register("email@gmail.com", "password", "Joshua", "Lee")
    (u_id_2 token_2) = auth.auth_register("email2@gmail.com", "password2", "Kelly", "Zhou")   
    channel_id = channels.channels_create(token_2, "Channel1", True)
    assert channel_addowner(token_1, channel_id, u_id)
    other.clear()   

def test_promote() :
    (u_id, token) = auth.auth_register("email@gmail.com", "password", "Joshua", "Lee")
    (u_id_2 token_2) = auth.auth_register("email2@gmail.com", "password2", "Kelly", "Zhou") 
    channel_id = channels.channels_create(token, "Channel1", True)
    channel_join(token_2, channel_id)
    assert channel_addowner(token_1, channel_id, u_id_2)
    other.clear()