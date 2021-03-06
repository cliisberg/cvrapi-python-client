import json
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
from cvrapi_client import exceptions
import cvrapi_client


class Adapter(HTTPAdapter):
    def init_pool(self, connections, block=False):
        self.pool = PoolManager(num_pools=connections, block=block)


class CVRAPI(object):
    base_url = 'https://cvrapi.dk/api'

    def __init__(self,
                 user_agent=None,
                 country=None,
                 version='6',
                 base_url=None):

        self.user_agent = user_agent

        if country:
            self.country = country

        if base_url:
            self.base_url = base_url

        if version:
            self.version = version

        self.session = _session()


    def perform(self, method, params, return_format, token, **kwargs):
        response = self.session

        url = '{0}{1}&version={2}&country={3}&format={4}'.format(self.base_url, params, self.version, self.country, return_format)
        if token:
            url += '&token={0}'.format(token)

        headers = {'User-Agent': self.user_agent}

        if method == 'post':
            response = response.post(url,
                                     data=json.dumps(kwargs),
                                     headers=headers)
        else:
            response = response.get(url,
                                    params=kwargs,
                                    headers=headers)

        if return_format == 'xml':
            body = response.text
        else:
            body = response.json()

        if response.status_code >= 400:
            raise exceptions.ApiError(body, response.status_code)

        return body


def _session():
    session = requests.Session()
    session.mount('https://', Adapter())
    return session
