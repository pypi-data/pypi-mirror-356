from http import HTTPStatus

import requests

from .scheme import AuthResponse


class AuthenticationError(Exception):
    """Исключение для ошибок аутентификации."""


def auth(username, password, base_url, proto, verify):
    session = requests.Session()
    login_data = {
        'user': username,
        'password': password,
    }
    if proto == 'http':
        response = session.post(
                f'{base_url}/login',
                json=login_data,
            )
    if proto == 'https':
        response = session.post(
            f'{base_url}/login',
            json=login_data,
            verify=verify,
        )
    if response.status_code != HTTPStatus.OK:
        raise AuthenticationError('AuthError')
    auth_response = AuthResponse(**response.json())
    token = auth_response.data.authToken
    uid = auth_response.data.me.id
    return token, uid


class Auth():
    def session(self, username, password, base_url, proto, verify):
        auth_token, uid = auth(username, password, base_url, proto, verify)
        session = requests.Session()
        headers = {
            'X-Auth-Token': auth_token,
            'X-User-Id': uid,
        }
        session.headers.update(headers)
        session.username = username
        session.uid = uid
        return session
