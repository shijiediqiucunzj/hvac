LDAP
====

.. contents::
   :local:
   :depth: 1


.. testsetup:: ldap

    from tests.utils.mock_ldap_server import MockLdapServer
    ldap_server = MockLdapServer()
    ldap_server.start()
    client.sys.enable_auth_method(
        method_type='ldap',
    )

    ldap_url = ldap_server.url

Configure LDAP Auth Method Settings
-----------------------------------

.. automethod:: hvac.api.auth_methods.Ldap.configure
   :noindex:

Examples
````````

.. testcode:: ldap

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    client.auth.ldap.configure(
        user_dn='dc=users,dc=hvac,dc=network',
        group_dn='ou=groups,dc=hvac,dc=network',
        url=ldap_url,
        bind_dn='cn=admin,dc=hvac,dc=network',
        bind_pass='notaverygoodpassword',
        user_attr='uid',
        group_attr='cn',
    )

Reading the LDAP Auth Method Configuration
------------------------------------------

.. automethod:: hvac.api.auth_methods.Ldap.configure
   :noindex:

Examples
````````

.. testcode:: ldap

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    ldap_configuration = client.auth.ldap.read_configuration()
    print('The LDAP auth method is configured with a LDAP server URL of: {url}'.format(
        url=ldap_configuration['data']['url']
    ))

Example output:

.. testoutput:: ldap

    The LDAP auth method is configured with a LDAP server URL of: ldap://...

Create or Update a LDAP Group Mapping
-------------------------------------

.. automethod:: hvac.api.auth_methods.Ldap.create_or_update_group
   :noindex:

Examples
````````

.. testcode:: ldap

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    client.auth.ldap.create_or_update_group(
        name='somedudes',
        policies=['policy-for-some-dudes'],
    )

List LDAP Group Mappings
------------------------

.. automethod:: hvac.api.auth_methods.Ldap.list_groups
   :noindex:

Examples
````````

.. testcode:: ldap

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    ldap_groups = client.auth.ldap.list_groups()
    print('The following groups are configured in the LDAP auth method: {groups}'.format(
        groups=','.join(ldap_groups['data']['keys'])
    ))

Example output:

.. testoutput:: ldap

    The following groups are configured in the LDAP auth method: somedudes


Read LDAP Group Mapping
-----------------------

.. automethod:: hvac.api.auth_methods.Ldap.read_group
   :noindex:

Examples
````````

.. testcode:: ldap

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    some_dudes_ldap_group = client.auth.ldap.read_group(
        name='somedudes',
    )
    print('The "somedudes" group in the LDAP auth method are mapped to the following policies: {policies}'.format(
        policies=','.join(some_dudes_ldap_group['data']['policies'])
    ))

Example output:

.. testoutput:: ldap

    The "somedudes" group in the LDAP auth method are mapped to the following policies: policy-for-some-dudes

Deleting a LDAP Group Mapping
-----------------------------

.. automethod:: hvac.api.auth_methods.Ldap.delete_group
   :noindex:

Examples
````````

.. testcode:: ldap

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    client.auth.ldap.delete_group(
        name='some-group',
    )

Creating or Updating a LDAP User Mapping
----------------------------------------

.. automethod:: hvac.api.auth_methods.Ldap.create_or_update_user
   :noindex:

Examples
````````

.. testcode:: ldap

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    client.auth.ldap.create_or_update_user(
        username='somedude',
        policies=['policy-for-some-dudes'],
    )

Listing LDAP User Mappings
--------------------------

.. automethod:: hvac.api.auth_methods.Ldap.list_users
   :noindex:

Examples
````````

.. testcode:: ldap

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    ldap_users = client.auth.ldap.list_users()
    print('The following users are configured in the LDAP auth method: {users}'.format(
        users=','.join(ldap_users['data']['keys'])
    ))

Example output:

.. testoutput:: ldap

    The following users are configured in the LDAP auth method: somedude

Reading a LDAP User Mapping
---------------------------

.. automethod:: hvac.api.auth_methods.Ldap.read_user
   :noindex:

Examples
````````

.. testcode:: ldap

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    some_dude_ldap_user = client.auth.ldap.read_user(
        username='somedude'
    )
    print('The "somedude" user in the LDAP auth method is mapped to the following policies: {policies}'.format(
        policies=','.join(some_dude_ldap_user['data']['policies'])
    ))

Example output:

.. testoutput:: ldap

    The "somedude" user in the LDAP auth method is mapped to the following policies: policy-for-some-dudes

Deleting a Configured User Mapping
----------------------------------

.. automethod:: hvac.api.auth_methods.Ldap.delete_user
   :noindex:

Examples
````````

.. testcode:: ldap

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    client.auth.ldap.delete_user(
        username='somedude',
    )

Authentication / Login
----------------------

.. automethod:: hvac.api.auth_methods.Ldap.login
   :noindex:

Examples
````````

.. testcode:: ldap

    import hvac

    ldap_username = 'somedude'
    ldap_password = os.environ['LDAP_PASSWORD']

    client = hvac.Client(url='https://127.0.0.1:8200')

    # Here the mount_point parameter corresponds to the path provided when enabling the backend
    client.auth.ldap.login(
        username=ldap_username,
        password=ldap_password,
    )
    print('Authentication status: {is_authenticated}'.format(
        is_authenticated=client.is_authenticated(),
    ))

Example output:

.. testoutput:: ldap

    Authentication status: True


.. testcleanup:: ldap

    client.token = os.environ['VAULT_TOKEN']
    ldap_server.stop()
