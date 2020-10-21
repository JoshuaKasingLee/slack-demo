# To be put into iteration 1

# (not given in spec) master users variables (contains ALL data relevant to ALL registered users)
# should update token each time we login
master_users = []
# [
#   {
#       'u_id': 100,
#       'email': 'apple@gmail.com',
#       'name_first': 'John',
#       'name_last': 'Smith',
#       'handle_str': 'herecomesjohnny'
#       'password': ilikecats
#       'token': 100
#       'log': True
#   },
#   {
#       'u_id': 300,
#       'email': 'Bpple@gmail.com',
#       'name_first': 'Cohn',
#       'name_last': 'Dmith',
#       'handle_str': 'byeerecomesjohnny'
#       'password': ilikedogs
#       'token': 300
#       'log': False
#   }

# User
# user = {}
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
# users = []
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
#message = {}

# Messages
#messages = []

# Channel
#channel = {}

# Channels
# List of dictionaries, where each dictionary contains types { channel_id, name }
channels = []

private_channels = [] # [{'channel_id': 2, 'name': 'channel1'},]
public_channels = []# [{'channel_id': 1, 'name': 'channel2'}, ]

# Member
#member = {}

# Members
#members = []

# channel with members
# channels_and_members = { channel_id: [owner_members, all_members], channel2: [owner_members2, all_members2], ...}
channels_and_members = {}


# messages in channels
#channels_and_messages = { channel_id: messages, channel_id2: messages2, ... }
#channels_and_messages = { 1: [ { 'message_id': 1, 'u_id': 1, 'message' = 'whtever the fuck', 'time_created' = 1111111111 }, { 'message_id': 2, ... } ... ], 2: ... }
channels_and_messages = {}

# messages = {
#   'message_id': {
#       'channel_id':
#       'u_id':
#       'message':
#       'deleted':
#   }
# }
messages = {}