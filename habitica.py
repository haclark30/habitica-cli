import  requests
import json
import time
from os import path

BASE_URL = "https://habitica.com/api/v3"
CACHE_PATH = "./cache"
CACHE_TIMEOUT = 60 * 60 * 24

class HabiticaAPI(object):
    """
    Object that handles making requests to the Habitica API
    """
    def __init__(self):
        client_key = "93c29c04-03b3-416f-bc6f-0edbfd806238-HabiticaCLI"
        auth_cfg = 'auth.cfg'

        with open(auth_cfg, 'r') as auth_file:
            user_id = auth_file.readline()
            user_id = user_id.split('=')[1].strip()

            api_key = auth_file.readline()
            api_key = api_key.split('=')[1].strip()

        auth_headers = {'x-api-user': user_id, 'x-api-key': api_key, 'x-client': client_key}
        self.auth_headers = auth_headers

    def get_content(self):
        content_path = "{}/content.json".format(CACHE_PATH)
        if path.exists(content_path):
            with open(content_path, 'r') as f:
                content = json.load(f)
            
            time_diff = time.time() - content['dateRetrieved']
                
            if time_diff > CACHE_TIMEOUT:
                content = self.make_request('content')
                content['dateRetrieved'] = time.time()
                with open(content_path, 'w') as f:
                    json.dump(content, f)
                return content
            else:
                return content
        else:
            content = self.make_request('content')
            content['dateRetrieved'] = time.time()
            with open(content_path, 'w') as f:
                json.dump(content, f)

            return content

    def make_request(self, uri, method='get', params=None, data=None):
        if method not in ['get', 'put', 'post', 'delete']:
            raise ValueError("method must be one of [get, put, post, delete]")

        uri = "{base_url}/{uri}".format(base_url=BASE_URL, uri=uri)

        # if params:
        #     resp = requests.get(uri, headers=self.auth_headers, params=params)
        # else:
        #     resp = requests.get(uri, headers= self.auth_headers)

        if method == 'get':
            resp = requests.get(uri, headers=self.auth_headers, params=params)
        elif method == 'put':
            resp = requests.put(uri, headers=self.auth_headers, params=params, data=json.dumps(data))
        elif method == 'post':
            resp = requests.post(uri, headers=self.auth_headers, params=params, data=json.dumps(data))
        elif method == 'delete':
            resp = requests.delete(uri, headers=self.auth_headers, params=params, data=json.dumps(data))

        if resp.ok:
            return resp.json()["data"]