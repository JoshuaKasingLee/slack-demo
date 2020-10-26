Assumptions

auth.py
- There will be < 100 users with the same first and last name (in order to generate unique handles)
- The given regex ('^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$') covers all valid emails

channel.py
- for channel_messages, assume we have an InputError when start < 0
- Promoting users that do not exist raise an error
- Assuming that the flockr owner can make another u_id an owner of a channel the flockr owner 
    hasn’t joined yet
- When fetching messages, if the channel has no messages, it will not raise an error, rather it will return an invalid start

channels.py
- Creating channels with the same name is allowed
- Channels cannot be created with an empty name

message.py
- When sending a message, checking a users access has higher priority than the message length meaning an AccessError will be raised before Input error
- When editing a message, an Input Error is raised if the message does not exist
- If the input message is the same as the edit message, no action is required

other.py
- Only owner can make or remove other members as admins

user.py
- A user can only access their own profile
- The given regex ('^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$') covers all valid emails