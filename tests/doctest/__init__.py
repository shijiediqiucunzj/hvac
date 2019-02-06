#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from requests_mock.mocker import Mocker
from datetime import datetime, timedelta
from tests import utils as test_utils
from tests.utils.mock_ldap_server import MockLdapServer
from tests.utils.server_manager import ServerManager
from mock import patch, MagicMock


def doctest_global_setup():
    client = test_utils.create_client()
    manager = ServerManager(
        config_paths=[test_utils.get_config_file_path('vault-doctest.hcl')],
        client=client,
    )
    manager.start()
    manager.initialize()
    manager.unseal()

    mocker = Mocker(real_http=True)
    mocker.start()
    mock_response = {
            'auth': {
                'accessor': 'accessor-1234-5678-9012-345678901234',
                'client_token': manager.root_token,
                'lease_duration': 10000,
                'metadata': {
                    'role': 'custom_role',
                    'service_account_email': 'dev1@project-123456.iam.gserviceaccount.com',
                    'service_account_id': '111111111111111111111'
                },
                'policies': [
                    'default',
                    'custom_role'
                ],
                'renewable': True
            },
            'data': None,
            'lease_duration': 0,
            'lease_id': '',
            'renewable': False,
            'request_id': 'requesti-1234-5678-9012-345678901234',
            'warnings': [],
            'wrap_info': None
        }
    mock_url = 'https://127.0.0.1:8200/v1/auth/aws/login'
    mocker.register_uri(
        method='POST',
        url=mock_url,
        json=mock_response
    )

    utc_timestamp = datetime.utcnow()
    datetime_format = '%Y-%m-%dT%H:%M:%SZ%z'
    last_updated = utc_timestamp - timedelta(hours=4)
    expiration = utc_timestamp + timedelta(hours=4)

    mock_response = {
        "Code": "Success",
        "LastUpdated": last_updated.strftime(datetime_format),
        "Type": "AWS-HMAC",
        "AccessKeyId": "foobar_key",
        "SecretAccessKey": "foobar_secret",
        "Token": "foobar_token",
        "Expiration": expiration.strftime(datetime_format),
    }
    mock_url = 'http://169.254.169.254/latest/meta-data/iam/security-credentials/some-instance-role'
    mocker.register_uri(
        method='GET',
        url=mock_url,
        json=mock_response
    )
    mock_response = 'some_pkcs7_string'
    mock_url = 'http://169.254.169.254/latest/dynamic/instance-identity/pkcs7'
    mocker.register_uri(
        method='GET',
        url=mock_url,
        json=mock_response
    )
    auth_method_paths = [
        'azure/login',
        'kubernetes/login',
        'gcp/login',
        'github/login',
        'ldap/login/{}'.format(MockLdapServer.ldap_user_name),
        'some-userpass/login/someuser',  # For MFA docs
        'okta/login',
        'okta/login/hvac-person',
    ]
    for auth_method_path in auth_method_paths:
        mock_url = 'https://127.0.0.1:8200/v1/auth/{path}'.format(path=auth_method_path)
        mock_response = {
            "auth": {
                "client_token": manager.root_token,
                "accessor": "0e9e354a-520f-df04-6867-ee81cae3d42d",
                "policies": ['default'],
                "lease_duration": 2764800,
                "renewable": True,
            },
        }
        mocker.register_uri(
            method='POST',
            url=mock_url,
            json=mock_response,
        )

    mock_url = 'https://127.0.0.1:8200/v1/auth/{mount_point}/duo/access'.format(
        mount_point='some-userpass',
    )
    mocker.register_uri(
        method='POST',
        url=mock_url,
    )

    mock_response = {
      "data": {
        "access_key": "AKIA..."
      }
    }
    mock_url = 'https://127.0.0.1:8200/v1/{mount_point}/config/rotate-root'.format(
        mount_point='aws',
    )
    mocker.register_uri(
        method='POST',
        url=mock_url,
        json=mock_response,
    )
    mock_response = {
      "data": {
        "access_key": "AKIA...",
        "secret_key": "xlCs...",
        "security_token": None
      }
    }
    mock_url = 'https://127.0.0.1:8200/v1/{mount_point}/creds/{role_name}'.format(
        mount_point='aws',
        role_name='hvac-role',
    )
    mocker.register_uri(
        method='GET',
        url=mock_url,
        json=mock_response,
    )

    mock_url = 'https://127.0.0.1:8200/v1/{mount_point}/roles/{name}'.format(
        mount_point='azure',
        name='hvac',
    )
    mocker.register_uri(
        method='POST',
        url=mock_url,
    )
    mock_url = 'https://127.0.0.1:8200/v1/{mount_point}/roles'.format(
        mount_point='azure',
    )
    mock_response = {
        'data': {
            'keys': ['hvac'],
        },
    }
    mocker.register_uri(
        method='LIST',
        url=mock_url,
        json=mock_response,
    )
    mock_response = {
        'data': {
            'client_id': 'some_client_id',
            'client_secret': 'some_client_secret',
        },
    }
    mock_url = 'https://127.0.0.1:8200/v1/{mount_point}/creds/{name}'.format(
        mount_point='azure',
        name='hvac',
    )
    mocker.register_uri(
        method='GET',
        url=mock_url,
        json=mock_response,
    )



    # mock_url = 'http://localhost:8200/v1/{mount_point}/roles/{name}'.format(
    #     mount_point=DEFAULT_MOUNT_POINT,
    #     name=role_name,
    # )
    # requests_mocker.register_uri(
    #     method='POST',
    #     url=mock_url,
    #     status_code=expected_status_code,
    #     # json=mock_response,
    # )

    client.token = manager.root_token
    os.environ['VAULT_TOKEN'] = manager.root_token
    os.environ['REQUESTS_CA_BUNDLE'] = test_utils.get_config_file_path('server-cert.pem')
    os.environ['LDAP_USERNAME'] = MockLdapServer.ldap_user_name
    os.environ['LDAP_PASSWORD'] = MockLdapServer.ldap_user_password
    os.environ['AWS_LAMBDA_FUNCTION_NAME'] = 'hvac-lambda'
    # "Mock" the AWS credentials as they can't be mocked in Botocore currently
    os.environ.setdefault("AWS_ACCESS_KEY_ID", "foobar_key")
    os.environ.setdefault("AWS_SECRET_ACCESS_KEY", "foobar_secret")
    os.environ.setdefault("VAULT_ADDR", "https://127.0.0.1:8200")
    os.environ.setdefault("VAULT_HEADER_VALUE", "some_header_value")
    os.environ.setdefault("GCP_SERVICE_ACCOUNT_JSON_PATH", test_utils.get_config_file_path('example.jwt.json'))
    os.environ.setdefault("LDAP_PASSWORD", MockLdapServer.ldap_user_password)

    with open(test_utils.get_config_file_path('example.jwt.json')) as fp:
        os.environ.setdefault('GCP_JWT_CREDENTIALS', fp.read())

    # GCP specific?
    # gcp_discovery_patcher = patch('googleapiclient.discovery')
    # gcp_discovery_mock = gcp_discovery_patcher.start()
    # mock_iam_service = MagicMock()
    # gcp_discovery_mock.build.return_value = mock_iam_service

    return manager
