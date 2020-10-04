Assumptions

auth.py
- there will be < 100 users with the same name
- correct number of inputs is given to all functions
- input types are all correct (e.g. strings, ints, etc.)
- the given regex covers all valid emails
- registering a user will log the user in
- handles cannot be blackbox tested without user.py implementation
- a user is able to log in an infinite number of times (can log in when user is already logged in)
- once logged out, the user does not have the option to log out again \
(i.e. logout is only tested on users who are logged in)
- each user's token is generated as a string of their u_id: all tokens are \
invalidated when a user is "logged out", and are validated once again when they "log in"

channel.py

- token is a string of the u_id
- for channel_messages, assume we have an InputError when start < 0
- Channel_join does nothing if the user trying to join is already a member of the channel
- Channel_addowner raises an input error if the u_id that is being promoted is not a registred user
- Channel_addowner can add non-members directly as an owner (and my default normal member) of a channel
- Assuming that the flockr owner can make another u_id an owner of a channel the flockr owner 
    has'nt joined yet. This assumptions comes from the fact that the global permissions of
    flockr owner is that they can edit other owners permissions, and global permissions come
    before channel permissions which implies flockr owner has power over all owners, not just
    the ones of channels theyve joined.
- flockr owner can join private channels as well

channels.py
- duplicate channel names are allowed
- empty channel names are not allowed
- channel_listall displays all channels, including public and private