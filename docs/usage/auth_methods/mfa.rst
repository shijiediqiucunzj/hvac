MFA
===

.. contents::
   :local:
   :depth: 1

.. note::

    The legacy/unsupported MFA auth method covered by this class's configuration API route only supports integration with a subset of Vault auth methods. See the list of supported auth methods in this module's :py:attr:`"SUPPORTED_AUTH_METHODS" attribute<hvac.api.auth_methods.mfa.SUPPORTED_AUTH_METHODS>` and/or the associated `Vault MFA documentation`_ for additional information.

.. _Vault MFA documentation: https://www.vaultproject.io/docs/auth/mfa.html

.. testsetup:: mfa

    test_userpass_password = 'some password'

    from mock import patch
    getpass_patcher = patch('getpass.getpass')
    mock_getpass = getpass_patcher.start()
    mock_getpass.return_value = test_userpass_password

    userpass_auth_path = 'some-userpass'
    # Reset state of our test userpass auth method under path: some-userpass
    client.sys.disable_auth_method(
        path=userpass_auth_path,
    )
    client.sys.enable_auth_method(
        method_type='userpass',
        path=userpass_auth_path,
    )
    client.create_userpass(
        username='someuser',
        password=test_userpass_password,
        policies=['default'],
        mount_point=userpass_auth_path,
    )

Configure
---------

.. automethod:: hvac.api.auth_methods.Mfa.configure
   :noindex:

Examples
````````

Adding MFA to the userpass auth method mounted under path "some-userpass":

.. testcode:: mfa

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    client.auth.mfa.configure(
        mount_point='some-userpass',
    )

Read Configuration
------------------

.. automethod:: hvac.api.auth_methods.Mfa.read_configuration
   :noindex:

Examples
````````
.. testcode:: mfa

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    mfa_configuration = client.auth.mfa.read_configuration(
        mount_point='some-userpass',
    )
    print('The MFA auth method is configured with a MFA type of: {mfa_type}'.format(
        mfa_type=mfa_configuration['data']['type']
    ))

Example output:

.. testoutput:: mfa

    The MFA auth method is configured with a MFA type of: duo

Configure Duo Access Credentials
--------------------------------

.. automethod:: hvac.api.auth_methods.Mfa.configure_duo_access
   :noindex:

Examples
````````

.. testcode:: mfa

    from getpass import getpass

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    secret_key_prompt = 'Please enter the Duo access secret key to configure: '
    duo_access_secret_key = getpass(prompt=secret_key_prompt)

    client.auth.mfa.configure_duo_access(
        mount_point=userpass_auth_path,
        host='api-1234abcd.duosecurity.com',
        integration_key='SOME_DUO_IKEY',
        secret_key=duo_access_secret_key,
    )

Configure Duo Behavior
----------------------

.. automethod:: hvac.api.auth_methods.Mfa.configure_duo_behavior
   :noindex:

Examples
````````
.. testcode:: mfa

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    client.auth.mfa.configure_duo_behavior(
        mount_point=userpass_auth_path,
        username_format='%s@hvac.network',
    )


Read Duo Behavior
-----------------

.. automethod:: hvac.api.auth_methods.Mfa.read_duo_behavior_configuration
   :noindex:

Examples
````````
.. testcode:: mfa

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    duo_behavior_config = client.auth.mfa.read_duo_behavior_configuration(
        mount_point=userpass_auth_path,
    )
    print('The Duo MFA behvaior is configured with a username_format of: {username_format}'.format(
        username_format=duo_behavior_config['data']['username_format'],
    ))

Example output:

.. testoutput:: mfa

    The Duo MFA behvaior is configured with a username_format of: %s@hvac.network

Authentication / Login
----------------------

Examples
````````
.. testcode:: mfa

    from getpass import getpass

    import hvac

    login_username = 'someuser'
    password_prompt = 'Please enter your password for the userpass (with MFA) authentication backend: '
    login_password = getpass(prompt=password_prompt)
    passcode_prompt = 'Please enter your OTP for the userpass (with MFA) authentication backend: '
    userpass_mfa_passcode = getpass(prompt=passcode_prompt)

    client = hvac.Client(url='https://127.0.0.1:8200')

    # Here the mount_point parameter corresponds to the path provided when enabling the backend
    client.auth_userpass(
        username=login_username,
        password=login_password,
        mount_point='some-userpass',
        passcode=userpass_mfa_passcode,
    )
    print('Authentication status: {is_authenticated}'.format(
        is_authenticated=client.is_authenticated(),
    ))

Example output:

.. testoutput:: mfa

    Authentication status: True


.. testcleanup:: mfa

    userpass_auth_path = 'some-userpass'
    client.sys.disable_auth_method(
        path=userpass_auth_path,
    )
    getpass_patcher.stop()
