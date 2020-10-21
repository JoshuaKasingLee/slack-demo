import database
from channel import channel_join
from error import InputError
from error import AccessError

def channels_list(token):

    u_id = token_check(token)
    database.channels_user_exist_check(u_id)
    return database.channels_return_membership(u_id)


def channels_listall(token):

    u_id = token_check(token)
    database.channels_user_exist_check(u_id)
    return database.channels_return_all()


def channels_create(token, name, is_public):

    u_id = token_check(token)
    database.channels_user_exist_check(u_id) 
    
    ## check valid name
    if len(name) > 20 or len(name) == 0:
        raise InputError

    channel_id = database.channels_assign_id()
    database.channels_add_to_database(u_id, name, channel_id, is_public)

    ## add creator as owner
    channel_join(token, channel_id)

    return {
        'channel_id': channel_id,
    }


# NON-DATABASE HELPER FUNCTIONS #

def token_check(token):
    ''' check if the token string is a valid integer'''
    try:
        u_id = int(token)
    except:
        raise AccessError #invalid token
    return u_id
