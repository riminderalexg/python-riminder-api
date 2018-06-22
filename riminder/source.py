from riminder import Riminder


class Source(object):

    def __init__(self, client):
        if not isinstance(client, Riminder):
            raise TypeError("client must be instance of Riminder class")

        self.client = client

    def get_sources(self):
        response = self.client.get("sources")
        return response.json()

    def get_source(self, source_id=None):
        query_params = {}
        query_params["source_id"] = self._validate_source_id(source_id)

        response = self.client.get('source', query_params)
        return response.json()

    def _validate_source_id(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("source_id must be string")

        return value
