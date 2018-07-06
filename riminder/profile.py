import time
import magic
import os
import os.path as path
import json

SERNIORITY_VALUES = ["all", "senior", "junior"]
STAGE_VALUES = [None, "NEW", "YES", "LATER", "NO"]
SORT_BY_VALUES = [None, "creation", "DESC", "reception", "ranking"]
VALID_EXTENSIONS = ['.pdf', '.png', '.jpg', '.jpeg', '.bmp', '.doc', '.docx', '.rtf', '.dotx', '.odt', '.odp', '.ppt', '.pptx', '.rtf', '.msg']
INVALID_FILENAME = ['.', '..']
TIMESTAMP_NOW = str(time.time())


class Profile(object):
    """Class that interacts with Riminder API profiles endpoint.

    Usage example:

    >>> from riminder import Riminder
    >>> from riminder.profile import Profile
    >>> client = Riminder(api_key="YOUR_API_KEY")
    >>> profile = Profile(self.client)
    >>> result = profile.get_profiles(source_ids=["5823bc959983f7a5925a5356020e60d605e8c9b5"])
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

        self.client = client
        self.stage = ProfileStage(self.client)
        self.document = ProfileDocument(self.client)
        self.parsing = ProfileParsing(self.client)
        self.scoring = ProfileScoring(self.client)
        self.rating = ProfileRating(self.client)
        self.data = ProfileData(self.client)

    def list(self, source_ids=None, seniority="all", stage=None,
            date_start="1494539999", date_end=TIMESTAMP_NOW, filter_id=None,
            page=1, limit=30, sort_by='ranking', filter_reference=None, order_by=None):
        """
        Retreive all profiles that match the query param

        Args:
            date_end:   <string> REQUIRED (default to "1502488799")
                        profiles' last date of reception
            date_start: <string> REQUIRED (default to "1494539999")
                        profiles' first date of reception
            filter_id:     <string>
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
        query_params["date_end"] = _validate_date_end(date_end)
        query_params["date_start"] = _validate_date_start(date_start)
        if filter_id:
            query_params["filter_id"] = _validate_filter_id(filter_id)
        if filter_reference:
            query_params["filter_reference"] = _validate_filter_reference(filter_reference)
        query_params["limit"] = _validate_limit(limit)
        query_params["page"] = _validate_page(page)
        query_params["seniority"] = _validate_seniority(seniority)
        query_params["sort_by"] = _validate_sort_by(sort_by)
        query_params["source_ids"] = json.dumps(_validate_source_ids(source_ids))
        query_params["stage"] = _validate_stage(stage)
        query_params["order_by"] = order_by

        response = self.client.get("profiles", query_params)
        return response.json()

    def add(self, source_id=None, file_path=None, profile_reference="",
            timestamp_reception=None, training_metadata=[]):
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
        data["source_id"] = _validate_source_id(source_id)
        data["profile_reference"] = _validate_profile_reference(profile_reference)
        data["timestamp_reception"] = _validate_timestamp_reception(timestamp_reception)
        data["training_metadata"] = _validate_training_metadata(training_metadata)
        files = _get_file_metadata(file_path, profile_reference)
        response = None
        with open(file_path, 'rb') as in_file:
            files = (files[0], in_file, files[2])
            response = self.client.post("profile", data=data, files={"file": files})
        return response.json()

    def addList(self, source_id, dir_path, is_recurcive=False, timestamp_reception=None, training_metadata=[]):
        if not path.isdir(dir_path):
            raise ValueError(dir_path + ' is not a directory')
        files_to_send = _get_files_from_dir(dir_path, is_recurcive)
        succeed_upload = {}
        failed_upload = {}
        for file_path in files_to_send:
            try:
                resp = self.add(source_id=source_id,
                    file_path=file_path, profile_reference="",
                    timestamp_reception=timestamp_reception, training_metadata=training_metadata)
                if resp['code'] != 200 and resp['code'] != 201:
                    failed_upload[file_path] = ValueError('Invalid response: ' + str(resp))
                else:
                    succeed_upload[file_path] = resp
            except BaseException as e:
                failed_upload[file_path] = e
        result = {
            'success': succeed_upload,
            'fail': failed_upload
        }
        return result

    def get(self, source_id=None, profile_id=None, profile_reference=None):
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
        query_params["source_id"] = _validate_source_id(source_id)
        if profile_id:
            query_params["profile_id"] = _validate_profile_id(profile_id)
        if profile_reference:
            query_params["profile_reference"] = _validate_profile_reference(profile_reference)
        response = self.client.get('profile', query_params)
        return response.json()


