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
users = []
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
channels = []

# Member
member = {}

# Members
members = []

# channel with members
# channels_and_members = { channel_id: [owner_members, all_members], channel2: [owner_members2, all_members2], ...}
channels_and_members = {}


# the first user to sign up
flockr_owner = users[0]


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
