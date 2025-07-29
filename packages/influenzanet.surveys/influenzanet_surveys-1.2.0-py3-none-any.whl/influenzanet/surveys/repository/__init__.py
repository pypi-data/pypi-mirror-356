import requests
import json
from time import sleep
import datetime
from typing import List, Optional, Dict, Any
from requests.auth import HTTPBasicAuth

REPOSITORY_API = 'https://surveys.ifn.epipop.fr'
DEFAULT_NAMESPACE = 'influenzanet'

class ApiError(Exception):
    """ 
        Api Error can be used to return the error with status
    """
    def __init__(self, message, status=None, response=None):
        super(ApiError, self).__init__(message)
        self.status = status
        self.response = response       
    
    def is_too_many_request(self):
        """
            Check if response is 
        """
        return self.status is not None and self.status == 429
    
    def retry_after(self):
        """
            Get Retry-After header
        """
        if self.response is None or self.response.headers is None:
            return None
        retry = self.response.headers.get('retry-after')
        if retry is None:
            return None
        return int(retry)
    
    def wait_retry_after(self, show:bool=True):
        retry = self.retry_after()
        if retry is None:
            return False
        if show:
            print("Waiting {} secs from Retry-After header".format(retry))
        sleep(retry)
        return True
        
class ApiRateLimiter:
    """
        Collect information about an eventual rate limiter 
        Provides wait() method to wait, or wait_delay() to get the delay
    """
    def __init__(self, headers):
        limit = headers.get('x-ratelimit-limit', None)
        self.limit = 0
        self.remaining = 0
        self.reset = 0
        if limit is not None:
            self.limit = int(limit)
        remaining = headers.get('x-ratelimit-remaining', None)
        if remaining is not None:
            self.remaining = int(remaining)
        reset = headers.get('x-ratelimit-reset', None)
        if reset is not None:
            self.reset = int(reset) 
    
    def wait_delay(self):
        """
            Compute the delay to wait (in sec.) considering the rate limiter info
        """
        if self.limit == 0 or self.reset == 0:
            return 0
        if self.remaining == 0:
            return self.reset
        w = (self.remaining / self.reset) + 0.05
        return w

    def wait(self, show: bool=True):
        w = self.wait_delay()
        if w > 0:
            if show:
                print("Waiting %f seconds (limit=%d, remains=%d, reset=%d)" % (w, self.limit, self.remaining, self.reset))
            sleep(w)

class APIResponse:

    def __init__(self, data, headers):
        self.data = data
        self.headers = headers
        self.limiter = ApiRateLimiter(headers)

class AuthKey:
    def __init__(self, key:str, expires: datetime.datetime):
        self.key = key
        self.expires = expires

    def expired(self):
        return self.expires < datetime.datetime.now()

    def add_header(self, headers:dict):
        headers['Authorization'] = "Bearer {}".format(self.key)

class ImportResponse:
    def __init__(self, meta, created:bool, limiter: ApiRateLimiter):
        self.id = meta.get('id', None)
        self.version = meta.get('version')
        self.published = meta.get('published')
        self.platform = meta.get('platform')
        self.survey_name = meta.get('name')
        self.model_type = meta.get('model_type')
        self.created = created
        self.limiter = limiter
 
