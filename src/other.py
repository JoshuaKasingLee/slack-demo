from database import master_users, channels, channels_and_members, channels_and_messages, private_channels, public_channels

# add functions below if needed
def clear():
    global master_users
    master_users.clear()
    global channels
    channels.clear()
    global channels_and_members
    channels_and_members.clear()
    global channels_and_messages
    channels_and_messages.clear()
    global private_channels
    private_channels.clear()
    global public_channels 
    public_channels.clear()
    #global user
    #user.clear()
    #global users
    #users.clear()
    #global message
    #message.clear()
    #global messages
    #messages.clear()
    #global channel
    #channel.clear()
    #global member
    #member.clear()
    #global members
    #members.clear()


def users_all(token):
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

def admin_userpermission_change(token, u_id, permission_id):
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