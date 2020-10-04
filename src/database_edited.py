# To be put into iteration 1

# User
user = {}
# user = {"u_id" : 1, "email" : "a", "name_first": "kelly", "name_last": "zhou", "handle_str": "kellyzhou"}
# The general structure of user is summarised below
# user = {
#   'u_id': XX
#   'email' = XX
#   'name_first' = XX
#   'name_last' = XX
#   'handle_str' = XX
# }
# the auth register file in auth aims to pass in a user to append to users

# Users
users = [{'u_id':1, 'email': 'gmail', 'name_first': '1', 'name_last': '1'}, {'u_id':2,'email': 'gmail2', 'name_first': '2', 'name_last': '2'}, {'u_id':3,'email': 'gmail', 'name_first': '3', 'name_last': '3'}]
# Users contain a list of user
# An example is as below:
# [
#   {
#       'u_id': 100,
#       'email': 'apple@gmail.com',
#       'name_first': 'John',
#       'name_last': 'Smith',
#       'handle_str': 'herecomesjohnny'
#   },
#   {
#       'u_id': 300,
#       'email': 'Bpple@gmail.com',
#       'name_first': 'Cohn',
#       'name_last': 'Dmith',
#       'handle_str': 'byeerecomesjohnny'
#   }
# ]

# Message
message = {}

# Messages
messages = []

# Channel
channel = {}

# Channels
# List of dictionaries, where each dictionary contains types { channel_id, name }
channels = [{'channel_id': 1, 'name': 'channel1'}, {'channel_id': 2, 'name': 'channel2'} ]

private_channels= [{'channel_id': 2, 'name': 'channel1'}, ]
public_channels= [{'channel_id': 1, 'name': 'channel2'}, ]

# Member
member = {}

# Members
# List of dictionaries, where each dictionary contains types { u_id, name_first, name_last }
members = []

# channel with members
# channels_and_members = { channel_id: [owner_members, all_members], channel2: [owner_members2, all_members2], ...}
#channels_and_members = {1:[[{'u_id':1, 'name_first': 'andreea', 'name_last': 'hi'}],[]], 2:[[]{'u_id':1, 'name_first': 'andreea', 'name_last': 'hi'}]]}
#{'u_id':1, 'name_first': 'andreea', 'name_last': 'hi'}, {'u_id':2, 'name_first': 'anvdreea', 'name_last': 'hii'}
channels_and_members = { 1: [[{'u_id':1, 'name_first': '1', 'name_last': '1'}], [{'u_id':1, 'name_first': '1', 'name_last': '1'}]], 2: [[{'u_id':2, 'name_first': '2', 'name_last': '2'}], [{'u_id':2, 'name_first': '2', 'name_last': '2'}, {'u_id':3, 'name_first': 3, 'name_last': '3'}]], 3: [[{'u_id': 3, 'name_first': '3', 'name_last': '3'}], [{'u_id':3, 'name_first': 3, 'name_last': '3'}]]}
# the first user to sign up



# add functions below if needed
def clear():
    global user
    user.clear()
    global users
    users.clear()
    global message
    message.clear()
    global messages
    messages.clear()
    global channel
    channel.clear()
    global channels
    channels.clear()
    global member
    member.clear()
    global members
    members.clear()
    global channels_and_members
    channels_and_members. clear()
    global flockr_owner
    flockr_owner.clear()
