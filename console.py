import shapeways

# Get keys from the environment
try:
    consumer_key = (os.environ['SW_CONSUMER_KEY'], os.environ['SW_CONSUMER_KEY_SECRET'])
    access_token = (os.environ['SW_ACCESS_TOKEN'], os.environ['SW_ACCESS_TOKEN_SECRET'])
except KeyError, e:
    sys.stderr.write("Please set SW_CONSUMER_KEY, SW_CONSUMER_KEY_SECRET, SW_ACCESS_TOKEN and SW_ACCESS_TOKEN_SECRET environment variables.\n")

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