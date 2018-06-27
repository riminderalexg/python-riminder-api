import unittest
import hmac
import hashlib
import base64
import json

from riminder import Riminder
from webhook import EVENT_FILTER_SCORE_ERROR


class TestHelper:
    def __init__(self):
        self.api_key = ""
        self.webhook_secret = 'totaly_a_valid_secret_key'
        self.source_id = None
        self.add_source_id = None
        self.profile_id = None
        self.profile_ref = None
        self.filter_id = None
        self.filter_ref = None
        self.rating = int(1)
        self.stage = 'NEW'
        self.source_type = 'api'
        # if source_name is empty no name is selected
        self.source_name = []

    def getKey(self):
        return self.api_key

    def getWebhookSecret(self):
        return self.webhook_secret

    def setup(self):
        api = Riminder(api_key=self.api_key)
        res = api.source.list()
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
        self.source_id = self.add_source_id
        res = api.profile.list(source_ids=[self.source_id])
        if not res['data']['profiles']:
            raise ValueError('no profiles found')
        profiles = res['data']['profiles']
        for profile in profiles:
            profile_id = str(profile['profile_id'])
            res = api.profile.scoring.list(source_id=self.source_id, profile_id=profile_id)
            if res['code'] != 200 or not res['data']:
                continue
            for scoring in res['data']:
                if scoring['filter_reference'] is None:
                    continue
                self.profile_id = profile_id
                self.profile_ref = profile['profile_reference']
                self.filter_id = str(scoring['filter_id'])
                self.filter_ref = str(scoring['filter_reference'])
                if scoring['rating'] is not None:
                    self.rating = int(scoring['rating'])
                if scoring['stage'] is not None:
                    self.stage = str(scoring['stage'])
                break
            # keep a valid profile but keep looking until one with a reference
            # is found.
            if not profile['profile_reference']:
                continue
            break
        if self.profile_id is None:
            raise ValueError('no valid profiles found...')

    def gen_err_msg(self, resp):
        return "Response invalid: " + str(resp)

    def gen_webhook_request(self, type):
        data = {
            'type': type,
            'message': 'pou lou lou',
            'profile': {'profile_id': '1', 'profile_reference': 'I\'m free'}
        }
        json_data = json.dumps(data)
        webhook_secret = bytes(self.webhook_secret, 'ascii')
        json_data = bytes(json_data, 'utf8')
        hasher = hmac.new(webhook_secret, json_data, hashlib.sha256)
        encoded_sign = bytes(hasher.hexdigest(), 'ascii')
        byte_encoded_sign = base64.encodebytes(encoded_sign)
        byte_json_data = base64.encodebytes(json_data)
        sign = '{}.{}'.format(byte_encoded_sign.decode('ascii'), byte_json_data.decode('ascii'))
        res = {'HTTP_RIMINDER_SIGNATURE': sign}
        return res


