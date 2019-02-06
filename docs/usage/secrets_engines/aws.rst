AWS
===

.. contents::
   :local:
   :depth: 1

.. testsetup:: aws-secrets

    client.sys.enable_secrets_engine(
        backend_type='aws',
    )

Configure Root IAM Credentials
------------------------------

.. automethod:: hvac.api.secrets_engines.Aws.configure_root_iam_credentials
   :noindex:

Examples
````````

.. testcode:: aws-secrets

    import os

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    client.secrets.aws.configure_root_iam_credentials(
        access_key=os.getenv('AWS_ACCESS_KEY_ID'),
        secret_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    )

Rotate Root IAM Credentials
---------------------------

.. automethod:: hvac.api.secrets_engines.Aws.rotate_root_iam_credentials
   :noindex:

Examples
````````

.. testcode:: aws-secrets

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    client.secrets.aws.rotate_root_iam_credentials()

Configure Lease
---------------

.. automethod:: hvac.api.secrets_engines.Aws.configure_lease
   :noindex:

Examples
````````

.. testcode:: aws-secrets

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    # Set the default lease TTL to 300 seconds / 5 minutes and a max TTL of 24 hours
    client.secrets.aws.configure_lease(
        lease='300s',
        lease_max='24h',
    )

Read Lease Configuration
------------------------

.. automethod:: hvac.api.secrets_engines.Aws.read_lease_config
   :noindex:

Examples
````````

.. testcode:: aws-secrets

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    read_lease_response = client.secrets.aws.read_lease_config()
    print('The current "lease_max" TTL is: {lease_max}'.format(
        lease_max=read_lease_response['data']['lease_max'],
    ))

Example output:

.. testoutput:: aws-secrets

    The current "lease_max" TTL is: ...

Create or Update Role
---------------------

.. automethod:: hvac.api.secrets_engines.Aws.create_or_update_role
   :noindex:

Examples
````````

.. testcode:: aws-secrets
    :skipif: test_utils.vault_version_lt('0.11.0') and os.getenv('HVAC_RENDER_DOCTESTS') is None

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    describe_ec2_policy_doc = {
        'Version': '2012-10-17',
        'Statement': [
            {
                'Resource': '*',
                'Action': 'ec2:Describe*',
                'Effect': 'Allow',
            },
        ],
    }
    client.secrets.aws.create_or_update_role(
        name='hvac-role',
        credential_type='assumed_role',
        policy_document=describe_ec2_policy_doc,
    )

Legacy Parameters
`````````````````

.. note::
    In previous versions of Vault (before version 0.11.0), this API route only supports the `policy_document` and `policy_arns` parameters (which hvac will translate to `policy` and `arn` parameters respectively in the request sent to Vault). If running these versions of Vault, the `legacy_params` parameter on this method can be set to `True`.

For older versions of Vault (any version before 0.11.0):

.. testcode:: aws-secrets
   :skipif: test_utils.vault_version_ge('0.11.0') and os.getenv('HVAC_RENDER_DOCTESTS') is None

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    # Note: with the legacy params, the `policy_arns` parameter is translated to `arn`
    # in the request sent to Vault and only one ARN is accepted. If a list is provided,
    # hvac will only use the first ARN in the list.
    client.secrets.aws.create_or_update_role(
        name='hvac-role',
        credential_type='iam_user',
        policy_arns='arn:aws:iam::aws:policy/AmazonVPCReadOnlyAccess',
        legacy_params=True,
    )

Read Role
---------

.. automethod:: hvac.api.secrets_engines.Aws.read_role
   :noindex:

Examples
````````

.. testcode:: aws-secrets

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    read_role_response = client.secrets.aws.read_role(
        name='hvac-role',
    )
    print('The credential type for role "hvac-role" is: {cred_type}'.format(
        cred_type=read_role_response['data']['credential_type'],
    ))

Example output:

.. testoutput:: aws-secrets

    The credential type for role "hvac-role" is: ...

List Roles
----------

.. automethod:: hvac.api.secrets_engines.Aws.list_roles
   :noindex:

Examples
````````

.. testcode:: aws-secrets

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    list_roles_response = client.secrets.aws.list_roles()
    print('AWS secrets engine role listing: {roles}'.format(
        roles=', '.join(list_roles_response['data']['keys'])
    ))

Example output:

.. testoutput:: aws-secrets

    AWS secrets engine role listing: hvac-role

Delete Role
-----------

.. automethod:: hvac.api.secrets_engines.Aws.delete_role
   :noindex:

Examples
````````

.. testcode:: aws-secrets

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    client.secrets.aws.delete_role(
        name='hvac-role',
    )

Generate Credentials
--------------------

.. automethod:: hvac.api.secrets_engines.Aws.generate_credentials
   :noindex:

Examples
````````

.. testsetup:: aws-secrets

    client.secrets.aws.create_or_update_role(
        name='hvac-role',
        credential_type='iam_user',
        policy_arns='arn:aws:iam::aws:policy/AmazonVPCReadOnlyAccess',
    )

.. testcode:: aws-secrets

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    gen_creds_response = client.secrets.aws.generate_credentials(
        name='hvac-role',
    )
    print('Generated access / secret keys: {access} / {secret}'.format(
        access=gen_creds_response['data']['access_key'],
        secret=gen_creds_response['data']['secret_key'],
    ))

Example output:

.. testoutput:: aws-secrets

    Generated access / secret keys: ...

.. testcleanup:: aws-secrets

    client.sys.disable_secrets_engine(
        path='aws',
    )