class SurveyRepositoryAPI:

    def __init__(self, config: Optional[Dict[str, Any]]=None):
        """
        Create a API wrapper

        config is an optional dictionary.
        Can contain:
        `user`: user name to import survey
        `password`: password for user (only to import survey)
        `url`: customize repository url, only needed for dev
        `platform_code`: code of the platform to use for import 
        """
        if config is None:
            config = {}
        if not isinstance(config, dict):
            raise ValueError("config must be a dictionary")
        self.api_url = config.get('url', REPOSITORY_API)
        creds = None
        if 'user' in config:
            if 'password' not in config:
                raise ValueError("Missing field 'password' in survey repository config")
            creds = HTTPBasicAuth(config['user'], config['password'])
        self.credentials = creds
        self.auth_key: Optional[AuthKey] = None
        self.platform_code = config.get('platform_code', None)

    def create_error(self, response: requests.Response):
        msg = None
        try:
            data = response.json()
            if isinstance(data, dict) and "error" in data:
                msg = data["error"]
        except:
            pass
        if msg is None:
            msg = "Request error : " + response.reason
        raise ApiError(msg, response.status_code, response=response)
    
    def login(self):
        if self.auth_key is None or self.auth_key.expired():
            url = "{}/user/login".format(self.api_url)
            r = requests.get(url, auth=self.credentials)
            if r.status_code >= 200 and r.status_code <= 202:
                d = r.json()
                expires = datetime.datetime.now() + datetime.timedelta(seconds=d['ttl'])
                self.auth_key = AuthKey(d['key'], expires=expires)
            else:
                raise ApiError("Unable to login", r.status_code, response=r)
        
    def import_survey(self, survey, platform=None, namespace=None, version=None, name=None):
        """
            Import survey definition into the repository

            Caution, it's possible to import a survey preview, but it must be one single version of a survey
            In this case, to provide the `name` parameter is mandatory
            survey: the survey data (serialized json as string)
            platform: the platform code from which the survey belongs
            credentials: the account credentials on the repository
            namespace: namespace of the repository, by default its influenzanet for the Influenzanet project.
            version: version id of the survey (if it's published in a platform),
            name: name of the survey, this is used when uploading a survey preview (survey key is not in the preview itself)
        """

        if platform is None:
            if self.platform_code is None:
                raise ValueError("platform code is not set in configuration, must be provided")
            platform = self.platform_code
        if namespace is None:
            namespace = DEFAULT_NAMESPACE
        url = "{}/import/{}".format(self.api_url, namespace)
        data = {
            'platform': platform,
        }
        if version is not None:
            data['version'] = version
        if name is not None:
            data['name'] = name
        files = {'survey': ('survey_json', survey, 'application/json')}

        headers = {}
        self.login()
        if self.auth_key is None:
            raise ApiError("Authkey is not set")
        self.auth_key.add_header(headers)
        r = requests.post(url, headers=headers, files=files, data=data)
        if r.status_code >= 200 and r.status_code < 300:
            d = r.json()
            created = False
            if r.status_code == 201:
                created = True
            limiter = ApiRateLimiter(r.headers)
            response = ImportResponse(d, created=created, limiter=limiter)
            return response
        self.create_error(r)
        
    def list_surveys(self, namespace=None, platforms: Optional[List[str]]=None, names:Optional[List[str]]=None, types:Optional[List[str]]=None, limit:int=0, offset:int=0, short:bool=False):
        """
            List available surveys

            platforms: list of platforms code
            names: list of survey names
            types: list of model type ('P' for preview, 'D' for Definition)
        """
        if namespace is None:
            namespace = DEFAULT_NAMESPACE
        url = "{}/namespace/{}/surveys".format(self.api_url, namespace)
        if short:
            url += '/versions'
        params = {}
        if platforms is not None and len(platforms) > 0:
            params['platforms'] = ','.join(platforms)
        if names is not None and len(names) > 0:
            params['names'] = ','.join(names)
        
        if types is not None and len(types) > 0:
            params['types'] = ','.join(types)
        
        params['limit'] = limit
        if limit > 0:
            # Cannot provide offset if limit is 0
            params['offset'] = offset
        
        r = requests.get(url, params=params)
        if r.status_code == 200:
            return r.json()
        self.create_error(r)
        
    def load_survey_meta(self, id):
        """
            Load content of a survey definition for it's id
        """
        url = "{}/survey/{}".format(self.api_url, id)
        r = requests.get(url)
        if r.status_code == 200:
            return APIResponse(r.json(), r.headers)
        self.create_error(r)

    def load_survey_data(self, id):
        """
            Load content of a survey definition for it's id
        """
        #"/survey/:id/data"
        url = "{}/survey/{}/data".format(self.api_url, id)
        r = requests.get(url)
        if r.status_code == 200:
            return APIResponse(r.json(), r.headers)
        self.create_error(r)
       
         
        