class ProfileDocument():
    def __init__(self, api):
        self.client = api

    def list(self, source_id=None, profile_id=None, profile_reference=None):
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
        query_params["source_id"] = _validate_source_id(source_id)
        if profile_id:
            query_params["profile_id"] = _validate_profile_id(profile_id)
        if profile_reference:
            query_params["profile_reference"] = _validate_profile_reference(profile_reference)
        response = self.client.get('profile/documents', query_params)
        return response.json()


class ProfileParsing():
    def __init__(self, api):
        self.client = api

    def get(self, source_id=None, profile_id=None, profile_reference=None):
        """
        Retrieve the parsing information

        Args:
            source_id:              <string>
                                    source id
            profile_id:             <string>
                                    profile id

        Returns:
            parsing information
        """
        query_params = {}
        query_params["source_id"] = _validate_source_id(source_id)
        if profile_id:
            query_params["profile_id"] = _validate_profile_id(profile_id)
        if profile_reference:
            query_params["profile_reference"] = _validate_profile_reference(profile_reference)
        response = self.client.get('profile/parsing', query_params)
        return response.json()


class ProfileScoring():
    def __init__(self, api):
        self.client = api

    def list(self, source_id=None, profile_id=None, profile_reference=None):
        """
        Retrieve the scoring information

        Args:
            source_id:              <string>
                                    source id
            profile_id:             <string>
                                    profile id

        Returns:
            parsing information
        """
        query_params = {}
        query_params["source_id"] = _validate_source_id(source_id)
        if profile_id:
            query_params["profile_id"] = _validate_profile_id(profile_id)
        if profile_reference:
            query_params["profile_reference"] = _validate_profile_reference(profile_reference)
        response = self.client.get('profile/scoring', query_params)
        return response.json()


class ProfileStage():
    def __init__(self, api):
        self.client = api

    def set(self, source_id=None, profile_id=None, filter_id=None, stage=None, profile_reference=None, filter_reference=None):
        """
        Edit the profile stage given a filter

        Args:
            profile_id:             <string>
                                    profile id
        body params:
            source_id:              <string>
                                    source id associated to the profile

            filter_id:                 <string>
                                    filter id
            stage:                 <string>
                                    profiles' stage associated to the filter ( null for all, NEW, YES, LATER or NO).

        Returns:
            Response that contains code 201 if successful
            Other status codes otherwise.
        """
        data = {}
        data["source_id"] = _validate_source_id(source_id)
        if profile_id:
            data["profile_id"] = _validate_profile_id(profile_id)
        if filter_id:
            data["filter_id"] = _validate_filter_id(filter_id)
        if profile_reference:
            data["profile_reference"] = _validate_profile_reference(profile_reference)
        if filter_reference:
            data["filter_reference"] = _validate_filter_reference(filter_reference)
        data["stage"] = _validate_stage(stage)

        response = self.client.patch('profile/stage', data=data)
        return response.json()


class ProfileRating():
    def __init__(self, api):
        self.client = api

    def set(self, source_id=None, profile_id=None, filter_id=None, rating=None, profile_reference=None, filter_reference=None):
        """
        Edit the profile rating given a filter

        Args:
            profile_id:             <string>
                                    profile id
        body params:
            source_id:              <string>
                                    source id associated to the profile

            filter_id:                 <string>
                                    filter id
            rating:                 <int32>
                                    profile rating from 1 to 4 associated to the filter.

        Returns:
            Response that contains code 201 if successful
            Other status codes otherwise.
        """
        data = {}
        data["source_id"] = _validate_source_id(source_id)
        if profile_id:
            data["profile_id"] = _validate_profile_id(profile_id)
        if filter_id:
            data["filter_id"] = _validate_filter_id(filter_id)
        if profile_reference:
            data["profile_reference"] = _validate_profile_reference(profile_reference)
        if filter_reference:
            data["filter_reference"] = _validate_filter_reference(filter_reference)
        data["rating"] = _validate_rating(rating)

        response = self.client.patch('profile/rating', data=data)
        return response.json()


