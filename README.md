# python-riminder-api
🐍 Riminder API Python Wrapper


# Installation

```sh
$ pip install riminder
```

# Usage

Example Source

```sh
    >>> from riminder import Riminder
    >>> from riminder.source import Source
    >>> client = Riminder(api_key="YOUR_API_KEY")
    >>> Source = Source(self.client)
    >>> result = source.get_all()
    >>> print(result)
    {
    "code": 200,
    "message": "ok",
    "data": [
        {
        "_id": "7c94e981cd23d16f5c549eea21a7554db0c927a7",
        "name": "Careers website",
        "type": "api",
        "archive": false
        ...

```

Example Profile

```sh
    >>> from riminder import Riminder
    >>> from riminder.profile import Profile
    >>> client = Riminder(api_key="YOUR_API_KEY")
    >>> profile = Profile(self.client)
    >>> result = profile.get_all(source_ids=["source_id"])
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

```
Example Filter

```sh
    >>> from riminder import Riminder
    >>> from riminder.filter import Filter
    >>> client = Riminder(api_key="YOUR_API_KEY")
    >>> filter = Filter(self.client)
    >>> result = filter.get_all()
    >>> print(result)
    {
        "code": 200,
        "message": "ok",
        "data": [
            {
            "filter_id": "7c94e981cd23d16f5c549eea21a7554db0c927a7",
            "filter_reference": "1248593",
            "name": "Talent Acquisition Specialist",
            "archive": false,
            "date_creation": {
                "date": "2017-07-27 18:49:41.000000",
                "timezone_type": 3,
                "timezone": "Europe/Paris"
            ...

```

# API

## Profile

* get_all().
Retreive all profiles that match the query param, only source_ids are required

```
    profile.get_all(source_ids, seniority, stage, date_start, date_end, filter_id, page, limit, sort_by, filter_reference, order_by)
```

* create_profile().
Add a profile resume to a sourced id

```
    profile.create_profile(source_id, file_path, profile_reference, timestamp_reception, training_metadata)
```

* get_by_id().
Retrieve the profile information associated with profile id, source_id and profile_id are required

```
    profile.get_by_id(source_id, profile_id, profile_reference)
```

* get_documents().
Retrieve the profile information associated with profile id, source_id and profile_id are required

```
    profile.get_documents(source_id, profile_id, profile_reference)
```

* get_parsing().
Retrieve the profile parsing data path associated with profile id, source_id and profile_id are required

```
    profile.get_extractions(source_id, profile_id, profile_reference)
```

* get_scoring().
Retrieve the profile scoring associated with profile id, source_id and profile_id are required

```
    profile.get_filters(source_id, profile_id)
```

* update_stage().
Edit the profile stage given a filter, source_id, profile_id and filter_id are required

```
    profile.update_stage(source_id, profile_id, filter_id, stage, profile_reference, filter_reference)
```

* update_rating.
Edit the profile rating given a filter, all params are required

```
    profile.update_rating(source_id, profile_id, filter_id, rating, profile_reference, filter_reference)
```


## Source

* get_all().
get all sources

```
    source.get_all()
```

* get_by_id().
Retrieve the source information associated with source id (required)

```
    source.get_by_id(source_id)
```

## filter

* get_all().
Retrieve all filters for given team account

```
    filter.get_all()
```

* get_by_id().
Retrieve the filter information associated with the filter_id (required)

```
    filter.get_by_id(filter_id, filter_reference)
```


# Tests

All code is unit tested.
To run the test, please follow these steps
* `git clone https://github.com/Riminder/python-riminder-api`
* From your python virtual environment navigate to the project directory and install requirements
```sh
$ pip install -r requirements.txt
```
* run test
```sh
$ python riminder/test.py
```

# Help

* Here an example on how to get help:

 ```sh
    >>> from riminder import Riminder
    >>> from riminder.profile import Profile
    >>> help(Profile.update_rating)

    Help on function update_rating in module riminder.profile:

    update_rating(self, source_id=None, profile_id=None, filter_id=None, rating=None)
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
(END)

```

* More help ? see  [Riminder API Docs](https://developers.riminder.net/v1.0/reference#authentication)

# Todo

* Finishing docstrings
* All test must pass
* Adding webhooks
