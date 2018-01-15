from werkzeug.security import safe_str_cmp
from models.user import UserModel

###
# users = [
#     {
#         'id': 1,
#         'username': 'bob',
#         'password': 'asdf'
#     }
# ]
###

### interact with database instead of hardcode
# use User class to replace direct list
# users = [
#     User(1, 'bob', 'asdf')
# ]
###

# use mapping so we don't need to iterate the list everytime

###
# username_mapping = { 'bob': {
#         'id': 1,
#         'username': 'bob',
#         'password': 'asdf'
#     }
# }
#
# userid_mapping = { 1: {
#     'id': 1,
#     'username': 'bob',
#     'password': 'asdf'
#     }
# }
###

### interact with database so no need mappings
# simplify the mapping: but still key-value pair in dictionary
# username_mapping = {u.username: u for u in users}
# userid_mapping = {u.id: u for u in users}
###


def authenticate(username, password):
    # user = username_mapping.get(username, None)
    # change to interact with database
    user = UserModel.find_by_username(username)
    # use a safer way - Safe String Compare - to compare string
    # if user and user.password == password:
    if user and safe_str_cmp(user.password, password):
        return user

def identity(payload):
    # what we got is JWT payload so we're going to extract the user ID from the payload
    user_id = payload['identity']
    # return userid_mapping.get(user_id, None)
    return UserModel.find_by_id(user_id)
