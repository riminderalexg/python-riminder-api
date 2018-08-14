"""Exeption raise by the package."""


class RiminderError(Exception):
    """Base Exception for riminder errors."""

    def __init__(self, message):
        """Init."""
        Exception.__init__(self, message)


class RiminderResponseError(RiminderError):
    """Error when response is invalid."""

    def __init__(self, response):
        """Init."""
        self.status_code = response.status_code
        self.reason = response.reason
        self.url = response.url
        self.response = response
        self.api_message = "..."
        try:
            tmp = response.json()
            if tmp is not None and "message" in tmp:
                self.api_message = tmp["message"]
        except Exception as e:
            self.api_message = "Can't parse api message: {}".format(e)
        self.mess = "Invalid response: {} -> {} ({})".format(self.status_code, self.reason, self.api_message)
        Exception.__init__(self, self.mess)


class RiminderRequestTransfertError(RiminderError):
    """Error while request handling."""

    def __init__(self, exp, exp_trace):
        """Init."""
        self.req_error = exp
        RiminderError.__init__(self, "Error during handling request: {}".format(exp_trace))
