# Tavern AWS plugin

This is a [Tavern](https://github.com/taverntesting/tavern) plugin to add AWS Sig4 authentication headers to your calls using [requests-aws4auth
](https://github.com/tedder/requests-aws4auth) plugin. 

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

Add necessary bits to your test file:
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

You can add `session_token`, e.g. if you use SSO.

You can suplly credentials either manually or from boto3 session object via pytest fixtures.
