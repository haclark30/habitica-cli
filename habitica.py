import  requests
import json
BASE_URL = "https://habitica.com/api/v3"

class HabiticaAPI(object):
    """
    Object that handles making requests to the Habitica API
    """
    def __init__(self, auth_headers=None):
        self.auth_headers = auth_headers

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