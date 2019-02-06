.. _gcp-auth-method:

GCP
===

.. contents::
   :local:
   :depth: 1


Configure
---------

.. automethod:: hvac.api.auth_methods.Gcp.configure
   :noindex:

Examples
````````
.. testsetup:: gcp-auth

    client = hvac.Client(url='https://127.0.0.1:8200')
    client.sys.enable_auth_method(
        method_type='gcp'
    )

.. testcode:: gcp-auth

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    client.auth.gcp.configure(
        credentials=os.environ['GCP_JWT_CREDENTIALS'],
    )

Read Config
-----------

.. automethod:: hvac.api.auth_methods.Gcp.read_config
   :noindex:

Examples
````````

.. testcode:: gcp-auth

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    read_config = client.auth.gcp.read_config()
    print('The configured project_id is: {id}'.format(id=read_config['project_id']))

Example output:

.. testoutput:: gcp-auth

    The configured project_id is: test-hvac-project-not-a-real-project

Delete Config
-------------

.. automethod:: hvac.api.auth_methods.Gcp.delete_config
   :noindex:

Examples
````````

.. TODO: convert this to a test code block pending the outcome of https://github.com/hashicorp/vault-plugin-auth-gcp/issues/62

.. code:: python

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    client.auth.gcp.delete_config()

Create Role
-----------

.. automethod:: hvac.api.auth_methods.Gcp.create_role
   :noindex:

Examples
````````

.. testcode:: gcp-auth

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    client.auth.gcp.create_role(
        name='some-iam-role-name',
        role_type='iam',
        project_id='some-gcp-project-id',
        bound_service_accounts=['hvac@appspot.gserviceaccount.com'],
    )

    client.auth.gcp.create_role(
        name='some-gce-role-name',
        role_type='gce',
        project_id='some-gcp-project-id',
        bound_service_accounts=['hvac@appspot.gserviceaccount.com'],
    )

Edit Service Accounts On IAM Role
---------------------------------

.. automethod:: hvac.api.auth_methods.Gcp.edit_service_accounts_on_iam_role
   :noindex:

Examples
````````

.. testcode:: gcp-auth

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    client.auth.gcp.edit_service_accounts_on_iam_role(
        name='some-iam-role-name',
        add=['hvac@appspot.gserviceaccount.com'],
    )

    client.auth.gcp.edit_service_accounts_on_iam_role(
        name='some-iam-role-name',
        remove=['disallowed-service-account@appspot.gserviceaccount.com'],
    )

Edit Labels On GCE Role
-----------------------

.. automethod:: hvac.api.auth_methods.Gcp.edit_labels_on_gce_role
   :noindex:

Examples
````````

.. testcode:: gcp-auth

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    client.auth.gcp.edit_labels_on_gce_role(
        name='some-gce-role-name',
        add=['some-key:some-value'],
    )

    client.auth.gcp.edit_labels_on_gce_role(
        name='some-gce-role-name',
        remove=['some-bad-key:some-bad-value'],
    )

Read A Role
-----------

.. automethod:: hvac.api.auth_methods.Gcp.read_role
   :noindex:

Examples
````````

.. testcode:: gcp-auth

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    read_role_response = client.auth.gcp.read_role(
        name='some-iam-role-name',
    )

    print('Bound service accounts for role "{name}": {bound_service_accounts}'.format(
        name='some-iam-role-name',
        bound_service_accounts=', '.join(read_role_response['bound_service_accounts']),
    ))

.. testoutput:: gcp-auth

    Bound service accounts for role "some-iam-role-name": hvac@appspot.gserviceaccount.com

List Roles
----------

.. automethod:: hvac.api.auth_methods.Gcp.list_roles
   :noindex:

Examples
````````

.. testcode:: gcp-auth

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    roles = client.auth.gcp.list_roles()
    print('The following GCP auth roles are configured: {roles}'.format(
        roles=', '.join(roles['keys']),
    ))

.. testoutput:: gcp-auth

    The following GCP auth roles are configured: some-gce-role-name, some-iam-role-name

Delete A Role
-------------

.. automethod:: hvac.api.auth_methods.Gcp.delete_role
   :noindex:

Examples
````````

.. testcode:: gcp-auth

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    client.auth.gcp.delete_role(
        role='some-iam-role-name',
    )

Login
-----

.. automethod:: hvac.api.auth_methods.Gcp.login
   :noindex:

Basic Example
`````````````

.. testcode:: gcp-auth

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    client.auth.gcp.login(
        role='some-iam-role-name',
        jwt='some signed JSON web token...',
    )
    client.is_authenticated  # ==> returns True


google-api-python-client Example
````````````````````````````````

.. code:: python

    import json
    import time

    from googleapiclient import discovery # pip install google-api-python-client
    from google.oauth2 import service_account # pip install google-auth
    import hvac # pip install hvac

    # First load some previously generated GCP service account key
    path_to_sa_json = os.environ['GCP_SERVICE_ACCOUNT_JSON_PATH']
    credentials = service_account.Credentials.from_service_account_file(path_to_sa_json)
    with open(path_to_sa_json, 'r') as f:
        creds = json.load(f)
        project = creds['project_id']
        service_account = creds['client_email']

    # Generate a payload for subsequent "signJwt()" call
    # Reference: https://google-auth.readthedocs.io/en/latest/reference/google.auth.jwt.html#google.auth.jwt.Credentials
    now = int(time.time())
    expires = now + 900  # 15 mins in seconds, can't be longer.
    payload = {
        'iat': now,
        'exp': expires,
        'sub': service_account,
        'aud': 'vault/my-role'
    }
    body = {'payload': json.dumps(payload)}
    name = f'projects/{project}/serviceAccounts/{service_account}'

    # Perform the GCP API call
    iam = discovery.build('iam', 'v1', credentials=credentials)
    request = iam.projects().serviceAccounts().signJwt(name=name, body=body)
    resp = request.execute()
    jwt = resp['signedJwt']

    # Perform hvac call to configured GCP auth method
    client.auth.gcp.login(
        role='my-role',
        jwt=jwt,
    )
