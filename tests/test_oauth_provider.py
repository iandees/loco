from unittest import TestCase

from location import oauth_providers


class OAuthProviderUnitTests(TestCase):

    def test_get_provider(self):
        for provider_name in oauth_providers.OAUTH_PROVIDERS.keys():
            provider = oauth_providers.get_provider(
                provider_name,
                'id',
                'secret',
                'example.com',
            )

            self.assertIsInstance(provider, oauth_providers.OAuthProvider)

    def test_get_non_existant_provider_fails(self):
        with self.assertRaises(ValueError):
            oauth_providers.get_provider(
                'example',
                'id',
                'secret',
                'example.com',
            )

    def test_settings_contain_correct_keys(self):
        for provider_name in oauth_providers.OAUTH_PROVIDERS.keys():
            provider = oauth_providers.get_provider(
                provider_name,
                'id',
                'secret',
                'example.com',
            )
            provider_settings = provider.settings()

            expected_settings = [
                'name',
                'consumer_key',
                'consumer_secret',
                'request_token_params',
                'base_url',
                'request_token_url',
                'access_token_method',
                'access_token_url',
                'authorize_url',
            ]

            for setting in expected_settings:
                self.assertIn(setting, provider_settings)