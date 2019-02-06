from __future__ import print_function
from tests import utils as test_utils
from tests.utils.mock_ldap_server import MockLdapServer
from tests.utils.server_manager import ServerManager
from time import sleep


def main():
    client = test_utils.create_client()
    manager = ServerManager(
        config_paths=[test_utils.get_config_file_path('vault-tls.hcl')],
        client=client,
    )
    ldap_server = MockLdapServer()
    try:
        manager.start()
        manager.initialize()
        manager.unseal()

        client.token = manager.root_token

        ldap_server.start()
        client.sys.enable_auth_method(
            method_type='ldap',
        )
        client.auth.ldap.configure(
            url=ldap_server.url,
            bind_dn=ldap_server.ldap_bind_dn,
            bind_pass=ldap_server.ldap_bind_password,
            user_dn=ldap_server.ldap_users_dn,
            user_attr='uid',
            group_dn=ldap_server.ldap_groups_dn,
            group_attr='cn',
            insecure_tls=True,
        )
        client.auth.ldap.create_or_update_group(
            name=ldap_server.ldap_group_name,
            policies=['default'],
        )
        print('Waiting for dudes to talk to Vault...')
        while True:
            print('.', end='')
            sleep(10)
    finally:
        manager.stop()
        ldap_server.stop()


if __name__ == '__main__':
    main()
