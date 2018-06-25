import requests as req
import json


RIMINDER_API_URL = "https://www.riminder.net/sf/public/api/v1.0/"


class Riminder(object):

    def __init__(self, api_key, webhook_secret=None):
        self.auth_header = {
            "X-API-Key": api_key
        }
        self.webhook_secret = webhook_secret

    def _create_request_url(self, resource_url):
        return "{api_endpoint}{resource_url}".format(
            api_endpoint=RIMINDER_API_URL,
            resource_url=resource_url
        )

    def _fill_headers(self, header):
        res = {}
        for key, value in header.items():
            res[key] = value
        return res

    def get(self, resource_endpoint, query_params={}, headers={}):
        url = self._create_request_url(resource_endpoint)
        header = self._fill_headers(self.auth_header)
        header = {**header, **self._fill_headers(headers)}
        if query_params:
            return req.get(url, headers=self.auth_header, params=query_params)
        else:
            return req.get(url, headers=self.auth_header)

    def post(self, resource_endpoint, data={}, files=None, headers={}):
        url = self._create_request_url(resource_endpoint)
        header = self._fill_headers(self.auth_header)
        header = {**header, **self._fill_headers(headers)}
        if files:
            return req.post(url, headers=header, files=files, data=data)
        else:
            return req.post(url, headers=header, data=data)

    def patch(self, resource_endpoint, data={}, headers={}):
        url = self._create_request_url(resource_endpoint)
        header = self._fill_headers(self.auth_header)
        header = {**header, **self._fill_headers(headers)}
        return req.patch(url, headers=self.auth_header, json=data)
