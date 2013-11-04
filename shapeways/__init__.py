## Imports
import requests
import rauth
import json
import urlparse

# todo: logging with "logging" module
# todo: custom exception classes
# todo: configuration variables (global) for api key and base URL

## Configuration
# TODO: read these from non-commitable config somewhere
# Per app keys
consumer_key = None #'9a894be3afac00b2899b8008ee73dabdd66c5c62'
consumer_secret = None #'a9f9cf4ca0f3bb8d0b279a35b374e07262dc6f16'
# Per user keys
access_token = None #'b1aad5af593ab9f3c031ffa7c9a7742190832088'
access_token_secret = None #'249a76bda58908a1943d420180a6cc7b017d444b'
# URL
api_base = 'http://api.shapeways.com'

def get_request_token_decoder(contents):
    '''Needed because Shapeways request_token groups oauth_token with the authorization URL.'''
    fields = urlparse.parse_qs(contents)
    authentication_url = urlparse.urlparse(fields['authentication_url'][0])
    
    oauth_token_secret = fields['oauth_token_secret'][0]
    oauth_token = urlparse.parse_qs(authentication_url.query)['oauth_token'][0]

    result = {
        'oauth_token_secret': oauth_token_secret, 
        'oauth_token': oauth_token
    }
    
    return result

def get_oauth_session():
    session = rauth.OAuth1Session(
        consumer_key = consumer_key,
        consumer_secret = consumer_secret,
        access_token = access_token,
        access_token_secret = access_token_secret
    )
    
    return session
    
def get_oauth_service():
    service = rauth.OAuth1Service(
        consumer_key = consumer_key,
        consumer_secret = consumer_secret,
        name = 'shapeways',
        access_token_url = api_base + '/oauth1/access_token/v1',
        authorize_url = api_base + '/login',
        request_token_url = api_base + '/oauth1/request_token/v1',
        base_url = api_base,
    )
    
    return service