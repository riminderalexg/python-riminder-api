import unittest
from riminder import Riminder
from profile import Profile
from source import Source
from filter import Filter


class TestProfile(unittest.TestCase):

    def setUp(self):
        # init client and profile objects
        self.client = Riminder(api_key="ask_ce813e1812ebeb663489abdad8b13aea")
        self.profile = Profile(self.client)

    def test_get_all(self):
        # get all profiles
        res = self.profile.get_all(source_ids=["5823bc959983f7a5925a5356020e60d605e8c9b5"])

        # print(res)
        self.assertEqual(res["code"], 200)

    def test_filter_by_seniority_and_limit_response_size(self):
        # filter profiles by seniority and limit
        # other params can be tested in the same manner
        res = self.profile.get_all(
            source_ids=["5823bc959983f7a5925a5356020e60d605e8c9b5"],
            seniority="junior",
            limit=5
            )

        self.assertEqual(res["code"], 200)
        self.assertEqual(len(res["data"]["profiles"]), 5)
        for profile in res["data"]["profiles"]:
            self.assertEqual(profile["seniority"], "junior")

    def test_create_profile(self):
        file_path = "riminder/test_assets/file.pdf"
        res = self.profile.create_profile(
            source_id="5823bc959983f7a5925a5356020e60d605e8c9b5",
            file_path=file_path,
        )
        self.assertEqual(res["code"], 201)

    def test_get_one_profile(self):
        res = self.profile.get_by_id(
            source_id="5823bc959983f7a5925a5356020e60d605e8c9b5",
            profile_id="5d20da1c2d7bb0a6956764a8b0b61c0371540ce6",
        )
        self.assertEqual(res["code"], 200)

    def test_get_documents(self):
        res = self.profile.get_documents(
            source_id="5823bc959983f7a5925a5356020e60d605e8c9b5",
            profile_id="5d20da1c2d7bb0a6956764a8b0b61c0371540ce6",
        )

        self.assertEqual(res["code"], 200)

    def test_get_parsing(self):
        res = self.profile.get_parsing(
            source_id="5823bc959983f7a5925a5356020e60d605e8c9b5",
            profile_id="5d20da1c2d7bb0a6956764a8b0b61c0371540ce6",
        )

        self.assertEqual(res["code"], 200)

    def test_get_scoring(self):
        res = self.profile.get_scoring(
            source_id="5823bc959983f7a5925a5356020e60d605e8c9b5",
            profile_id="5d20da1c2d7bb0a6956764a8b0b61c0371540ce6",
        )

        self.assertEqual(res["code"], 200)

    def test_update_stage(self):
        res = self.profile.update_stage(
            source_id="5823bc959983f7a5925a5356020e60d605e8c9b5",
            profile_id="5d20da1c2d7bb0a6956764a8b0b61c0371540ce6",
            filter_id="4f391e19bb02cb60eb81b31b31b177296ecd5208",
            stage="NEW",
        )
        # print(res)
        self.assertEqual(res["code"], 200)

    def test_update_rating(self):
        res = self.profile.update_rating(
            source_id="5823bc959983f7a5925a5356020e60d605e8c9b5",
            profile_id="5d20da1c2d7bb0a6956764a8b0b61c0371540ce6",
            filter_id="4f391e19bb02cb60eb81b31b31b177296ecd5208",
            rating=1,
        )
        # print(res)

        self.assertEqual(res["code"], 200)


class TestSource(unittest.TestCase):

    def setUp(self):
        # init client and profile objects
        self.client = Riminder(api_key="ask_ce813e1812ebeb663489abdad8b13aea")
        self.source = Source(self.client)

    def test_get_all(self):
        # get all sources
        res = self.source.get_all()

        # print(res)
        self.assertEqual(res["code"], 200)

    def test_get_one_profile(self):
        # get one source by id
        res = self.source.get_by_id(
            source_id="5823bc959983f7a5925a5356020e60d605e8c9b5"
        )
        # print(res)
        self.assertEqual(res["code"], 200)


class TestFilter(unittest.TestCase):

    def setUp(self):
        # init client and filter objects
        self.client = Riminder(api_key="ask_ce813e1812ebeb663489abdad8b13aea")
        self.filter = Filter(self.client)

    def test_get_all(self):
        # get all filters
        res = self.filter.get_all()

        # print(res)
        self.assertEqual(res["code"], 200)

    def test_get_one_filter(self):
        # get one filter by id
        res = self.filter.get_by_id(
            filter_id="4f391e19bb02cb60eb81b31b31b177296ecd5208"
        )
        # print(res)
        self.assertEqual(res["code"], 200)


if __name__ == '__main__':
    unittest.main()
