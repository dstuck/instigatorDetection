from os import environ

import twitter
from yaml import safe_load

def get_credentials():
    credential_file = environ.get('TWITTER_CREDENTIAL_FILE', '/etc/twitter_api/credentials.yml')
    with open(credential_file) as f:
        credentials = safe_load(f.read())
    return credentials

def _get_api():
    return twitter.Api(**get_credentials())
