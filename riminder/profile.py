from riminder import Riminder

SERNIORITY_VALUES = ["all", "senior", "junior"]
STAGE_VALUES = [None, "NEW", "YES", "LATER", "NO"]
SORT_BY_VALUES = [None, "CREATION", "DESC", "RECEPTION", "RANKING"]


class Profile(object):

    def __init__(self, client):
        if not isinstance(client, Riminder):
            raise TypeError("client must be instance of Riminder class")

        self.client = client

    def get_all(self, source_ids=None, seniority="all", stage=None,
                date_start="1494539999", date_end="1502488799", job_id=None,
                page=1, limit=30, sort_by=None):

        query_params = {}
        query_params["date_end"] = self._validate_date_end(date_end)
        query_params["date_start"] = self._validate_date_start(date_start)
        query_params["job_id"] = self._validate_job_id(job_id)
        query_params["limit"] = self._validate_limit(limit)
        query_params["page"] = self._validate_page(page)
        query_params["seniority"] = self._validate_seniority(seniority)
        query_params["sort_by"] = self._validate_sort_by(sort_by)
        query_params["source_ids"] = self._validate_source_ids(source_ids)
        query_params["stage"] = self._validate_stage(stage)

        response = self.client.get("profiles", query_params)
        return response.json()

    def create_profile(self, source_id=None, file=None, profile_reference=None,
                       timestamp_reception=None):
        data = {}
        data["source_id"] = self._validate_source_id(source_id)
        data["profile_reference"] = profile_reference
        data["timestamp_reception"] = timestamp_reception

        response = self.client.post("profile", data=data, files={"file": file})
        return response.json()

    def get_by_id(self, source_id=None, profile_id=None):
        query_params = {}
        query_params["source_id"] = self._validate_source_id(source_id)
        resource_endpoint = "profile/{}".format(self._validate_profile_id(profile_id))

        response = self.client.get(resource_endpoint, query_params)
        return response.json()

    def get_documents(self, source_id=None, profile_id=None):
        query_params = {}
        query_params["source_id"] = self._validate_source_id(source_id)
        resource_endpoint = "profile/{}/documents".format(self._validate_profile_id(profile_id))

        response = self.client.get(resource_endpoint, query_params)
        return response.json()

    def get_extractions(self, source_id=None, profile_id=None):
        query_params = {}
        query_params["source_id"] = self._validate_source_id(source_id)
        resource_endpoint = "profile/{}/extractions".format(self._validate_profile_id(profile_id))

        response = self.client.get(resource_endpoint, query_params)
        return response.json()

    def get_jobs(self, source_id=None, profile_id=None):
        query_params = {}
        query_params["source_id"] = self._validate_source_id(source_id)
        resource_endpoint = "profile/{}/jobs".format(self._validate_profile_id(profile_id))

        response = self.client.get(resource_endpoint, query_params)
        return response.json()

    def update_stage(self, source_id=None, profile_id=None, job_id=None, stage=None):
        data = {}
        data["source_id"] = self._validate_source_id(source_id)
        data["job_id"] = self._validate_job_id(job_id)
        data["stage"] = self._validate_stage(stage)
        resource_endpoint = "profile/{}/stage".format(self._validate_profile_id(profile_id))

        response = self.client.patch(resource_endpoint, data=data)
        return response.json()

    def update_rating(self, source_id=None, profile_id=None, job_id=None, rating=None):
        data = {}
        data["source_id"] = self._validate_source_id(source_id)
        data["job_id"] = self._validate_job_id(job_id)
        data["rating"] = self._validate_rating(rating)
        resource_endpoint = "profile/{}/rating".format(self._validate_profile_id(profile_id))

        response = self.client.patch(resource_endpoint, data=data)
        return response.json()

    def _validate_source_ids(self, value):
        if not isinstance(value, list):
            raise TypeError("source_ids must be a list")

        if not value or not all(isinstance(elt, str) for elt in value):
            raise TypeError("source_ids must contain list of strings")

        return value

    def _validate_source_id(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("source_id must be string")

        return value

    def _validate_profile_id(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("source_id must be string")

        return value

    def _validate_seniority(self, value):
        if value not in SERNIORITY_VALUES:
            raise ValueError("seniority value must be in {}".format(str(SERNIORITY_VALUES)))

        return value

    def _validate_stage(self, value):
        if value not in STAGE_VALUES:
            raise ValueError("stage value must be in {}".format(str(STAGE_VALUES)))

        return value

    def _validate_date_start(self, value):
        if not isinstance(value, str):
            raise TypeError("date_start must be string")

        return value

    def _validate_date_end(self, value):
        if not isinstance(value, str):
            raise TypeError("date_end must be string")

        return value

    def _validate_job_id(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("job_id must be string")

        return value

    def _validate_page(self, value):
        if not isinstance(value, int):
            raise TypeError("page must be 'int'")

        return value

    def _validate_limit(self, value):
        if not isinstance(value, int):
            raise TypeError("limit must be 'int'")

        return value

    def _validate_rating(self, value):
        if not isinstance(value, int):
            raise TypeError("rating must be 'int'")

        return value

    def _validate_sort_by(self, value):
        if value not in SORT_BY_VALUES:
            raise ValueError("sort_by value must be in {}".format(str(SORT_BY_VALUES)))

        return value