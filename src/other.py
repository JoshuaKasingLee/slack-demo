import database
from error import InputError

def clear():
    database.clear()      
        
def users_all(token):

    database.token_check(token)
    u_id = database.convert_from_tok_to_u_id(token)
    database.channels_user_log_check(u_id)
    
    list_of_users = []
    list_of_users = database.add_all_users_to_list(list_of_users)
        
    return {
        'users': list_of_users
    }


def admin_userpermission_change(token, u_id, permission_id):
    
    database.token_check(token)
    u_id_converted = database.convert_from_tok_to_u_id(token)
    database.channels_user_log_check(u_id_converted) 
    
    database.channel_user_exist_check(u_id)
    database.is_flockr_owner(token) 
    
    is_permission_valid(permission_id)

    if permission_id == 1:
        database.make_admin(u_id)
    
    if permission_id == 2:
        database.remove_admin(u_id)
        
    pass

def search(token, query_str):
    
    database.token_check(token)
    u_id = database.convert_from_tok_to_u_id(token)
    database.channels_user_log_check(u_id)   
    
    list_of_messages = []
    list_of_messages = database.add_selected_messages_to_list(query_str, token, list_of_messages)        
        
    return {
        'messages': list_of_messages
    }

# Helper Functions:
        
def is_permission_valid(permission_id):
    valid = 0
    if permission_id == 1:
        valid = 1
    if permission_id == 2:
        valid = 1
    if valid == 0: 
        raise InputError 
    pass

'''
assumptions:
    
    - only owner can make or remove other members as admins
'''