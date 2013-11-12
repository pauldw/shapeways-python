## Imports
import rauth
import json
import urlparse
import base64

# TODO: logging with "logging" module
# TODO: custom exception classes
# TODO: docstrings for each API method that repeat what's in the HTTP docs

class API():
    '''
    Shapeways API methods.
    '''
    def __init__(self, consumer_key, access_token):
        '''
        requestor is a Requestor object set up to make requests for a particular application and user
        '''
        self.requestor = Requestor(consumer_key, access_token)
    
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
        '''
        scale is upload 'scale' in meters.  1 means that 1 model unit equals 1 meter.  0.001 means that 1 model unit equals 1 mm.
        '''
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
    
    def get_model_file(self, id, version, include_file=None):
        data = {
            'modelId': id,
            'fileVersion': version,
            'file': include_file
        }
        
        return self.requestor.get('/models/' + str(id) + '/files/' + str(version) + '/v1', data)    

    def add_model_photo(self, id, file, filename, title=None, description=None, material_id=None, is_default=None):
        data = {
            'modelId': id,
            'file': base64.b64encode(file.read()),
            'title': title,
            'description': description,
            'materialId': material_id,
            'isDefault': is_default
        }
        
        return self.requestor.post('/models/' + str(id) + '/photos/v1', data)

    ## Printers
    def get_printers(self):
        return self.requestor.get('/printers/v1')

    def get_printer(self, id):
        return self.requestor.get('/printers/' + str(id) + '/v1') 
    
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

    ## Categories
    def get_categories(self):
        return self.requestor.get('/categories/v1')

    def get_category(self, id):
        return self.requestor.get('/categories/' + str(id) + '/v1') 

        
class Requestor():
    '''
    Provides underlying request methods that understand Shapeways API conventions and include OAuth information in each request.
    '''
    def __init__(self, consumer_key, access_token, api_base = 'http://api.shapeways.com'):
        '''
        consumer_key is a (public, secret) tuple of your application's consumer key
        access_token is a (public, secret) tuple of the access key you got for your application to access a particular user's account
        '''
        self.session = rauth.OAuth1Session(
            consumer_key = consumer_key[0],
            consumer_secret = consumer_key[1],
            access_token = access_token[0],
            access_token_secret = access_token[1]
        )
        
        self.api_base = api_base
    
    def filter_none(self, data):
        filtered_data = {k: v for k, v in data.items() if v != None}
        return filtered_data
        
    def parse_response(self, response):
        '''Turn response into JSON and raise exception on non-success result code.'''
        json_data = json.loads(response.content)
        
        if json_data['result'] not 'success':
            raise Exception("Got %s result from server." % json_data['result'])
        
        return json_data
        
    def get(self, path, data={}):
        response = self.session.get(self.api_base + path, data=self.filter_none(data))
        return self.parse_response(response)

    def delete(self, path, data={}):
        response = self.session.delete(self.api_base + path, data=self.filter_none(data))
        return self.parse_response(response)

    def post(self, path, data):    
        headers = {'Content-Type': 'application/json'}
        response = self.session.post(self.api_base + path, data = json.dumps(self.filter_none(data)), headers = headers)
        return self.parse_response(response)

    def put(self, path, data):    
        headers = {'Content-Type': 'application/json'}
        response = self.session.put(self.api_base + path, data = json.dumps(self.filter_none(data)), headers = headers)
        return self.parse_response(response)

class OAuthDance():
    '''
    OAuth Dance
    
    1. Call get_request to get request keys and the URL the user must visit to authorize the application
    2. Call get_access to get access keys.
    '''
    
    def __init__(self, consumer_key, api_base = 'http://api.shapeways.com'):
        '''
        consumer_key is the (public,secret) consumer key for your application, provided by Shapeways
        '''
        self.service = rauth.OAuth1Service(
            consumer_key = consumer_key[0],
            consumer_secret = consumer_key[1],
            name = 'shapeways',
            access_token_url = api_base + '/oauth1/access_token/v1',
            authorize_url = api_base + '/login',
            request_token_url = api_base + '/oauth1/request_token/v1',
            base_url = api_base,
        )
    
    def get_request(self):
        '''Get a request token and URL for user authorization.  You must save the request token for use when calling get_access.'''
        
        def decoder(contents):
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
        
        request_token = self.service.get_request_token(decoder = decoder)
        
        return (request_token, self.service.get_authorize_url(request_token[0]))
    
    def get_access(self, request_token, verifier):
        '''Use request token and user provided verifier to get the acccess token.  You must save the access token for use when making API requests on behalf of the user.'''        
        return self.service.get_access_token(request_token[0], request_token[1], data = {'oauth_verifier': verifier})