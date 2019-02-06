Okta
====

.. contents::
   :local:
   :depth: 1


.. testsetup:: okta

    test_okta_password = 'some password'

    from mock import patch
    getpass_patcher = patch('getpass.getpass')
    mock_getpass = getpass_patcher.start()
    mock_getpass.return_value = test_okta_password

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    # Reset state of our test okta auth method under path
    client.sys.disable_auth_method(
        path='okta',
    )
    client.sys.enable_auth_method(
        method_type='okta',
    )


Configure
---------

.. automethod:: hvac.api.auth_methods.Okta.configure
   :noindex:

Examples
````````
.. testcode:: okta

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    client.auth.okta.configure(
        org_name='hvac-project'
    )

Read Config
-----------

.. automethod:: hvac.api.auth_methods.Okta.read_config
   :noindex:

Examples
````````
.. testcode:: okta

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    okta_config = client.auth.okta.read_config()
    print('The Okta auth method at path /okta has a configured organization name of: {name}'.format(
        name=okta_config['data']['org_name'],
    ))

Example output:

.. testoutput:: okta

    The Okta auth method at path /okta has a configured organization name of: hvac-project

List Users
----------

.. automethod:: hvac.api.auth_methods.Okta.list_users
   :noindex:

Examples
````````
.. testsetup:: okta

    client.auth.okta.register_user(
        username='hvac-person',
        policies=['hvac-admin'],
    )

.. testcode:: okta

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    users = client.auth.okta.list_users()
    print('The following Okta users are registered: {users}'.format(
        users=','.join(users['data']['keys']),
    ))

Example output:

.. testoutput:: okta

    The following Okta users are registered: hvac-person

Register User
-------------

.. automethod:: hvac.api.auth_methods.Okta.register_user
   :noindex:

Examples
````````
.. testcode:: okta

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    client.auth.okta.register_user(
        username='hvac-person',
        policies=['hvac-admin'],
    )

Read User
---------

.. automethod:: hvac.api.auth_methods.Okta.read_user
   :noindex:

Examples
````````
.. testcode:: okta

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    read_user = client.auth.okta.read_user(
        username='hvac-person',
    )
    print('Okta user "{name}" has the following attached policies: {policies}'.format(
        name='hvac-person',
        policies=', '.join(read_user['data']['policies']),
    ))

Example output:

.. testoutput:: okta

    Okta user "hvac-person" has the following attached policies: hvac-admin

Delete User
-----------

.. automethod:: hvac.api.auth_methods.Okta.delete_user
   :noindex:

Examples
````````
.. testcode:: okta

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    client.auth.okta.delete_user(
        username='hvac-person'
    )

List Groups
-----------

.. automethod:: hvac.api.auth_methods.Okta.list_groups
   :noindex:

Examples
````````
.. testsetup:: okta

    client.auth.okta.register_group(
        name='hvac-group',
        policies=['hvac-group-members'],
    )

.. testcode:: okta

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    groups = client.auth.okta.list_groups()
    print('The following Okta groups are registered: {groups}'.format(
        groups=','.join(groups['data']['keys']),
    ))

Example output:

.. testoutput:: okta

    The following Okta groups are registered: hvac-group

Register Group
--------------

.. automethod:: hvac.api.auth_methods.Okta.register_group
   :noindex:

Examples
````````
.. testcode:: okta

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    client.auth.okta.register_group(
        name='hvac-group',
        policies=['hvac-group-members'],
    )

Read Group
----------

.. automethod:: hvac.api.auth_methods.Okta.read_group
   :noindex:

Examples
````````
.. testcode:: okta

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    read_group = client.auth.okta.read_group(
        name='hvac-group',
    )
    print('Okta group "{name}" has the following attached policies: {policies}'.format(
        name='hvac-group',
        policies=', '.join(read_group['data']['policies']),
    ))

Example output:

.. testoutput:: okta

    Okta group "hvac-group" has the following attached policies: hvac-group-members

Delete Group
------------

.. automethod:: hvac.api.auth_methods.Okta.delete_group
   :noindex:

Examples
````````
.. testcode:: okta

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    client.auth.okta.delete_group(
        name='hvac-group',
    )

Login
-----

.. automethod:: hvac.api.auth_methods.Okta.login
   :noindex:

Examples
````````
.. testcode:: okta

    from getpass import getpass

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')


    password_prompt = 'Please enter your password for the Okta authentication backend: '
    okta_password = getpass(prompt=password_prompt)

    client.auth.okta.login(
        username='hvac-person',
        password=okta_password,
    )

.. testcleanup:: okta

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    # Reset state of our test okta auth method under path
    client.sys.disable_auth_method(
        path='okta',
    )

    getpass_patcher.stop()
