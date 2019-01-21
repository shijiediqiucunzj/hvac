#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from tests import utils as test_utils
from tests.utils.server_manager import ServerManager
from tests.utils.mock_ldap_server import MockLdapServer

def doctest_global_setup():
    client = test_utils.create_client()
    manager = ServerManager(
        config_paths=[test_utils.get_config_file_path('vault-doctest.hcl')],
        client=client,
    )
    manager.start()
    manager.initialize()
    manager.unseal()

    client.token = manager.root_token
    os.environ['VAULT_TOKEN'] = manager.root_token
    os.environ['REQUESTS_CA_BUNDLE'] = test_utils.get_config_file_path('server-cert.pem')
    os.environ['LDAP_USERNAME'] = MockLdapServer.ldap_user_name
    os.environ['LDAP_PASSWORD'] = MockLdapServer.ldap_user_password

    return manager
