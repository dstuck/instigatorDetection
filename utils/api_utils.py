from os import environ

from resilient_api.direct_twitter_api import DirectTwitterApi
from yaml import safe_load

def get_credentials():
    """
    Pull credentials from $TWITTER_CREDENTIAL_FILE or /etc/twitter_api/credentials.yml
    :return: credential dict
    """
    credential_file = environ.get('TWITTER_CREDENTIAL_FILE', '/etc/twitter_api/credentials.yml')
    with open(credential_file) as f:
        credentials = safe_load(f.read())
    return credentials

def get_api(credentials=None):
    """
    Get api from credentials. Default credentials pulled from $TWITTER_CREDENTIAL_FILE
    :param credentials: Dict specifying "consumer_key" and "consumer_secret"
    :return: twitter Api object
    """
    credentials = credentials or get_credentials()
    return DirectTwitterApi(application_only_auth=True, **credentials)
