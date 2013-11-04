import shapeways

def set_keys():
    shapeways.consumer_key = '9a894be3afac00b2899b8008ee73dabdd66c5c62'
    shapeways.consumer_secret = 'a9f9cf4ca0f3bb8d0b279a35b374e07262dc6f16'
    shapeways.access_token = '59e8b4bf1bb3d7d8955207f98e2fed1d31dd4127'
    shapeways.access_token_secret = '18bcb77e16a5dc70bda95a0b0b14e9297eccd572'

def get_session():
    return shapeways.get_oauth_session()
    
#shapeways.consumer_key = '9a894be3afac00b2899b8008ee73dabdd66c5c62'
#shapeways.consumer_secret = 'a9f9cf4ca0f3bb8d0b279a35b374e07262dc6f16'
#s = shapeways.get_oauth()
#rt = s.get_request_token(decoder = shapeways.get_request_token_decoder)
# need to do browser stuff, browse to access URL, authorize the app, get the verifier coder, then...
#authorize_url = s.get_authorize_url(rt[0])
# Where fde243 is whatever verifier you were given at the authorize URL
#s.get_access_token(rt[0], rt[1], data = {'oauth_verifier': 'fde243'})
# For your cube app this is the access token:
#(u'675d1d0731be188014a463b4ea37902b8f418491', u'ce6ad9188396a3c0ae703e7c6ecf0c064a629888')
# And this was the request token (not needed once you have access token)
# ('b1aad5af593ab9f3c031ffa7c9a7742190832088', '249a76bda58908a1943d420180a6cc7b017d444b')

def run_oauth():
    print "consumer_key:"
    shapeways.consumer_key = raw_input()
    print "consumer_key_secret:"
    shapeways.consumer_secret = raw_input()

    s = shapeways.get_oauth_service()
    rt = s.get_request_token(decoder = shapeways.get_request_token_decoder)

    print "Browse to:"
    print s.get_authorize_url(rt[0])

    print "verifier:"
    verifier = raw_input()

    (shapeways.access_token, shapeways.access_token_secret) = s.get_access_token(rt[0], rt[1], data = {'oauth_verifier': verifier})

    # Test session to see if this worked
    r = shapeways.get_oauth_session()
    r.get(shapeways.api_base + '/api/v1')
    
    if r.status_code not 200:
        raise Exception(r.content)

    print "Session established"
    print "shapeways.consumer_key = " + shapeways.consumer_key
    print "shapeways.consumer_secret = " + shapeways.consumer_secret
    print "shapeways.access_token = " + shapeways.access_token
    print "shapeways.access_token_secret = " + shapeways.access_token_secret