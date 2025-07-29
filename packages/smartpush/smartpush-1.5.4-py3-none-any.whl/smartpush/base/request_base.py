import json

import requests
from requests import session
from requests.adapters import HTTPAdapter
from tenacity import stop_after_attempt, wait_fixed, retry
from urllib3 import Retry

from smartpush.export.basic.GetOssUrl import log_attempt


class RequestBase:
    def __init__(self, host, headers, retries=3, **kwargs):
        """

        :param headers: 头，cookie
        :param host: 域名
        """
        self.host = host
        self.headers = headers

        # 配置重试策略
        retry_strategy = Retry(
            total=retries,
            status_forcelist=[429, 500, 502, 503, 504],
            backoff_factor=1
        )

        # 创建 Session 并配置适配器
        self.session = requests.Session()
        self.session.mount("https://", HTTPAdapter(max_retries=retry_strategy))

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2), after=log_attempt)
    def request(self, method, path, **kwargs):
        url = f"{self.host}{path}"
        print(f"{method} 请求：", url)
        # 统一处理请求参数
        default_kwargs = {
            "timeout": 30,
            "headers": self.headers
        }
        default_kwargs.update(kwargs)
        if default_kwargs.get('data'): # 如果data有值json序列化
            data = json.dumps(default_kwargs.get('data'))
            default_kwargs.update({'data': data})
        try:
            response = self.session.request(method, url, **default_kwargs)
            response.raise_for_status()
            print("响应内容为：\n", response.json())
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"请求失败: {e}")
            return None


class FormRequestBase(RequestBase):
    def __init__(self, form_id, host, headers):
        super().__init__(host, headers)
        self.form_id = form_id