class TestProfile(unittest.TestCase):

    def setUp(self):
        self.helper = TestHelper()
        self.helper.setup()
        # init client and profile objects
        self.client = Riminder(api_key=self.helper.getKey())

    def test_get_profiles(self):
        # get all profiles
        res = self.client.profile.list(source_ids=[self.helper.source_id])

        # print(res)
        self.assertEqual(res["code"], 200, msg=self.helper.gen_err_msg(res))

    def test_filter_by_seniority_and_limit_response_size(self):
        # filter profiles by seniority and limit
        # other params can be tested in the same manner
        res = self.client.profile.list(
            source_ids=[self.helper.source_id],
            seniority="junior",
            limit=5
            )
        self.assertEqual(res["code"], 200, msg=self.helper.gen_err_msg(res))
        self.assertLessEqual(len(res["data"]["profiles"]), 5)
        for profile in res["data"]["profiles"]:
            self.assertEqual(profile["seniority"], "junior")

    def test_post_profile(self):
        file_path = "riminder/test_assets/cv_test5.pdf"
        res = self.client.profile.add(
            source_id=self.helper.add_source_id,
            file_path=file_path,
        )
        self.assertEqual(res["code"], 201, msg=self.helper.gen_err_msg(res))

    def test_post_profiles(self):
        dir_path = "riminder/test_assets/"
        res = self.client.profile.addList(source_id=self.helper.add_source_id, dir_path=dir_path, is_recurcive=True)
        if len(res['fail']) > 0:
            for kf, failed in res['fail'].items():
                print('failed send: {}->{}\n', kf, failed)
        self.assertEqual(len(res['success']), 2)

    def test_get_profile(self):
        res = self.client.profile.get(
            source_id=self.helper.source_id,
            profile_id=self.helper.profile_id,
        )
        self.assertEqual(res["code"], 200, msg=self.helper.gen_err_msg(res))

    def test_get_profile_ref(self):
        res = self.client.profile.get(
            source_id=self.helper.source_id,
            profile_reference=self.helper.profile_ref,
        )
        errMessage = ""
        if not self.helper.profile_ref:
            errMessage = "No profile reference found: " + self.helper.gen_err_msg(res)
        self.assertEqual(res["code"], 200, msg=errMessage)

    def test_get_documents(self):
        res = self.client.profile.document.list(
            source_id=self.helper.source_id,
            profile_id=self.helper.profile_id,
        )

        self.assertEqual(res["code"], 200, msg=self.helper.gen_err_msg(res))

    def test_get_documents_ref(self):
        res = self.client.profile.document.list(
            source_id=self.helper.source_id,
            profile_reference=self.helper.profile_ref,
        )
        errMessage = ""
        if not self.helper.profile_ref:
            errMessage = "No profile reference found: " + self.helper.gen_err_msg(res)
        self.assertEqual(res["code"], 200, msg=errMessage)

    def test_get_parsing(self):
        res = self.client.profile.parsing.get(
            source_id=self.helper.source_id,
            profile_id=self.helper.profile_id,
        )

        self.assertEqual(res["code"], 200, msg=self.helper.gen_err_msg(res))

    def test_get_parsing_ref(self):
        res = self.client.profile.parsing.get(
            source_id=self.helper.source_id,
            profile_reference=self.helper.profile_ref,
        )
        errMessage = ""
        if not self.helper.profile_ref:
            errMessage = "No profile reference found: " + self.helper.gen_err_msg(res)
        self.assertEqual(res["code"], 200, msg=errMessage)

    def test_get_scoring(self):
        res = self.client.profile.scoring.list(
            source_id=self.helper.source_id,
            profile_id=self.helper.profile_id,
        )

        self.assertEqual(res["code"], 200, msg=self.helper.gen_err_msg(res))

    def test_get_scoring_ref(self):
        res = self.client.profile.scoring.list(
            source_id=self.helper.source_id,
            profile_reference=self.helper.profile_ref,
        )
        errMessage = ""
        if not self.helper.profile_ref:
            errMessage = "No profile reference found: " + self.helper.gen_err_msg(res)
        self.assertEqual(res["code"], 200, msg=errMessage)

    def test_update_stage(self):
        res = self.client.profile.stage.set(
            source_id=self.helper.source_id,
            profile_id=self.helper.profile_id,
            filter_id=self.helper.filter_id,
            stage=self.helper.stage,
        )
        self.assertEqual(res["code"], 200, msg=self.helper.gen_err_msg(res))

    def test_update_stage_ref(self):
        res = self.client.profile.stage.set(
            source_id=self.helper.source_id,
            profile_reference=self.helper.profile_ref,
            filter_reference=self.helper.filter_ref,
            stage=self.helper.stage,
        )
        errMessage = self.helper.gen_err_msg(res)
        if not self.helper.profile_ref or not self.helper.filter_ref:
            errMessage = "No profile reference found: " + self.helper.gen_err_msg(res)
        self.assertEqual(res["code"], 200, msg=errMessage)

    def test_update_rating(self):
        res = self.client.profile.rating.set(
            source_id=self.helper.source_id,
            profile_id=self.helper.profile_id,
            filter_id=self.helper.filter_id,
            rating=int(self.helper.rating),
        )
        self.assertEqual(res["code"], 200, msg=self.helper.gen_err_msg(res))

    def test_update_rating_ref(self):
        res = self.client.profile.rating.set(
            source_id=self.helper.source_id,
            profile_reference=self.helper.profile_ref,
            filter_reference=self.helper.filter_ref,
            rating=int(self.helper.rating),
        )
        errMessage = self.helper.gen_err_msg(res)
        if not self.helper.profile_ref or not self.helper.filter_ref:
            errMessage = "No profile reference found: " + self.helper.gen_err_msg(res)
        self.assertEqual(res["code"], 200, msg=errMessage)


class TestSource(unittest.TestCase):

    def setUp(self):
        self.helper = TestHelper()
        self.helper.setup()
        # init client and profile objects
        self.client = Riminder(api_key=self.helper.getKey())

    def test_get_sources(self):
        # get all sources
        res = self.client.source.list()

        # print(res)
        self.assertEqual(res["code"], 200, msg=self.helper.gen_err_msg(res))

    def test_get_source(self):
        # get one source by id
        res = self.client.source.get(
            source_id=self.helper.source_id
        )
        # print(res)
        self.assertEqual(res["code"], 200, msg=self.helper.gen_err_msg(res))


class TestFilter(unittest.TestCase):

    def setUp(self):
        self.helper = TestHelper()
        self.helper.setup()
        # init client and filter objects
        self.client = Riminder(api_key=self.helper.getKey())

    def test_get_filters(self):
        # get all filters
        res = self.client.filter.list()

        # print(res)
        self.assertEqual(res["code"], 200, msg=self.helper.gen_err_msg(res))

    def test_get_filter(self):
        # get one filter by id
        res = self.client.filter.get(
            filter_id=self.helper.filter_id
        )
        # print(res)
        self.assertEqual(res["code"], 200, msg=self.helper.gen_err_msg(res))

    def test_get_filter_ref(self):
        # get one filter by ref
        res = self.client.filter.get(
            filter_reference=self.helper.filter_ref
        )
        # print(res)
        self.assertEqual(res["code"], 200, msg=self.helper.gen_err_msg(res))


class TestWebhook(unittest.TestCase):

    last_evt_type = None
    last_decoded_request = None

    @staticmethod
    def handler(event_type, decoded_request):
        TestWebhook.last_evt_type = event_type
        TestWebhook.last_decoded_request = decoded_request

    def setUp(self):
        self.helper = TestHelper()
        self.helper.setup()
        self.client = Riminder(api_key=self.helper.getKey(), webhook_secret=self.helper.getWebhookSecret())

    def test_post_check(self):
        res = self.client.webhook.check()
        self.assertEqual(res['code'], 200, msg=self.helper.gen_err_msg(res))

    def test_handle_request(self):
        self.client.webhook.setHandler(EVENT_FILTER_SCORE_ERROR, TestWebhook.handler)
        webhook_req = self.helper.gen_webhook_request(EVENT_FILTER_SCORE_ERROR)
        self.client.webhook.handleRequest(webhook_req['HTTP_RIMINDER_SIGNATURE'])
        self.assertEqual(TestWebhook.last_evt_type, EVENT_FILTER_SCORE_ERROR)
        if 'profile' not in TestWebhook.last_decoded_request:
            self.fail('Resquest is not full.')


if __name__ == '__main__':
    unittest.main()
