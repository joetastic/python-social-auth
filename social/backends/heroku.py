"""
Heroku OAuth2 Backend
"""
from social.backends.oauth import BaseOAuth2
import requests.auth as auth


class Bearer(auth.AuthBase):
    def __init__(self, access_token):
        self._access_token = access_token

    def __call__(self, r):
        r.headers['Authorization'] = 'Bearer {}'.format(
            self._access_token)
        return r


class HerokuOAuth2(BaseOAuth2):
    """Heroku OAuth authentication backend"""
    name = 'heroku-oauth2'
    ID_KEY = 'user_id'
    AUTHORIZATION_URL = 'https://id.heroku.com/oauth/authorize'
    ACCESS_TOKEN_URL = 'https://id.heroku.com/oauth/token'
    ACCESS_TOKEN_METHOD = 'POST'
    SCOPE_SEPARATOR = ','
    EXTRA_DATA = [
        ('refresh_token', 'refresh_token', True),
        ('expires_in', 'expires'),
        ('token_type', 'token_type', True)
    ]

    def get_user_details(self, response):
        """Return user details from Heroku account"""
        return {'email': response.get('email') or '',
                'fullname': response.get('name') or ''}

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        url = 'https://api.heroku.com/account'
        return self.get_json(url, auth=Bearer(access_token))
