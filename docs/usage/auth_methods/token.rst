Token
=====

.. contents::
   :local:
   :depth: 1

Authentication
--------------

Examples
````````
.. testcode:: token

    import hvac


    client = hvac.Client(url='https://127.0.0.1:8200')

    client.token = os.environ['VAULT_TOKEN']
    print('Authentication status: {is_authenticated}'.format(
        is_authenticated=client.is_authenticated(),
    ))

Example output:

.. testoutput:: token

    Authentication status: True

Token Management
----------------

Token Creation and Revocation
`````````````````````````````

.. testsetup:: token

    token_a = client.create_token(policies=['root'], lease='1h')['auth']['client_token']
    token_x = client.create_token(policies=['root'], lease='1h')['auth']['client_token']
    token_y = client.create_token(policies=['root'], lease='1h')['auth']['client_token']
    token_z = client.create_token(policies=['root'], lease='1h')['auth']['client_token']
    token_z_prefix = token_z[:5]

.. testcode:: token

    import hvac


    client = hvac.Client(url='https://127.0.0.1:8200')

    token = client.create_token(policies=['root'], lease='1h')

    current_token = client.lookup_token()
    some_other_token = client.lookup_token(token_x)

    client.revoke_token(token_x)
    client.revoke_token(token_y, orphan=True)

    client.renew_token(token_a)


Lookup and Revoke Tokens
````````````````````````

.. testcode:: token

    import hvac


    client = hvac.Client(url='https://127.0.0.1:8200')

    token = client.create_token(policies=['root'], lease='1h')
    token_accessor = token['auth']['accessor']

    same_token = client.lookup_token(token_accessor, accessor=True)
    client.revoke_token(token_accessor, accessor=True)

Wrapping/unwrapping a Token
```````````````````````````

.. testcode:: token

    import hvac


    client = hvac.Client(url='https://127.0.0.1:8200')

    wrap = client.create_token(policies=['root'], lease='1h', wrap_ttl='1m')
    result = client.sys.unwrap(wrap['wrap_info']['token'])
