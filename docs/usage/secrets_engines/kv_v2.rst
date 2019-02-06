KV - Version 2
==============

.. contents::
   :local:
   :depth: 1

.. testsetup:: kv_v2, kv_v2_configuration

    client.sys.enable_secrets_engine(
        backend_type='kv',
        path='kv',
        options=dict(version=2),
    )

    # We occasionally see issues with the newly enabled secrets engine not becoming available in time for our test cases.
    # So we wait for it to show up in the mounted secrets engines list here before proceeding.
    attempts = 0
    while attempts < 25 and 'kv/' not in client.sys.list_mounted_secrets_engines()['data']:
        attempts += 1
        logging.debug('Waiting 1 second for KV V2 secrets engine under path {path} to become available...'.format(
            path='kv',
        ))
        sleep(1)

Configuration
-------------

.. automethod:: hvac.api.secrets_engines.KvV2.configure
   :noindex:

Examples
````````

Setting the default `cas_required` (check-and-set required) flag under the implicit default path of `secret`:

.. testcode:: kv_v2_configuration

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    client.secrets.kv.v2.configure(
        cas_required=True,
        mount_point='kv',
    )

Setting the default `max_versions` for a key/value engine version 2 under a path of `kv`:

.. testcode:: kv_v2_configuration

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    client.secrets.kv.v2.configure(
        max_versions=20,
        mount_point='kv',
    )

Read Configuration
------------------

.. automethod:: hvac.api.secrets_engines.KvV2.read_configuration
   :noindex:

Examples
````````

Reading the configuration of a KV version 2 engine mounted under a path of `kv`:

.. testcode:: kv_v2_configuration

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    kv_configuration = client.secrets.kv.v2.read_configuration(
        mount_point='kv',
    )
    print('Config under path "kv", max_versions set to: "{max_ver}"'.format(
        max_ver=kv_configuration['data']['max_versions'],
    ))
    print('Config under path "kv", check-and-set require flag set to: {cas}'.format(
        cas=kv_configuration['data']['cas_required'],
    ))

Example output:

.. testoutput:: kv_v2_configuration

    Config under path "kv", max_versions set to: "20"
    Config under path "kv", check-and-set require flag set to: True


Read Secret Versions
--------------------

.. automethod:: hvac.api.secrets_engines.KvV2.read_configuration
   :noindex:

Examples
````````

Read the latest version of a given secret/path ("hvac"):

.. testsetup:: kv_v2

    client.secrets.kv.v2.create_or_update_secret(
        path='hvac',
        secret=dict(pssst='this is secret'),
        mount_point='kv',
    )

.. testcode:: kv_v2

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    secret_version_response = client.secrets.kv.v2.read_secret_version(
        path='hvac',
        mount_point='kv',
    )
    print('Latest version of secret under path "hvac" contains the following keys: {data}'.format(
        data=secret_version_response['data']['data'].keys(),
    ))
    print('Latest version of secret under path "hvac" created at: {date}'.format(
        date=secret_version_response['data']['metadata']['created_time'],
    ))
    print('Latest version of secret under path "hvac" is version #{ver}'.format(
        ver=secret_version_response['data']['metadata']['version'],
    ))

Example output:

.. testoutput:: kv_v2

    Latest version of secret under path "hvac" contains the following keys: dict_keys(['pssst'])
    Latest version of secret under path "hvac" created at: ...
    Latest version of secret under path "hvac" is version #1


Read specific version (1) of a given secret/path ("hvac"):

.. testcode:: kv_v2

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    secret_version_response = client.secrets.kv.v2.read_secret_version(
        path='hvac',
        version=1,
        mount_point='kv',
    )
    print('Version 1 of secret under path "hvac" contains the following keys: {data}'.format(
        data=secret_version_response['data']['data'].keys(),
    ))
    print('Version 1 of secret under path "hvac" created at: {date}'.format(
        date=secret_version_response['data']['metadata']['created_time'],
    ))

Example output:

.. testoutput:: kv_v2

    Version 1 of secret under path "hvac" contains the following keys: dict_keys(['pssst'])
    Version 1 of secret under path "hvac" created at: ...



Create/Update Secret
--------------------

.. automethod:: hvac.api.secrets_engines.KvV2.read_configuration
   :noindex:

Examples
````````

.. testcode:: kv_v2

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    client.secrets.kv.v2.create_or_update_secret(
        path='hvac',
        secret=dict(pssst='this is secret'),
        mount_point='kv',
    )

`cas` parameter with an argument that doesn't match the current version:

.. testcode:: kv_v2

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    # Assuming a current version of "6" for the path "hvac" =>
    client.secrets.kv.v2.create_or_update_secret(
        path='hvac',
        secret=dict(pssst='this is secret'),
        cas=5,
        mount_point='kv',
    )  # Raises hvac.exceptions.InvalidRequest


Example output:

.. testoutput:: kv_v2

    Traceback (most recent call last):
    ...
    hvac.exceptions.InvalidRequest: check-and-set parameter did not match the current version

`cas` parameter set to `0` will only succeed if the path hasn't already been written.

.. testcode:: kv_v2

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    client.secrets.kv.v2.create_or_update_secret(
        path='hvac',
        secret=dict(pssst='this is secret #1'),
        cas=0,
        mount_point='kv',
    )

    client.secrets.kv.v2.create_or_update_secret(
        path='hvac',
        secret=dict(pssst='this is secret #2'),
        cas=0,
        mount_point='kv',
    )  # => Raises hvac.exceptions.InvalidRequest

