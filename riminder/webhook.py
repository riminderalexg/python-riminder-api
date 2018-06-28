"""Webhook support."""
import hmac
import hashlib
import base64
import json

EVENT_PROFILE_PARSE_SUCCESS = 'profile.parse.success'
EVENT_PROFILE_PARSE_ERROR = 'profile.parse.error'
EVENT_PROFILE_SCORE_SUCCESS = 'profile.score.success'
EVENT_PROFILE_SCORE_ERROR = 'profile.score.error'
EVENT_FILTER_TRAIN_SUCCESS = 'filter.train.success'
EVENT_FILTER_TRAIN_ERROR = 'filter.train.error'
EVENT_FILTER_SCORE_SUCCESS = 'filter.score.success'
EVENT_FILTER_SCORE_ERROR = 'filter.score.error'
SIGNATURE_HEADER = 'HTTP-RIMINDER-SIGNATURE'


class Webhook(object):
    """Class that handles Webhooks."""

    def __init__(self, client):
        """Init."""
        self.client = client
        self.handlers = {
            EVENT_PROFILE_PARSE_SUCCESS: None,
            EVENT_PROFILE_PARSE_ERROR: None,
            EVENT_PROFILE_SCORE_SUCCESS: None,
            EVENT_PROFILE_SCORE_ERROR: None,
            EVENT_FILTER_TRAIN_SUCCESS: None,
            EVENT_FILTER_TRAIN_ERROR: None,
            EVENT_FILTER_SCORE_SUCCESS: None,
            EVENT_FILTER_SCORE_ERROR: None,
        }

    def check(self):
        """Get response from api for POST webhook/check."""
        response = self.client.post("webhook/check")
        return response.json()

    def setHandler(self, event_name, callback):
        """Set an handler for given event."""
        if event_name not in self.handlers:
            raise ValueError('{} is not a valid event'.format(event_name))
        if callable(event_name):
            raise TypeError('{} is not callable'.format(callback))
        self.handlers[event_name] = callback

    def isHandlerPresent(self, event_name):
        """Check if an event has an handler."""
        if event_name not in self.handlers:
            raise ValueError('{} is not a valid event'.format(event_name))
        return self.handlers[event_name] is not None

    def removeHandler(self, event_name):
        """Remove handler for given event."""
        if event_name not in self.handlers:
            raise ValueError('{} is not a valid event'.format(event_name))
        self.handlers[event_name] = None

    def _strtr(self, inp, fr, to):
        res = ''
        for c in inp:
            for idx, c_to_replace in enumerate(fr):
                if c == c_to_replace and idx < len(to):
                    c = to[idx]
            res = res + c
        return res

    def _get_signature_header(self, signature_header, request_headers):
        if signature_header is not None:
            return signature_header
        if SIGNATURE_HEADER in request_headers:
            return request_headers[SIGNATURE_HEADER]
        raise ValueError('Error: No {} given'.format(SIGNATURE_HEADER))

    def handleRequest(self, signature_header=None, request_headers={}):
        """Handle request."""
        if self.client.webhook_secret is None:
            raise ValueError('Error: no webhook secret.')
        encoded_header = self._get_signature_header(signature_header, request_headers)
        decoded_request = self._decode_request(encoded_header)
        if 'type' not in decoded_request:
            raise ValueError("Error invalid request: no type field found.")
        handler = self._getHandlerForEvent(decoded_request['type'])
        if handler is None:
            return
        handler(decoded_request['type'], decoded_request)

    def _base64Urldecode(self, inp):
        inp = self._strtr(inp, '-_', '+/')
        byte_inp = base64.b64decode(bytearray(inp, 'ascii'))
        return byte_inp.decode('ascii')

    def _is_signature_valid(self, signature, payload):
        utf8_payload = bytearray(payload, 'utf8')
        utf8_wb_secret = bytearray(self.client.webhook_secret, 'utf8')
        hasher = hmac.new(utf8_wb_secret, utf8_payload, hashlib.sha256)
        exp_sign_digest = hasher.hexdigest()

        if exp_sign_digest == signature:
            return True
        return False

    def _decode_request(self, encoded_request):
        tmp = encoded_request.split('.', 2)
        if len(tmp) < 2:
            raise ValueError("Error invalid request. Maybe it's not the 'HTTP-RIMINDER-SIGNATURE' field")
        encoded_sign = tmp[0]
        payload = tmp[1]
        sign = self._base64Urldecode(encoded_sign)
        data = self._base64Urldecode(payload)
        if not self._is_signature_valid(sign, data):
            raise ValueError("Error: invalid signature.")
        return json.loads(data)

    def _getHandlerForEvent(self, event_name):
        if event_name not in self.handlers:
            raise ValueError('{} is not a valid event'.format(event_name))
        handler = self.handlers[event_name]
        return handler
