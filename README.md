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
Example Job 

```sh
    >>> from riminder import Riminder
    >>> from riminder.job import Job
    >>> client = Riminder(api_key="YOUR_API_KEY")
    >>> job = Job(self.client)
    >>> result = job.get_all()
    >>> print(result)
    {
        "code": 200,
        "message": "ok",
        "data": [
            {
            "job_id": "7c94e981cd23d16f5c549eea21a7554db0c927a7",
            "job_reference": "1248593",
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

* get_all()
Retreive all profiles that match the query param, only source_ids are required

```
    profile.get_all(source_ids, seniority, stage, date_start, date_end, job_id, page, limit, sort_by)
```

* create_profile()
Add a profile resume to a sourced id

```
    profile.create_profile(source_id, file_path, profile_reference, timestamp_reception)
```

* get_by_id()
Retrieve the profile information associated with profile id, source_id and profile_id are required

```
    profile.get_by_id(source_id, profile_id)
```

* get_documents()
Retrieve the profile information associated with profile id, source_id and profile_id are required

```
    profile.get_documents(source_id, profile_id)
```

* get_extractions()
Retrieve the profile career's path associated with profile id, source_id and profile_id are required

```
    profile.get_extractions(source_id, profile_id)
```

* get_extractions()
Retrieve the profile assessments associated with profile id, source_id and profile_id are required

```
    profile.get_jobs(source_id, profile_id)
```

* update_stage()
Edit the profile stage given a job, source_id, profile_id and job_id are required

```
    profile.update_stage(source_id, profile_id, job_id, stage)
```

* update_rating
Edit the profile rating given a job, all params are required

```
    profile.update_rating(source_id, profile_id, job_id, rating)
```


## Source

* get_all()
get all sources

```
    source.get_all()
```

* get_by_id()
Retrieve the source information associated with source id (required)

```
    source.get_by_id(source_id)
```

## job

* get_all()
Retrieve all jobs for given team account

```
    job.get_all()
```

* get_by_id()
Retrieve the job information associated with the job_id (required)

```
    job.get_by_id(job_id)
```


# Tests
All code is unit tested
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

# Todo

* All test must pass
* Adding webhooks