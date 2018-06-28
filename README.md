# python-riminder-api
🐍 Riminder API Python Wrapper

# python2
  python2 package is available [here](https://github.com/Riminder/python-riminder-api/tree/masterpython2).

# Installation
The package is available for python3.5 >= or python2.7.*
```sh
$ pip3 install riminder
```
or
```sh
$ pip install riminder
```

# Usage

Example Source

```sh
    >>> import riminder
    >>> client = riminder.Riminder(api_key="YOUR_API_KEY")
    >>> result = client.source.list()
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
    >>> import riminder
    >>> client = riminder.Riminder(api_key="YOUR_API_KEY")
    >>> result = client.profile.list(source_ids=["source_id"])
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
    >>> import riminder
    >>> client = riminder.Riminder(api_key="YOUR_API_KEY")
    >>> result = client.filter.list()
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

For any methods that needs `*_id` and `*_reference`
you need to provide at least one of them but not necessarily both, keep in mind that reference override id.
## Profile

* profile.list().
Retreive all profiles that match the query param, only source_ids are required

```python
    client.profile.list(source_ids, seniority, stage, date_start, date_end, filter_id, page, limit, sort_by, filter_reference, order_by)
```

* profile.add().
Add a profile resume to a source id

```python
    client.profile.add(source_id, file_path, profile_reference, timestamp_reception, training_metadata)
```

* profile.addList().
Add all resume from a directory to a source id

```python
    response = client.profile.addList(source_id, file_path, is_recurcive, timestamp_reception, training_metadata)
    # file successfully sent
    serverResponse = response['success']['path/to/file']
    # file not sent
    error = response['fail']['path/to/file']
```

* profile.get().
Retrieve the profile information associated with profile id, source_id and profile_id are required

```python
    client.profile.get(source_id, profile_id, profile_reference)
```

* profile.document.list().
Retrieve the profile information associated with profile id, source_id and profile_id are required

```python
    client.profile.document.list(source_id, profile_id, profile_reference)
```

* profile.parsing.get().
Retrieve the profile parsing data path associated with profile id, source_id and profile_id are required

```python
    client.profile.parsing.get(source_id, profile_id, profile_reference)
```

* profile.scoring.list().
Retrieve the profile scoring associated with profile id, source_id and profile_id are required

```python
    client.profile.scoring.list(source_id, profile_id)
```

* profile.stage.set().
Edit the profile stage given a filter, source_id, profile_id and filter_id are required

```python
    client.profile.stage.set(source_id, profile_id, filter_id, stage, profile_reference, filter_reference)
```

* profile.rating.set().
Edit the profile rating given a filter, all params are required

```python
    client.profile.rating.set(source_id, profile_id, filter_id, rating, profile_reference, filter_reference)
```


## Source

* source.list().
get all sources

```python
    client.source.list()
```

* source.get().
Retrieve the source information associated with source id (required)

```python
    client.source.get(source_id)
```

## filter

* filter.list().
Retrieve all filters for given team account

```python
    client.filter.list()
```

* filter.get().
Retrieve the filter information associated with the filter_id (required)

```python
    client.filter.get(filter_id, filter_reference)
```


# Tests

All code is unit tested.
To run the test, please follow these steps
* `git clone https://github.com/Riminder/python-riminder-api`
* From your python virtual environment navigate to the project directory and install requirements
```sh
$ pip3 install -r requirements.txt
```
or
```sh
$ pip install -r requirements.txt
```
* run test
```sh
$ ./run_test
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
