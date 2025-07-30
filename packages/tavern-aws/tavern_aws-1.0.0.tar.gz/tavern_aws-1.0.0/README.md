# Tavern AWS plugin

This is a [Tavern](https://github.com/taverntesting/tavern) plugin to add AWS Sig4 authentication headers to your calls using [requests-aws4auth
](https://github.com/tedder/requests-aws4auth) plugin. 

You can suplly credentials either manually or from boto3 session object via pytest fixtures.

## Usage

Install it: `pip install tavern-aws`

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
