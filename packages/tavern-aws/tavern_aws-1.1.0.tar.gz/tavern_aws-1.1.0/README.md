[![image](https://img.shields.io/pypi/v/tavern-aws)](https://pypi.python.org/pypi/tavern-aws)
[![image](https://img.shields.io/pypi/l/tavern-aws)](https://github.com/aeresov/tavern-aws/blob/main/LICENSE)
[![image](https://img.shields.io/pypi/pyversions/tavern-aws)](https://pypi.python.org/pypi/tavern-aws)

# Tavern AWS plugin

This is a [Tavern](https://github.com/taverntesting/tavern) plugin to add AWS Sig4 authentication headers to your calls using [requests-aws4auth
](https://github.com/tedder/requests-aws4auth).

This plugin reuses original `requests`-based REST plugin from Tavern, so it works with non-AWS endpoints too.

## Usage

### Install

Regular install via pip: `pip install tavern-aws`

### Tavern integration

Set option `tavern_http_backend` to `aws`.

You can do it via project options:
```toml
[tool.pytest.ini_options]
tavern_http_backend = aws
```
or via conftest.py:
```python
def pytest_configure(config: pytest.Config):
    config.option.tavern_http_backend = "aws"
```
Change it back to `requests` to use regular Tavern's REST plugin.

### Tests

Supply AWS credentials as text fields:
```yaml
test_name: Call endpoint with IAM auth

aws:
    access_key: xxxxxxxxxxxxxxxxxxxx
    secret_key: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    service: appsync
    region: us-east-1

stages:
  - name: first stage
```

Or from boto3 session object via pytest fixtures:
```python
import boto3
import botocore.credentials
import pytest

@pytest.fixture(scope="session", autouse=True)
def boto_session() -> boto3.Session:
    return boto3.Session()

@pytest.fixture(scope="session", autouse=True)
def boto_credentials(boto_session: boto3.Session) -> botocore.credentials.Credentials:
    return boto_session.get_credentials()
```
```yaml
test_name: Call endpoint with IAM auth

aws:
    access_key: "{boto_credentials.access_key}"
    secret_key: "{boto_credentials.secret_key}"
    service: appsync
    region: us-east-1
    session_token: "{boto_credentials.token}"

stages:
  - name: first stage
```