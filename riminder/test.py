import unittest
from riminder import Riminder
from profile import Profile


class TestProfile(unittest.TestCase):

    def setUp(self):
        self.client = Riminder(api_key="ask_ce813e1812ebeb663489abdad8b13aea")
        self.profile = Profile(self.client)

    def test_get_all(self):
        res = self.profile.get_all(source_ids=["5823bc959983f7a5925a5356020e60d605e8c9b5"])
        self.assertEqual(res["code"], 200)

    def test_filter_by_seniority(self):
        res = self.profile.get_all(
            source_ids=["5823bc959983f7a5925a5356020e60d605e8c9b5"],
            seniority="junior",
            limit=5
            )
        # Other params can be tested in the same manner
        self.assertEqual(res["code"], 200)
        self.assertEqual(len(res["data"]["profiles"]), 5)
        for profile in res["data"]["profiles"]:
            self.assertEqual(profile["seniority"], "junior")


if __name__ == '__main__':
    unittest.main()