class ProfileData():
    """Gathers route about structured profile."""

    def __init__(self, api):
        """Init."""
        self.client = api

    def check(self, profile_data, training_metadata=[]):
        """Use the api to check weither the profile_data are valid."""
        data = {
            "profile_json": profile_data,
            "training_metadata": training_metadata
        }
        response = self.client.post("profile/data/check", data=data)
        return response.json()

    def add(self, source_id, profile_data, training_metadata=[], profile_reference=None, timestamp_reception=None):
        """Use the api to add a new profile using profile_data."""
        data = {
            "source_id": _validate_source_id(source_id),
            "profile_json": profile_data,
            "training_metadata": training_metadata,
            "profile_reference": profile_reference,
            "timestamp_reception": timestamp_reception
        }
        response = self.client.post("profile/data", data=data)
        return response.json()


def _get_file_metadata(file_path, profile_reference):

    try:
        return (
            os.path.basename(file_path) + profile_reference,  # file_name
            None,
            magic.Magic(True).from_file(file_path)
        )
    except Exception as e:
        raise Exception(repr(e))


def _validate_training_metadata(value):
    if not isinstance(value, list):
        raise TypeError("training_metadata must be a list")
    return value


def _validate_source_ids(value):
    if not isinstance(value, list):
        raise TypeError("source_ids must be a list")

    if not value or not all(isinstance(elt, str) for elt in value):
        raise TypeError("source_ids must contain list of strings")

    return value


def _validate_source_id(value):
    if not isinstance(value, str) and value is not None:
        raise TypeError("source_id must be string")

    return value


def _validate_profile_id(value):
    if not isinstance(value, str) and value is not None:
        raise TypeError("source_id must be string")

    return value


def _validate_seniority(value):
    if value not in SERNIORITY_VALUES:
        raise ValueError("seniority value must be in {}".format(str(SERNIORITY_VALUES)))

    return value


def _validate_stage(value):
    if value not in STAGE_VALUES:
        raise ValueError("stage value must be in {}".format(str(STAGE_VALUES)))

    return value


def _validate_date_start(value):
    if not isinstance(value, str):
        raise TypeError("date_start must be string")

    return value


def _validate_date_end(value):
    if not isinstance(value, str):
        raise TypeError("date_end must be string")

    return value


def _validate_filter_id(value):
    if not isinstance(value, str) and value is not None:
        raise TypeError("filter_id must be string")

    return value


def _validate_filter_reference(value):
    if not isinstance(value, str) and value is not None:
        raise TypeError("filter_reference must be string")

    return value


def _validate_profile_reference(value):
    if not isinstance(value, str) and value is not None:
        raise TypeError("profile_reference must be string")

    return value


def _validate_page(value):
    if not isinstance(value, int):
        raise TypeError("page must be 'int'")

    return value


def _validate_limit(value):
    if not isinstance(value, int):
        raise TypeError("limit must be 'int'")

    return value


def _validate_rating(value):
    if not isinstance(value, int):
        raise TypeError("rating must be 'int'")

    return value


def _validate_sort_by(value):
    if value not in SORT_BY_VALUES:
        raise ValueError("sort_by value must be in {}".format(str(SORT_BY_VALUES)))

    return value


def _validate_timestamp_reception(value):
    if not isinstance(value, str) and value is not None:
        raise TypeError("timestamp_reception must be string")

    return value


def _is_valid_extension(file_path):
    ext = path.splitext(file_path)[1]
    if not ext:
        return False
    return ext in VALID_EXTENSIONS


def _is_valid_filename(file_path):
    name = path.basename(file_path)
    return name not in INVALID_FILENAME


def _get_files_from_dir(dir_path, is_recurcive):
    file_res = []
    files_path = os.listdir(dir_path)

    for file_path in files_path:
        true_path = path.join(dir_path, file_path)
        if path.isdir(true_path) and is_recurcive:
            if _is_valid_filename(true_path):
                file_res += _get_files_from_dir(true_path, is_recurcive)
            continue
        if _is_valid_extension(true_path):
            file_res.append(true_path)
    return file_res
