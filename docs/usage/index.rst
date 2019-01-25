Usage
=====

.. toctree::
   :maxdepth: 2

   secrets_engines/index
   auth_methods/index
   system_backend/index

Initialize and seal/unseal
--------------------------

.. testsetup:: init-seal-and-unseal

    manager.restart_vault_cluster(perform_init=False)
    client.token = manager.root_token

.. doctest:: init-seal-and-unseal

    >>> client.sys.is_initialized()
    False

    >>> shares = 5
    >>> threshold = 3
    >>> result = client.sys.initialize(shares, threshold)
    >>> root_token = result['root_token']
    >>> keys = result['keys']
    >>> client.sys.is_initialized()
    True

    >>> client.token = root_token

    >>> client.sys.is_sealed()
    True
    >>> # Unseal a Vault cluster with individual keys
    >>> unseal_response1 = client.sys.submit_unseal_key(keys[0])
    >>> unseal_response2 = client.sys.submit_unseal_key(keys[1])
    >>> unseal_response3 = client.sys.submit_unseal_key(keys[2])
    >>> client.sys.is_sealed()
    False
    >>> # Seal a previously unsealed Vault cluster.
    >>> client.sys.seal()
    <Response [204]>
    >>> client.sys.is_sealed()
    True

    >>> # Unseal with multiple keys until threshold met
    >>> unseal_response = client.sys.submit_unseal_keys(keys)

    >>> client.sys.is_sealed()
    False

.. testcleanup:: init-seal-and-unseal

    manager.restart_vault_cluster(perform_init=True)
    client.token = manager.root_token
