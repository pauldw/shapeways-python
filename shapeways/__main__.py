'''Console for experimenting with the Shapeways API.'''
import shapeways
import json
import sys
import os
import code

def input(prompt):
    sys.stdout.write(prompt + ": ")
    return raw_input()

def create_keys_interactive(filename):
    '''Interactive portion to help with creating a persistent keyfile for future console use.'''    
    print("It looks like you need to create some keys for the console.  Keys will be stored in %s." % filename)
    print("Note you must first have created an app on Shapeways at https://developers.shapeways.com/manage-apps/create")
    
    consumer_key = input("consumer key")
    consumer_key_secret = input ("consumer key secret")
    oa = shapeways.OAuthDance((consumer_key, consumer_key_secret))
    (request_token, url) = oa.get_request()
    
    print("Go to: %s" % url)
    
    verifier = input("verifier")
    (access_token, access_token_secret) = oa.get_access(request_token, verifier)
    
    print("Access token: %s" % access_token)
    print("Access token secret: %s" % access_token_secret)
    
    oauth_keys = {'consumer_key': consumer_key, 'consumer_key_secret': consumer_key_secret, 'access_token': access_token, 'access_token_secret': access_token_secret}
    
    json.dump(oauth_keys, open(filename, 'wb'))
    
    print "Wrote keys to %s.  Done!" % filename

def get_keys(filename='console_oauth_keys.json'):
    '''Returns keys stored in filename as ((consumer_key, consumer_key_secret), (access_token, access_token_secret))'''
    if not os.path.isfile(filename):
        create_keys_interactive(filename)

    keys = json.load(open(filename))
    
    r = ((keys['consumer_key'], keys['consumer_key_secret']), (keys['access_token'], keys['access_token_secret']))
    
    return r

def get_api():
    keys = get_keys()
    return shapeways.API(keys[0], keys[1])

api = get_api()
code.interact(banner="Shapeways console.  Use the 'api' object for API access.", local=locals())