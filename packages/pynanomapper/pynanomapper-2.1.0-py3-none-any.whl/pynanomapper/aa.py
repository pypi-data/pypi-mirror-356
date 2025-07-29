from requests.auth import AuthBase
import requests
import pandas as pd
import yaml
from pandas import json_normalize

def search_service_protected(url,apikey):
    return (url,apikey)
def search_service_open(url):
    return (url)

class AmbitAPIKEYAuth(AuthBase):
    """Authorization: APIKEY XXXX"""
    def __init__(self, apikey=None):
        self.apikey = apikey

    def __call__(self, r):
        r.headers['Authorization'] = "APIKEY {}".format(self.apikey)
        return r

    def setKey(self, apikey):
        self.apikey=apikey


class GraviteeAuth(AuthBase):

    def __init__(self, apikey=None):
        self.apikey = apikey

    def __call__(self, r):
        r.headers['X-Gravitee-Api-Key'] = self.apikey
        return r

    def setKey(self, apikey):
        self.apikey=apikey

class BearerAuth(AuthBase):
    """Authorization: Bearer XXXX"""
    def __init__(self, token=None):
        self.token = token

    def __call__(self, r):
        if self.token != None:
            r.headers['Authorization'] = "Bearer {}".format(self.token)
        return r

    def setKey(self, token):
        self.apikey=token



def parseOpenAPI3(url='https://search.data.enanomapper.net/api-docs/', config='solr.yaml',auth="enmKeyAuth"):
    apikey=None
    config = yaml.load(requests.get(url+config).text, Loader=yaml.FullLoader)
    config_servers = json_normalize(config['servers'], None, ['url'])
    if 'securitySchemes' in config['components']:
        config_security = json_normalize(config['components']['securitySchemes'], None, [])
        try:
            apikey=config_security['{}.name'.format(auth)][0]
        except:
            apikey=None
    else:
        config_security = None

    auth_class=None
    msg=""
    if 'X-Gravitee-Api-Key' == apikey:
        auth_class = GraviteeAuth()
        msg = 'Enter `{}` you have received upon subscription to http://api.ideaconsult.net'.format(apikey)

    elif 'Authorization' == apikey:
        auth_class = AmbitAPIKEYAuth()
        msg = 'Enter AMBIT API Key'

    return config,config_servers, apikey, auth_class, msg