Example output:

.. testoutput:: kv_v2

    Traceback (most recent call last):
    ...
    hvac.exceptions.InvalidRequest: check-and-set parameter did not match the current version

Patch Existing Secret
---------------------

Method (similar to the Vault CLI command `vault kv patch`) to update an existing path. Either to add a new key/value to the secret and/or update the value for an existing key. Raises an :py:class:`hvac.exceptions.InvalidRequest` if the path hasn't been written to previously.

.. automethod:: hvac.api.secrets_engines.KvV2.patch
   :noindex:


Examples
````````

.. testcode:: kv_v2

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    client.secrets.kv.v2.patch(
        path='hvac',
        secret=dict(pssst='this is a patched secret'),
        mount_point='kv',
    )


Delete Latest Version of Secret
-------------------------------

.. automethod:: hvac.api.secrets_engines.KvV2.delete_latest_version_of_secret
   :noindex:

Examples
````````

.. testcode:: kv_v2

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    client.secrets.kv.v2.delete_latest_version_of_secret(
        path=hvac,
        mount_point='kv',
    )

Delete Secret Versions
----------------------

.. automethod:: hvac.api.secrets_engines.KvV2.delete_secret_versions
   :noindex:

Examples
````````

Marking the first 3 versions of a secret deleted under path "hvac":

.. testcode:: kv_v2

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    client.secrets.kv.v2.delete_secret_versions(
        path='hvac',
        versions=[1, 2, 3],
        mount_point='kv',
    )

Undelete Secret Versions
------------------------

.. automethod:: hvac.api.secrets_engines.KvV2.undelete_secret_versions
   :noindex:

Examples
````````

Marking the last 3 versions of a secret deleted under path "hvac" as "undeleted":

.. testcode:: kv_v2

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    hvac_path_metadata = client.secrets.kv.v2.read_secret_metadata(
        path='hvac',
        mount_point='kv',
    )

    oldest_version = hvac_path_metadata['data']['oldest_version']
    current_version = hvac_path_metadata['data']['current_version']
    versions_to_undelete = list(range(max(oldest_version, current_version - 2), current_version + 1))

    client.secrets.kv.v2.undelete_secret_versions(
        path='hvac',
        versions=versions_to_undelete,
        mount_point='kv',
    )

Destroy Secret Versions
-----------------------

.. automethod:: hvac.api.secrets_engines.KvV2.destroy_secret_versions
   :noindex:

Examples
````````

Destroying the first three versions of a secret under path 'hvac':

.. testcode:: kv_v2

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    client.secrets.kv.v2.destroy_secret_versions(
        path='hvac',
        versions=[1, 2, 3],
        mount_point='kv',
    )

List Secrets
------------

.. automethod:: hvac.api.secrets_engines.KvV2.list_secrets
   :noindex:

Examples
````````

Listing secrets under the 'hvac' path prefix:

.. testcode:: kv_v2

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    client.secrets.kv.v2.create_or_update_secret(
        path='hvac/big-ole-secret',
        secret=dict(pssst='this is a large secret'),
        mount_point='kv',
    )

    client.secrets.kv.v2.create_or_update_secret(
        path='hvac/lil-secret',
        secret=dict(pssst='this secret... not so big'),
        mount_point='kv',
    )

    list_response = client.secrets.kv.v2.list_secrets(
        path='hvac',
        mount_point='kv',
    )

    print('The following paths are available under "hvac" prefix: {keys}'.format(
        keys=', '.join(list_response['data']['keys']),
    ))

Example output:

.. testoutput:: kv_v2

    The following paths are available under "hvac" prefix: big-ole-secret, lil-secret


Read Secret Metadata
--------------------

.. automethod:: hvac.api.secrets_engines.KvV2.read_secret_metadata
   :noindex:

Examples
````````

.. testcode:: kv_v2

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    hvac_path_metadata = client.secrets.kv.v2.read_secret_metadata(
        path='hvac',
        mount_point='kv',
    )

    print('Secret under path hvac is on version {cur_ver}, with an oldest version of {old_ver}'.format(
        cur_ver=hvac_path_metadata['data']['oldest_version'],
        old_ver=hvac_path_metadata['data']['current_version'],
    ))

Example output:

.. testoutput:: kv_v2

    Secret under path hvac is on version 0, with an oldest version of 3

Update Metadata
---------------

.. automethod:: hvac.api.secrets_engines.KvV2.update_metadata
   :noindex:

Examples
````````

Set max versions for a given path ("hvac") to 3:

.. testcode:: kv_v2

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    client.secrets.kv.v2.update_metadata(
        path='hvac',
        max_versions=3,
        mount_point='kv',
    )

Set cas (check-and-set) parameter as required for a given path ("hvac"):

.. testcode:: kv_v2

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    client.secrets.kv.v2.update_metadata(
        path='hvac',
        cas_required=True,
        mount_point='kv',
    )


Delete Metadata and All Versions
--------------------------------

.. automethod:: hvac.api.secrets_engines.KvV2.delete_metadata_and_all_versions
   :noindex:

Examples
````````

Delete all versions and metadata for a given path:

.. testcode:: kv_v2

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    client.secrets.kv.v2.delete_metadata_and_all_versions(
        path='hvac',
        mount_point='kv',
    )
