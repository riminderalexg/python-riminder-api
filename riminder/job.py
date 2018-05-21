from riminder import Riminder


class Job(object):

    def __init__(self, client):
        if not isinstance(client, Riminder):
            raise TypeError("client must be instance of Riminder class")

        self.client = client

    def get_all(self):
        response = self.client.get("jobs")
        return response.json()

    def get_by_id(self, job_id=None):
        query_params = {}
        query_params["job_id"] = self._validate_job_id(job_id)
        resource_endpoint = "job/{}".format(self._validate_job_id(job_id))

        response = self.client.get(resource_endpoint, query_params)
        return response.json()

    def _validate_job_id(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("job_id must be string")

        return value
