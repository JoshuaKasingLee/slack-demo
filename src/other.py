import database
from error import InputError#, AcccessError

# add functions below if needed
def clear():
    database.clear()


def users_all(token):

    # using the function in the database but hasnt been pushed yet:
    #if database.is_token_valid(token) == FALSE: 
    #   return 
    
    list_of_users = []
    single_user = {}
    for user in database.master_users:
        single_user['u_id'] = user['u_id']
        single_user['email'] = user['email']
        single_user['name_first'] = user['name_first']
        single_user['name_last'] = user['name_last']
        single_user['handle_str'] = user['handle_str']
        list_of_users.append(single_user)
        
    return {
        'users': list_of_users
    }

'''
return {
    'users': [
        {
            'u_id': 1,
            'email': 'cs1531@cse.unsw.edu.au',
            'name_first': 'Hayden',
            'name_last': 'Jacobs',
            'handle_str': 'hjacobs',
        },
    ],
}
'''

def admin_userpermission_change(token, u_id, permission_id):
    
    # using the function in the database but hasnt been pushed yet:
    #if database.is_token_valid(token) == FALSE: 
    #   return AccessError
    
    # using the function in the database but hasnt been pushed yet:
    #if database.is_u_id_valid(u_id) == FALSE: 
    #   return InputError
    
    # using the function in the database but hasnt been pushed yet:
    #if database.is_token_owner(token) == FALSE: 
    #   return AccessError
    
    is_permission_valid(permission_id)

    if permission_id == 1:
        database.make_admin(token)
    
    if permission_id == 2:
        database.remove_admin(token)
        
    pass

def search(token, query_str):
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
    }
        
def is_permission_valid(permission_id):
    if permission_id != 1 or 2:
        return InputError 
    pass

'''
assumptions:
    
    only owner can make or remove other members as admins
'''