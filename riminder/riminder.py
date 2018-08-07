import requests as req
import json

from .filter import Filter
from .profile import Profile
from .webhook import Webhook
from .source import Source

RIMINDER_API_URL = "https://www.riminder.net/sf/public/api/v1.0/"


class Riminder(object):
    """Riminder api wrapper client."""

    def __init__(self, api_key, webhook_secret=None, url=RIMINDER_API_URL):
        """Init."""
        self.url = url
        self.auth_header = {
            "X-API-Key": api_key
        }
        self.webhook_secret = webhook_secret
        self.filter = Filter(self)
        self.profile = Profile(self)
        self.webhooks = Webhook(self)
        self.source = Source(self)

    def _create_request_url(self, resource_url):
        return "{api_endpoint}{resource_url}".format(
            api_endpoint=self.url,
            resource_url=resource_url
        )

    def _fill_headers(self, header, base={}):
        for key, value in header.items():
            base[key] = value
        return base

    def _prepare_params_for_file_upload(self, bodyparams):
        for key, value in bodyparams.items():
            if isinstance(value, dict) or isinstance(value, list):
                bodyparams[key] = json.dumps(value)
        return bodyparams

    def get(self, resource_endpoint, query_params={}):
        """Don't use it."""
        url = self._create_request_url(resource_endpoint)
        if query_params:
            return req.get(url, headers=self.auth_header, params=query_params)
        else:
            return req.get(url, headers=self.auth_header)

    def post(self, resource_endpoint, data={}, files=None):
        """Don't use it."""
        url = self._create_request_url(resource_endpoint)
        if files:
            data = self._prepare_params_for_file_upload(data)
            return req.post(url, headers=self.auth_header, files=files, data=data)
        else:
            return req.post(url, headers=self.auth_header, json=data)

    def patch(self, resource_endpoint, data={}):
        """Don't use it."""
        url = self._create_request_url(resource_endpoint)
        return req.patch(url, headers=self.auth_header, json=data)
