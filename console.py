import shapeways

# For your sample app
consumer_key = ('9a894be3afac00b2899b8008ee73dabdd66c5c62', 'a9f9cf4ca0f3bb8d0b279a35b374e07262dc6f16')

# For pwalker
access_token = ('59e8b4bf1bb3d7d8955207f98e2fed1d31dd4127', '18bcb77e16a5dc70bda95a0b0b14e9297eccd572')

def run_price():
    session = shapeways.get_oauth_session()
    return shapeways.get_price(session, 0.000001, 0.0008, (0, 0, 0), (0.001, 0.001, 0.001))

def run_dance():
    oa = shapeways.OAuthDance(consumer_key)
    (request_token, url) = oa.get_request()
    print url
    print "Enter verifier:"
    verifier = raw_input()
    access_token = oa.get_access(request_token, verifier)
    
    print "Access token:"
    print access_token