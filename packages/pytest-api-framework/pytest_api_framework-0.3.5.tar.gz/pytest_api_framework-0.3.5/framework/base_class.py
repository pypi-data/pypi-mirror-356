import traceback
from urllib.parse import urlparse, urlunparse, urljoin

import pytest
from box import Box

from framework.utils.log_util import logger
from framework.db.mysql_db import MysqlDB
from framework.db.redis_db import RedisDB
from framework.exit_code import ExitCode
from framework.http_client import ResponseUtil
from framework.global_attribute import CONFIG, GlobalAttribute


class BaseTestCase(object):
    context: GlobalAttribute = None
    config: GlobalAttribute = None
    http = None
    data: Box = None
    scenario: Box = None
    belong_app = None
    response: ResponseUtil = None

    def request(self, app=None, *, account, data, **kwargs):
        try:
            app = self.default_app(app)
            app_http = getattr(self.http, app)
            domain = self.context.get(app).get("domain")
            data.request.url = self.replace_domain(data.request.url, domain)
            self.response = getattr(app_http, account).request(data=data, keyword=kwargs)
            return self.response
        except AttributeError as e:
            logger.error(f"app {app} or account {account} no exist: {e}")
            traceback.print_exc()
            pytest.exit(ExitCode.APP_OR_ACCOUNT_NOT_EXIST)
            return None

    def post(self, app, account, url, data=None, json=None, **kwargs):
        domain = self.context.get(app).get("domain")
        url = urljoin(domain, url)
        return getattr(getattr(self.http, app), account).post(app, url, data=data, json=json, **kwargs)

    def get(self, app, account, url, params=None, **kwargs):
        domain = self.context.get(app).get("domain")
        url = urljoin(domain, url)
        return getattr(getattr(self.http, app), account).get(app, url, params=params, **kwargs)

    def put(self, app, account, url, data=None, **kwargs):
        domain = self.context.get(app).get("domain")
        url = urljoin(domain, url)
        return getattr(getattr(self.http, app), account).put(app, url, data=data, **kwargs)

    def delete(self, app, account, url, **kwargs):
        domain = self.context.get(app).get("domain")
        url = urljoin(domain, url)
        return getattr(getattr(self.http, app), account).delete(app, url, **kwargs)

    def mysql_conn(self, db, app=None):
        try:
            config = CONFIG.get(app=self.default_app(app), key="mysql")
            config["db"] = db
            return MysqlDB(**config)
        except AttributeError:
            traceback.print_exc()
            pytest.exit(ExitCode.LOAD_DATABASE_INFO_ERROR)

    def redis_conn(self, db, app=None):
        try:
            config = CONFIG.get(app=self.default_app(app), key="redis")
            config["db"] = db
            return RedisDB(**config)
        except AttributeError:
            traceback.print_exc()
            pytest.exit(ExitCode.LOAD_DATABASE_INFO_ERROR)

    def contest_set(self, key, value):
        self.context.set(app=self.belong_app, key=key, value=value)

    def contest_get(self, key):
        return self.context.get(app=self.belong_app, key=key)

    def default_app(self, app):
        return app or self.belong_app

    @staticmethod
    def replace_domain(url: str, new_base: str) -> str:
        """
        替换 URL 的 scheme 和 netloc（协议和域名）。
        :param url: 原始 URL
        :param new_base: 新的 base，如 'https://new.example.com'
        :return: 替换后的 URL
        """
        parsed_url = urlparse(url)
        new_base_parsed = urlparse(new_base)

        updated_url = parsed_url._replace(
            scheme=new_base_parsed.scheme,
            netloc=new_base_parsed.netloc
        )
        return urlunparse(updated_url)
