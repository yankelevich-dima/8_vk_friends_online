import sys
import getpass

import vk

APP_ID = 5114432


def get_access_token(path):
    with open(path, 'r') as f:
        access_token = f.read()
    return access_token.replace('\n', '')


def get_user_login():
    return input('Username: ')


def get_user_password():
    return getpass.getpass()


def get_session(access_token=None, login=None, password=None):
    session = None
    if access_token:
        try:
            session = vk.Session(
                access_token=access_token
            )
        except vk.exceptions.VkAPIError:
            print('Something wrong with access token')
    elif login and password:
        try:
            session = vk.AuthSession(
                app_id=APP_ID,
                user_login=login,
                user_password=password,
            )
        except vk.exceptions.VkAuthError:
            print('Login or password are incorrect or this login uses 2FA')

    return session


def get_online_friends(session):
    api = vk.API(session)
    friends = api.friends.get()
    return filter(
        lambda friend: friend['online'],
        api.users.get(user_ids=friends, fields=['online'])
    )


def output_friends_to_console(friends_online):
    for friend in friends_online:
        print('{} {}'.format(friend['last_name'], friend['first_name']))


if __name__ == '__main__':
    if len(sys.argv) > 1:
        access_token = get_access_token(sys.argv[1])
        session = get_session(access_token=access_token)
    else:
        login = get_user_login()
        password = get_user_password()
        session = get_session(login=login, password=password)

    if session is not None:
        friends_online = get_online_friends(session)
        output_friends_to_console(friends_online)
