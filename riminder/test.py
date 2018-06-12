import unittest
from riminder import Riminder
from profile import Profile
from source import Source
from filter import Filter


class TestHelper:
    def __init__(self):
        self.api_key = ""
        self.source_id = None
        self.add_source_id = None
        self.profile_id = None
        self.filter_id = None
        self.rating = int(1)
        self.stage = 'NEW'
        self.source_type = 'api'
        # if source_name is empty no name is selected
        self.source_name = []

    def getKey(self):
        return self.api_key

    def setup(self):
        api = Riminder(api_key=self.api_key)
        api_source = Source(api)
        api_profile = Profile(api)
        res = api_source.get_all()
        for source in res['data']:
            name = False
            type = False
            if source['type'] == self.source_type:
                source_type = True
            if self.source_name and source['name'] in self.source_name:
                name = True
            if name and source_type:
                self.add_source_id = str(source['source_id'])
                break
        if self.add_source_id is None:
            raise ValueError('no api test source found')
        self.source_id = str(res['data'][0]['source_id'])
        res = api_profile.get_all(source_ids=[self.source_id])
        if not res['data']['profiles']:
            raise ValueError('no profiles found')
        profiles = res['data']['profiles']
        for profile in profiles:
            profile_id = str(profile['profile_id'])
            res = api_profile.get_scoring(source_id=self.source_id, profile_id=profile_id)
            if res['code'] != 200 or not res['data']:
                continue
            self.profile_id = profile_id
            self.filter_id = str(res['data'][0]['filter_id'])
            if res['data'][0]['rating'] is not None:
                self.rating = int(res['data'][0]['rating'])
            if res['data'][0]['stage'] is not None:
                self.stage = str(res['data'][0]['stage'])
            break
        if self.profile_id is None:
            raise ValueError('no valid profiles found...')


class TestProfile(unittest.TestCase):

    def setUp(self):
        self.helper = TestHelper()
        self.helper.setup()
        # init client and profile objects
        self.client = Riminder(api_key=self.helper.getKey())
        self.profile = Profile(self.client)

    def test_get_all(self):
        # get all profiles
        res = self.profile.get_all(source_ids=[self.helper.source_id])

        # print(res)
        self.assertEqual(res["code"], 200)

    def test_filter_by_seniority_and_limit_response_size(self):
        # filter profiles by seniority and limit
        # other params can be tested in the same manner
        res = self.profile.get_all(
            source_ids=[self.helper.source_id],
            seniority="junior",
            limit=5
            )
        self.assertEqual(res["code"], 200)
        self.assertLessEqual(len(res["data"]["profiles"]), 5)
        for profile in res["data"]["profiles"]:
            self.assertEqual(profile["seniority"], "junior")

    def test_create_profile(self):
        file_path = "riminder/test_assets/file.pdf"
        res = self.profile.create_profile(
            source_id=self.helper.add_source_id,
            file_path=file_path,
        )
        self.assertEqual(res["code"], 201)

    def test_create_profiles(self):
        dir_path = "riminder/test_assets"
        res = self.profile.create_profiles(source_id=self.helper.add_source_id, dir_path=dir_path)
        self.assertEqual(len(res['success']), 1)

    def test_get_one_profile(self):
        res = self.profile.get_by_id(
            source_id=self.helper.source_id,
            profile_id=self.helper.profile_id,
        )
        self.assertEqual(res["code"], 200)

    def test_get_documents(self):
        res = self.profile.get_documents(
            source_id=self.helper.source_id,
            profile_id=self.helper.profile_id,
        )

        self.assertEqual(res["code"], 200)

    def test_get_parsing(self):
        res = self.profile.get_parsing(
            source_id=self.helper.source_id,
            profile_id=self.helper.profile_id,
        )

        self.assertEqual(res["code"], 200)

    def test_get_scoring(self):
        res = self.profile.get_scoring(
            source_id=self.helper.source_id,
            profile_id=self.helper.profile_id,
        )

        self.assertEqual(res["code"], 200)

    def test_update_stage(self):
        res = self.profile.update_stage(
            source_id=self.helper.source_id,
            profile_id=self.helper.profile_id,
            filter_id=self.helper.filter_id,
            stage=self.helper.stage,
        )
        self.assertEqual(res["code"], 200)

    def test_update_rating(self):
        res = self.profile.update_rating(
            source_id=self.helper.source_id,
            profile_id=self.helper.profile_id,
            filter_id=self.helper.filter_id,
            rating=int(self.helper.rating),
        )
        # print(res)

        self.assertEqual(res["code"], 200)


class TestSource(unittest.TestCase):

    def setUp(self):
        self.helper = TestHelper()
        self.helper.setup()
        # init client and profile objects
        self.client = Riminder(api_key=self.helper.getKey())
        self.source = Source(self.client)

    def test_get_all(self):
        # get all sources
        res = self.source.get_all()

        # print(res)
        self.assertEqual(res["code"], 200)

    def test_get_one_profile(self):
        # get one source by id
        res = self.source.get_by_id(
            source_id=self.helper.source_id
        )
        # print(res)
        self.assertEqual(res["code"], 200)


class TestFilter(unittest.TestCase):

    def setUp(self):
        self.helper = TestHelper()
        self.helper.setup()
        # init client and filter objects
        self.client = Riminder(api_key=self.helper.getKey())
        self.filter = Filter(self.client)

    def test_get_all(self):
        # get all filters
        res = self.filter.get_all()

        # print(res)
        self.assertEqual(res["code"], 200)

    def test_get_one_filter(self):
        # get one filter by id
        res = self.filter.get_by_id(
            filter_id=self.helper.filter_id
        )
        # print(res)
        self.assertEqual(res["code"], 200)


if __name__ == '__main__':
    unittest.main()
