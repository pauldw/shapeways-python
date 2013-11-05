## Imports
import rauth
import json
import urlparse

# todo: logging with "logging" module
# todo: custom exception classes

## Configuration
# App keys
consumer_key = None
consumer_secret = None
# User keys
access_token = None
access_token_secret = None
# URL
api_base = 'http://api.shapeways.com'

## Objects
# API 
# Cart
# Material
# Model
# Printer
# Price
# Category

def do_get(path, data={}):
    response = get_session().get(api_base + path, data=data)
    json_data = json.loads(response.content)
    return json_data

def do_post(path, data):    
    headers = {'Content-Type': 'application/json'}
    response = get_session().post(api_base + path, data = json.dumps(data), headers = headers)
    json_data = json.loads(response.content)
    return json_data
    
def get_session():
    if not consumer_key or not consumer_secret or not access_token or not access_token_secret:
        raise Exception("access keys not set, please see configuration guide")

    return get_oauth_session()

def get_api_info():
    return do_get('/api/v1')    

def get_cart():
    return do_get('/orders/cart/v1')

def add_to_cart(model_id, material_id, quantity):
    data = {
        'modelId': model_id,
        'materialId': material_id,
        'quantity': quantity
    }
    
    return do_post('/orders/cart/v1', data)
    
def get_materials():
    return do_get('/materials/v1')

def get_material(id):
    return do_get('/materials/' + str(id) + '/v1') 

def get_models(page=None):
    data = {}
    
    if page:
        data['page'] = page
    
    return do_get('/models/v1', data)
    
def get_price(volume, area, point_min, point_max, materials=None):
    (x_min, y_min, z_min) = point_min
    (x_max, y_max, z_max) = point_max
    
    data = {
        'volume': volume,
        'area': area,
        #'x_bound_min': x_min,
        #'x_bound_max': x_max,
        #'y_bound_min': y_min,
        #'y_bound_max': y_max,
        #'z_bound_min': z_min,
        #'z_bound_max': z_max
    }
    
    return do_post('/price/v1', data)

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