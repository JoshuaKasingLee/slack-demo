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

