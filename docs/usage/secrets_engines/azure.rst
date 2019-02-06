.. _azure-secret-engine:

Azure
=====

.. contents::
   :local:
   :depth: 1

.. testsetup:: azure-secrets

    client.sys.enable_secrets_engine(
        backend_type='azure',
    )


Configure
---------

.. automethod:: hvac.api.secrets_engines.Azure.configure
   :noindex:

Examples
````````

.. testcode:: azure-secrets

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    client.secrets.azure.configure(
        subscription_id='my-subscription-id',
        tenant_id='my-tenant-id',
    )

Read Config
-----------

.. automethod:: hvac.api.secrets_engines.Azure.read_config
   :noindex:

Examples
````````

.. testcode:: azure-secrets

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    azure_secret_config = client.secrets.azure.read_config()
    print('The Azure secret engine is configured with a subscription ID of {id}'.format(
        id=azure_secret_config['subscription_id'],
    ))

Example output:

.. testoutput:: azure-secrets

    The Azure secret engine is configured with a subscription ID of my-subscription-id

Delete Config
-------------

.. automethod:: hvac.api.secrets_engines.Azure.delete_config
   :noindex:

Examples
````````

.. testsetup:: azure-secrets-delete-config

    client.sys.enable_secrets_engine(
        backend_type='azure',
    )

.. testcode:: azure-secrets-delete-config

    # TODO: figure out why we can't configure the engine again after the delete_config method is called...

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    client.secrets.azure.delete_config()

Create Or Update A Role
-----------------------

.. automethod:: hvac.api.secrets_engines.Azure.create_or_update_role
   :noindex:

Examples
````````

.. testcode:: azure-secrets

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')


    azure_roles = [
        {
            'role_name': "Contributor",
            'scope': "/subscriptions/95e675fa-307a-455e-8cdf-0a66aeaa35ae",
        },
    ]
    client.secrets.azure.create_or_update_role(
        name='hvac',
        azure_roles=azure_roles,
    )

List Roles
----------

.. automethod:: hvac.api.secrets_engines.Azure.list_roles
   :noindex:

Examples
````````

.. testcode:: azure-secrets

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    azure_secret_engine_roles = client.secrets.azure.list_roles()
    print('The following Azure secret roles are configured: {roles}'.format(
        roles=', '.join(azure_secret_engine_roles['keys']),
    ))

Example output:

.. testoutput:: azure-secrets

    The following Azure secret roles are configured: hvac


Generate Credentials
--------------------

.. automethod:: hvac.api.secrets_engines.Azure.generate_credentials
   :noindex:

Examples
````````

.. testsetup:: azure-secrets

    from mock import patch
    azure_spc_patcher = patch('azure.common.credentials.ServicePrincipalCredentials')
    mock_azure_spc = azure_spc_patcher.start()

.. testcode:: azure-secrets

    import hvac
    from azure.common.credentials import ServicePrincipalCredentials

    client = hvac.Client(url='https://127.0.0.1:8200')
    azure_creds = client.secrets.azure.generate_credentials(
        name='hvac',
    )
    azure_spc = ServicePrincipalCredentials(
        client_id=azure_creds['client_id'],
        secret=azure_creds['client_secret'],
        tenant='my-tenant-id',
    )

.. testcleanup:: azure-secrets

    azure_spc_patcher.stop()

.. testcleanup:: azure-secrets

    client.sys.disable_secrets_engine(
        path='azure',
    )
