import  requests
BASE_URL = "https://habitica.com/api/v3"

class HabiticaAPI(object):
    """
    Object that handles making requests to the Habitica API
    """
    def __init__(self, auth_headers=None):
        self.auth_headers = auth_headers

    def make_request(self, uri, params=None):
        uri = "{base_url}/{uri}".format(base_url=BASE_URL, uri=uri)
        if params:
            resp = requests.get(uri, headers=self.auth_headers, params=params)
        else:
            resp = requests.get(uri, headers= self.auth_headers)

        if resp.ok:
            return resp.json()["data"]