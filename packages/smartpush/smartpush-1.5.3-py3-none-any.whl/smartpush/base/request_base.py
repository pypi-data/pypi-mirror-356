import requests


class RequestBase:
    def __init__(self, host, headers):
        """

        :param headers: 头，cookie
        :param host: 域名
        """
        self.host = host
        self.headers = headers
        self.request = requests.Request(headers=self.headers)
        self.post = requests.Request("POST", headers=self.headers)
        self.get = requests.Request("GET", headers=self.headers)


class FormRequestBase(RequestBase):
    def __init__(self, form_id, host, headers):
        super().__init__(host, headers)
        self.form_id = form_id

