# To be put into iteration 1

# (not given in spec) master users variables (contains ALL data relevant to ALL registered users)
# should update token each time we login
master_users = []

channels = []

private_channels = [] # [{'channel_id': 2, 'name': 'channel1'},]
public_channels = []# [{'channel_id': 1, 'name': 'channel2'}, ]

# channels_and_members = { channel_id: [owner_members, all_members], channel2: [owner_members2, all_members2], ...}
channels_and_members = {}


# messages in channels
#channels_and_messages = { channel_id: messages, channel_id2: messages2, ... }
#channels_and_messages = { 1: [ { 'message_id': 1, 'u_id': 1, 'message' = 'whtever the fuck', 'time_created' = 1111111111 }, { 'message_id': 2, ... } ... ], 2: ... }
channels_and_messages = {}