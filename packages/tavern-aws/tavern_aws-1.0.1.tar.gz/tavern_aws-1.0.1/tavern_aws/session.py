import logging

import requests
from requests_aws4auth import AWS4Auth
from tavern._core import exceptions
from tavern._core.dict_util import check_expected_keys

logger = logging.getLogger(__name__)


class AWSSession(requests.Session):
    def __init__(self, **kwargs):
        super().__init__()

        expected_blocks = {
            "access_key",
            "secret_key",
            "service",
            "region",
            "session_token",
        }
        check_expected_keys(expected_blocks, kwargs)

        access_key = kwargs.get("access_key")
        if not access_key:
            raise exceptions.MissingKeysError("Need to specify aws access_key")
        secret_key = kwargs.get("secret_key")
        if not secret_key:
            raise exceptions.MissingKeysError("Need to specify aws secret_key")
        service = kwargs.get("service")
        if not service:
            raise exceptions.MissingKeysError("Need to specify aws service")
        region = kwargs.get("region")
        if not region:
            raise exceptions.MissingKeysError("Need to specify aws region")
        session_token = kwargs.get("session_token", None)

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
