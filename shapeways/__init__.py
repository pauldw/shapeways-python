## Imports
import rauth
import json
import urlparse
import base64

# todo: logging with "logging" module
# todo: custom exception classes

class Requestor():
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret, api_base = 'http://api.shapeways.com'):
        self.session = rauth.OAuth1Session(
            consumer_key = consumer_key,
            consumer_secret = consumer_secret,
            access_token = access_token,
            access_token_secret = access_token_secret
        )
        
        self.api_base = api_base
    
    @classmethod
    def filter_none(data):
        filtered_data = {k: v for k, v in data.items() if v != None}
        return filtered_data
        
    def get(self, path, data={}):
        response = self.session.get(self.api_base + path, data=filter_none(data))
        json_data = json.loads(response.content)
        return json_data

    def delete(self, path, data={}):
        response = self.session.delete(self.api_base + path, data=filter_none(data))
        json_data = json.loads(response.content)
        return json_data    

    def post(self, path, data):    
        headers = {'Content-Type': 'application/json'}
        response = self.session.post(self.api_base + path, data = json.dumps(filter_none(data)), headers = headers)
        json_data = json.loads(response.content)
        return json_data

    def put(self, path, data):    
        headers = {'Content-Type': 'application/json'}
        response = self.session.put(self.api_base + path, data = json.dumps(filter_none(data)), headers = headers)
        json_data = json.loads(response.content)
        return json_data

class API():
    def __init__(self, requestor):
        self.requestor = requestor
    
    ## API Info
    def get_api_info(self):
        return self.requestor.get('/api/v1')    
    
    ## Cart
    def get_cart(self):
        return self.requestor.get('/orders/cart/v1')

    def add_to_cart(self, model_id, material_id=None, quantity=None):
        data = {
            'modelId': model_id,
            'materialId': material_id,
            'quantity': quantity
        }
        
        return self.requestor.post('/orders/cart/v1', data)
    
    ## Materials
    def get_materials(self):
        return self.requestor.get('/materials/v1')

    def get_material(self, id):
        return self.requestor.get('/materials/' + str(id) + '/v1') 

    ## Models
    def get_models(self, page=None):
        data = {
            'page': page
        }
        
        return self.requestor.get('/models/v1', data)

    def get_model(self, id):
        return self.requestor.get('/models/' + str(id) + '/v1') 
       
    def get_model_info(self, id):
        return self.requestor.get('/models/' + str(id) + '/info/v1') 

    def add_model(self, file, filename, scale=None, title=None, description=None, is_public=None, is_for_sale=None, is_downloadable=None, tags=None, materials=None, default_material_id=None, categories=None):
        data = {
            'file': base64.b64encode(file.read()),
            'fileName': filename,
            'uploadScale': scale,
            'hasRightsToModel': True,
            'acceptTermsAndConditions': True,
            'title': title,
            'description': description,
            'isPublic': is_public,
            'isForSale': is_for_sale,
            'isDownloadable': is_downloadable,
            'tags': tags,
            'materials': materials,
            'defaultMaterialId': default_material_id,
            'categories': categories
        }
        
        return self.requestor.post('/models/v1', data)

    def delete_model(self, id):
        return self.requestor.delete('/models/' + str(id) + '/v1')     

    def update_model_info(self, id, title=None, description=None, is_public=None, is_for_sale=None, is_downloadable=None, tags=None, materials=None, default_material_id=None, categories=None):
        data = {
            'title': title,
            'description': description,
            'isPublic': is_public,
            'isForSale': is_for_sale,
            'isDownloadable': is_downloadable,
            'tags': tags,
            'materials': materials,
            'defaultMaterialId': default_material_id,
            'categories': categories
        }
        
        return self.requestor.put('/models/' + str(id) + '/info/v1', data)

    def update_model_file(self, id, file, filename, scale=None):
        data = {
            'file': base64.b64encode(file.read()),
            'fileName': filename,
            'uploadScale': scale,
            'hasRightsToModel': True,
            'acceptTermsAndConditions': True
        }
        
        return self.requestor.post('/models/' + str(id) + '/files/v1', data)
    
    ## Pricing
    def get_price(self, volume, area, point_min, point_max, materials=None):
        (x_min, y_min, z_min) = point_min
        (x_max, y_max, z_max) = point_max
        
        data = {
            'volume': volume,
            'area': area,
            'xBoundMin': x_min,
            'xBoundMax': x_max,
            'yBoundMin': y_min,
            'yBoundMax': y_max,
            'zBoundMin': z_min,
            'zBoundMax': z_max
        }
        
        return self.requestor.post('/price/v1', data)

class OAuthDance():
    def __init__(self, consumer_key, consumer_secret, api_base = 'http://api.shapeways.com'):
        self.api_base = api_base
        
        ## The Dance to get Access Tokens
        
        # 1. __init__: Start with these consumer keys for our application
        self.consumer_key = consumer_key
        self.consumer_key_secret = consumer_key_secret
        
        # 2. get_authorize_url: Generate request tokens and generate a link for the user to authorize us.  We must remember the request tokens.
        self.request_token = None

        # 3. get_access_token: Get a verifier back from the user, combine with our request token and get these access tokens for the user.  Done!
        
        self.service = rauth.OAuth1Service(
            consumer_key = self.consumer_key,
            consumer_secret = self.consumer_secret,
            name = 'shapeways',
            access_token_url = api_base + '/oauth1/access_token/v1',
            authorize_url = api_base + '/login',
            request_token_url = api_base + '/oauth1/request_token/v1',
            base_url = api_base,
        )
    
    def get_authorize_url(self, request_token):
        def get_request_token_decoder(self, contents):
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
        
        # Remember request token.
        self.request_token = self.service.get_request_token(decoder = get_request_token_decoder)
        
        return self.service.get_authorize_url(self.request_token[0])
    
    def get_access_token(self, verifier):
        if not self.request_token:
            raise Exception("You must first call get_authorize_url to get request tokens and authorize URL for user to visit.")
            
        return self.service.get_access_token(self.request_token[0], self.request_token[1], data = {'oauth_verifier': verifier})
    
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
    
    if r.status_code != 200:
        raise Exception(r.content)

    print "Session established"
    print "shapeways.consumer_key = " + shapeways.consumer_key
    print "shapeways.consumer_secret = " + shapeways.consumer_secret
    print "shapeways.access_token = " + shapeways.access_token
    print "shapeways.access_token_secret = " + shapeways.access_token_secret