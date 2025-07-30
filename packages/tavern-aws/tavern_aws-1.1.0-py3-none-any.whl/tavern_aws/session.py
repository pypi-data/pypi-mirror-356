import logging

import requests
from requests_aws4auth import AWS4Auth
from tavern._core import exceptions
from tavern._core.dict_util import check_expected_keys

logger = logging.getLogger(__name__)


class AWSSession(requests.Session):
    def __init__(self, **kwargs):
        super().__init__()

        access_key = kwargs.get("access_key")
        secret_key = kwargs.get("secret_key")
        service = kwargs.get("service")
        region = kwargs.get("region")
        session_token = kwargs.get("session_token")

        if access_key and secret_key and service and region:
            auth = AWS4Auth(
                access_key,
                secret_key,
                region,
                service,
                session_token=session_token,
            )
            self.auth = auth

    def __enter__(self):
        pass

    def __exit__(self, *args):
        pass
