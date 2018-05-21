from riminder import Riminder
import magic
import os

SERNIORITY_VALUES = ["all", "senior", "junior"]
STAGE_VALUES = [None, "NEW", "YES", "LATER", "NO"]
SORT_BY_VALUES = [None, "CREATION", "DESC", "RECEPTION", "RANKING"]


class Profile(object):
    """Class that interacts with Riminder API profiles endpoint.

    Usage example:

    >>> from riminder import Riminder
    >>> from riminder.profile import Profile
    >>> client = Riminder(api_key="YOUR_API_KEY")
    >>> profile = Profile(self.client)
    >>> result = profile.get_all(source_ids=["5823bc959983f7a5925a5356020e60d605e8c9b5"])
    >>> print(result)
    {
        "code": 200,
        "message": "OK",
        "data": {
            "page": 1,
            "maxPage": 3,
            "count_profiles": 85,
            "profiles": [
            {
                "profile_id": "215de6cb5099f4895149ec0a6ac91be94ffdd246",
                "profile_reference": "49583",
                ...
    """

    def __init__(self, client):
        """
        Initialize Profile object with Riminder client.
        Args:
            client: Riminder client instance <Riminder object>

        Returns:
            Profile instance object.
        """
        if not isinstance(client, Riminder):
            raise TypeError("client must be instance of Riminder class")

        self.client = client

    def get_all(self, source_ids=None, seniority="all", stage=None,
                date_start="1494539999", date_end="1502488799", job_id=None,
                page=1, limit=30, sort_by=None):
        """
        Retreive all profiles that match the query param

        Args:
            date_end:   <string> REQUIRED (default to "1502488799")
                        profiles' last date of reception
            date_start: <string> REQUIRED (default to "1494539999")
                        profiles' first date of reception
            job_id:     <string>
            limit:      <int> (default to 30)
                        number of fetched profiles/page
            page:       <int> REQUIRED default to 1
                        number of the page associated to the pagination
            seniority:  <string> defaut to "all"
                        profiles' seniority ("all", "senior", "junior")
            sort_by:    <string>
            source_ids: <array of strings> REQUIRED
            stage:      <string>

        Returns:
            Retrieve the profiles data as <dict>
        """
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

    def create_profile(self, source_id=None, file_path=None, profile_reference="",
                       timestamp_reception=None):
        """
        Add a profile resume to a sourced id

        Args:
            source_id:              <string>
                                    source id
            file_path:              <string>
                                    local path to resume file
            profile_reference:      <string> (default to "")
                                    reference to assign to the profile
            timestamp_reception:    <string>
                                    original date of the application of the profile

        Returns:
            Response that contains code 201 if successful
            Other status codes otherwise.
        """
        data = {}
        data["source_id"] = self._validate_source_id(source_id)
        data["profile_reference"] = self._validate_profile_reference(profile_reference)
        data["timestamp_reception"] = self._validate_timestamp_reception(timestamp_reception)
        files = self._get_file(file_path, profile_reference)

        response = self.client.post("profile", data=data, files={"file": files})
        return response.json()

    def get_by_id(self, source_id=None, profile_id=None):
        """
        Retrieve the profile information associated with profile id

        Args:
            source_id:              <string>
                                    source id
            profile_id:             <string>
                                    profile id

        Returns:
            profile information
        """
        query_params = {}
        query_params["source_id"] = self._validate_source_id(source_id)
        resource_endpoint = "profile/{}".format(self._validate_profile_id(profile_id))

        response = self.client.get(resource_endpoint, query_params)
        return response.json()

    def get_documents(self, source_id=None, profile_id=None):
        """
        Retrieve the file information

        Args:
            source_id:              <string>
                                    source id
            profile_id:             <string>
                                    profile id

        Returns:
            document information, like type, name, extension, url.. associated to the profile id
        """
        query_params = {}
        query_params["source_id"] = self._validate_source_id(source_id)
        resource_endpoint = "profile/{}/documents".format(self._validate_profile_id(profile_id))

        response = self.client.get(resource_endpoint, query_params)
        return response.json()

    def get_extractions(self, source_id=None, profile_id=None):
        """
        Retrieve the profile career's path associated with profile id

        Args:
            source_id:              <string>
                                    source id
            profile_id:             <string>
                                    profile id

        Returns:
            response see: https://developers.riminder.net/v1.0/reference#profileidextractions
        """
        query_params = {}
        query_params["source_id"] = self._validate_source_id(source_id)
        resource_endpoint = "profile/{}/extractions".format(self._validate_profile_id(profile_id))

        response = self.client.get(resource_endpoint, query_params)
        return response.json()

    def get_jobs(self, source_id=None, profile_id=None):
        """
        Retrieve the profile assessments associated with profile id

        Args:
            source_id:              <string>
                                    source id
            profile_id:             <string>
                                    profile id

        Returns:
            response see: https://developers.riminder.net/v1.0/reference#profileidjobs
        """
        query_params = {}
        query_params["source_id"] = self._validate_source_id(source_id)
        resource_endpoint = "profile/{}/jobs".format(self._validate_profile_id(profile_id))

        response = self.client.get(resource_endpoint, query_params)
        return response.json()

    def update_stage(self, source_id=None, profile_id=None, job_id=None, stage=None):
        """
        Edit the profile stage given a job

        Args:
            profile_id:             <string>
                                    profile id
        body params:
            source_id:              <string>
                                    source id associated to the profile
            
            job_id:                 <string>
                                    job id
            stage:                 <string>
                                    profiles' stage associated to the job ( null for all, NEW, YES, LATER or NO).

        Returns:
            Response that contains code 201 if successful
            Other status codes otherwise.
        """
        data = {}
        data["source_id"] = self._validate_source_id(source_id)
        data["job_id"] = self._validate_job_id(job_id)
        data["stage"] = self._validate_stage(stage)
        resource_endpoint = "profile/{}/stage".format(self._validate_profile_id(profile_id))

        response = self.client.patch(resource_endpoint, data=data)
        return response.json()

    def update_rating(self, source_id=None, profile_id=None, job_id=None, rating=None):
        """
        Edit the profile rating given a job

        Args:
            profile_id:             <string>
                                    profile id
        body params:
            source_id:              <string>
                                    source id associated to the profile
            
            job_id:                 <string>
                                    job id
            rating:                 <int32>
                                    profile rating from 1 to 4 associated to the job.

        Returns:
            Response that contains code 201 if successful
            Other status codes otherwise.
        """
        data = {}
        data["source_id"] = self._validate_source_id(source_id)
        data["job_id"] = self._validate_job_id(job_id)
        data["rating"] = self._validate_rating(rating)
        resource_endpoint = "profile/{}/rating".format(self._validate_profile_id(profile_id))

        response = self.client.patch(resource_endpoint, data=data)
        return response.json()

    def _get_file(self, file_path, profile_reference):

        try:
            return (
                os.path.basename(file_path) + profile_reference,  # file_name
                open(file_path, 'rb'),
                magic.Magic(mime=True).from_file(file_path)
            )
        except Exception as e:
            raise Exception(repr(e))

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

    def _validate_profile_reference(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("profile_reference must be string")

        return value

    def _validate_timestamp_reception(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("timestamp_reception must be string")

        return value
