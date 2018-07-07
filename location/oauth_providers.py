import os
from mimetypes import guess_extension

from location.core import oauth

GOOGLE = 'google'
MICROSOFT = 'microsoft'


class OAuthProvider():

    def __init__(self, client_id, client_secret, allowed_domain=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.allowed_domain = allowed_domain

    def identity_endpoint(self):
        raise NotImplementedError

    def settings(self):
        raise NotImplementedError

    def user_domain(self):
        raise NotImplementedError

    def user_info(self):
        raise NotImplementedError


class GoogleOAuth(OAuthProvider):

    NAME = GOOGLE

    def identity_endpoint(self):
        return 'userinfo'

    def settings(self):
        return dict(
            name=GOOGLE,
            consumer_key=self.client_id,
            consumer_secret=self.client_secret,
            request_token_params={
                'scope': 'email profile',
                'hd': self.allowed_domain,
            },
            base_url='https://www.googleapis.com/oauth2/v1/',
            request_token_url=None,
            access_token_method='POST',
            access_token_url='https://accounts.google.com/o/oauth2/token',
            authorize_url='https://accounts.google.com/o/oauth2/auth',
        )

    def user_domain(self, response):
        return response.data['domain']

    def user_info(self, response):
        data = response.data
        return dict(
            oauth_id=data['id'],
            email=data['email'],
            avatar=data['picture'],
            name=data['name'],
        )


class MicrosoftOAuth(OAuthProvider):

    AUTH_TYPE = 'organizations'
    NAME = MICROSOFT
    SAVED_AVATAR_PATH = 'static/images/avatars'

    def identity_endpoint(self):
        return 'me'

    def settings(self):
        return dict(
            name=MICROSOFT,
            consumer_key=self.client_id,
            consumer_secret=self.client_secret,
            request_token_params={
                'scope': 'User.Read',
            },
            base_url='https://graph.microsoft.com/v1.0/',
            request_token_url=None,
            access_token_method='POST',
            access_token_url='https://login.microsoftonline.com/{}/oauth2/v2.0/token'.format(self.AUTH_TYPE),
            authorize_url='https://login.microsoftonline.com/{}/oauth2/v2.0/authorize'.format(self.AUTH_TYPE),
        )

    def user_domain(self, response):
        return response.data.get('mail', '').partition('@')[-1]

    def user_info(self, response):
        data = response.data
        return dict(
            oauth_id=data['id'],
            email=data['mail'],
            avatar=self._avatar(response),
            name=data['displayName'],
        )

    def _avatar(self, response):
        """
        Since the Microsoft identity API returns bytes,
        save the avatar image for the user
        and return the local path
        """
        if not os.path.isdir(self.SAVED_AVATAR_PATH):
            os.mkdir(self.SAVED_AVATAR_PATH)

        oauth_app = oauth.remote_apps[self.NAME]
        photo_metadata = oauth_app.get('me/photo')
        content_type = photo_metadata.data['@odata.mediaContentType']
        photo_tag = photo_metadata.data['@odata.mediaEtag']

        if not photo_tag:
            return ''

        photo_bytes = oauth_app.get('me/photo/$value')
        filename = response.data['id'] + guess_extension(content_type)
        relative_path = os.path.join(self.SAVED_AVATAR_PATH, filename)
        absolute_path = '/' + relative_path

        with open(relative_path, 'wb') as output:
            output.write(photo_bytes.data)

        return absolute_path


OAUTH_PROVIDERS = {
    GOOGLE: GoogleOAuth,
    MICROSOFT: MicrosoftOAuth,
}


def get_provider(provider, client_id, client_secret, allowed_domain):
    if provider not in OAUTH_PROVIDERS.keys():
        raise ValueError('OAuthProvider must be one of: {}'.format(', '.join(OAUTH_PROVIDERS.keys())))

    return OAUTH_PROVIDERS[provider](client_id, client_secret, allowed_domain)
