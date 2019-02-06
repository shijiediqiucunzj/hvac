KV - Version 1
==============

.. contents::
   :local:
   :depth: 1



Read a Secret
-------------

.. automethod:: hvac.api.secrets_engines.KvV1.read_secret
   :noindex:

Examples
````````
.. testsetup:: kv_v1_read
    :skipif: client.sys.retrieve_mount_option('secret', 'version', '1') != '1' and os.getenv('HVAC_RENDER_DOCTESTS') is None

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    hvac_secret = {
        'psst': 'this is so secret yall',
    }
    client.secrets.kv.v1.create_or_update_secret(
        path='hvac',
        secret=hvac_secret,
    )

.. testcode:: kv_v1_read
    :skipif: client.sys.retrieve_mount_option('secret', 'version', '1') != '1' and os.getenv('HVAC_RENDER_DOCTESTS') is None

    import hvac

    client = hvac.Client(url='https://127.0.0.1:8200')


    read_secret_result = client.secrets.kv.v1.read_secret(
        path='hvac',
    )
    print('The "psst" key under the secret path ("/v1/secret/hvac") is: {psst}'.format(
        psst=read_secret_result['data']['psst'],
    ))

Example output:

.. testoutput:: kv_v1_read

    The "psst" key under the secret path ("/v1/secret/hvac") is: this is so secret yall

List Secrets
------------

.. automethod:: hvac.api.secrets_engines.KvV1.list_secrets
   :noindex:

Examples
````````

.. testsetup:: kv_v1_list

    for num in range(1, 10):
        client.secrets.kv.v1.create_or_update_secret(
            path='hvac/secret{num}'.format(num=num),
            secret=dict(number=num),
        )

.. testcode:: kv_v1_list
    :skipif: client.sys.retrieve_mount_option('secret', 'version', '1') != '1' and os.getenv('HVAC_RENDER_DOCTESTS') is None

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    list_secrets_result = client.secrets.kv.v1.list_secrets(path='hvac')

    print('The following keys found under the selected path ("/v1/secret/hvac"): {keys}'.format(
        keys=', '.join(list_secrets_result['data']['keys']),
    ))

Example output:

.. testoutput:: kv_v1_list

    The following keys found under the selected path ("/v1/secret/hvac"): secret1, secret2, secret3, ...

Create or Update a Secret
-------------------------

.. automethod:: hvac.api.secrets_engines.KvV1.create_or_update_secret
   :noindex:

Examples
````````

.. testcode:: kv_v1_create_or_update
    :skipif: client.sys.retrieve_mount_option('secret', 'version', '1') != '1' and os.getenv('HVAC_RENDER_DOCTESTS') is None

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    hvac_secret = {
        'psst': 'this is so secret yall',
    }
    client.secrets.kv.v1.create_or_update_secret(
        path='hvac',
        secret=hvac_secret,
    )
    read_secret_result = client.secrets.kv.v1.read_secret(
        path='hvac',
    )
    print('The "psst" key under the secret path ("/v1/secret/hvac") is: {psst}'.format(
        psst=read_secret_result['data']['psst'],
    ))

    updated_hvac_secret = {
        'psst': 'this is now even more secret yall',
    }
    client.secrets.kv.v1.create_or_update_secret(
        path='hvac',
        secret=updated_hvac_secret,
    )
    read_secret_result = client.secrets.kv.v1.read_secret(
        path='hvac',
    )
    print('The updated "psst" key under the secret path ("/v1/secret/hvac") is: {psst}'.format(
        psst=read_secret_result['data']['psst'],
    ))

Example output:

.. testoutput:: kv_v1_create_or_update

    The "psst" key under the secret path ("/v1/secret/hvac") is: this is so secret yall
    The updated "psst" key under the secret path ("/v1/secret/hvac") is: this is now even more secret yall

Delete a Secret
---------------

.. automethod:: hvac.api.secrets_engines.KvV1.delete_secret
   :noindex:

Examples
````````

.. testcode:: kv_v1_delete
    :skipif: client.sys.retrieve_mount_option('secret', 'version', '1') != '1' and os.getenv('HVAC_RENDER_DOCTESTS') is None

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    client.secrets.kv.v1.delete_secret(
        path='hvac',
    )

    # The following will raise a :py:class:`hvac.exceptions.InvalidPath` exception.
    read_secret_result = client.secrets.kv.v1.read_secret(
        path='hvac',
    )

.. testoutput:: kv_v1_delete

    Traceback (most recent call last):
    ...
    hvac.exceptions.InvalidPath: None

