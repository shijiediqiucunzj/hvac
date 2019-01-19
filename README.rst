
hvac
====


.. image:: https://raw.githubusercontent.com/hvac/hvac/master/docs/_static/hvac_logo_800px.png
   :target: https://raw.githubusercontent.com/hvac/hvac/master/docs/_static/hvac_logo_800px.png
   :alt: Header image


`HashiCorp <https://hashicorp.com/>`_ `Vault <https://www.vaultproject.io>`_ API client for Python 2.7/3.x


.. image:: https://travis-ci.org/hvac/hvac.svg?branch=master
   :target: https://travis-ci.org/hvac/hvac
   :alt: Travis CI


.. image:: https://codecov.io/gh/hvac/hvac/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/hvac/hvac
   :alt: codecov


.. image:: https://readthedocs.org/projects/hvac/badge/
   :target: https://hvac.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status


.. image:: https://badge.fury.io/py/hvac.svg
   :target: https://badge.fury.io/py/hvac
   :alt: PyPI version


.. image:: https://img.shields.io/twitter/follow/python_hvac.svg?label=Twitter%20-%20@python_hvac&style=social?style=plastic
   :target: https://twitter.com/python_hvac
   :alt: Twitter - @python_hvac


Tested against the latest release, HEAD ref, and 3 previous major versions (counting back from the latest release) of Vault. 
Currently supports Vault v0.9.6 or later.

Documentation
-------------

Documentation for this module is hosted on `readthedocs.io <https://hvac.readthedocs.io/en/latest/>`_.

Getting started
---------------

Installation
^^^^^^^^^^^^

.. code-block:: bash

   pip install hvac

or

.. code-block:: bash

   pip install "hvac[parser]"

if you would like to be able to return parsed HCL data as a Python dict for methods that support it.

Initialize the Client
^^^^^^^^^^^^^^^^^^^^^

Using TLS:

.. doctest:: init

    >>> client = hvac.Client(url='https://localhost:8200')
    >>> client.is_authenticated()
    True


Using TLS with client-side certificate authentication:

.. doctest:: init

    >>> client = hvac.Client(
    ...     url='https://localhost:8200',
    ...     token=os.environ['VAULT_TOKEN'],
    ...     cert=(client_cert_path, client_key_path),
    ...     verify=server_cert_path,
    ... )
    >>> client.is_authenticated()
    True


Using `Vault Enterprise namespace <https://www.vaultproject.io/docs/enterprise/namespaces/index.html>`_\ :

.. doctest:: init

    >>> client = hvac.Client(
    ...     url='https://localhost:8200',
    ...     namespace=os.getenv('VAULT_NAMESPACE'),
    ... )


Using plaintext / HTTP (not recommended for anything other than development work):

.. doctest::

    >>> client = hvac.Client(url='http://localhost:8200')


Read and write to secrets engines
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. testsetup:: kvv2
   :skipif: test_utils.vault_version_lt('0.10.0')

   from time import sleep


   resp = client.sys.tune_mount_configuration(
        path='secret',
        options=dict(version=2)
   )
   sleep(1)


.. doctest:: kvv2
   :skipif: test_utils.vault_version_lt('0.10.0')

    >>> client = test_utils.create_client()
    >>> create_resp = client.secrets.kv.create_or_update_secret('secret/foo', secret=dict(baz='bar'))
    >>> print('Created secret version "{ver}" at path "secret/foo"!'.format(
    ...     ver=create_resp['data']['version'],
    ... ))
    Created secret version "1" at path "secret/foo"!
    >>> read_response = client.secrets.kv.read_secret_version('secret/foo')
    >>> read_response['data']['data']['baz']
    'bar'
    >>> client.secrets.kv.delete_metadata_and_all_versions('secret/foo')
    <Response [204]>



.. code-block:: python

   import os

   import hvac

   # Using plaintext
   client = hvac.Client()
   client = hvac.Client(url='http://localhost:8200')
   client = hvac.Client(url='http://localhost:8200', token=os.environ['VAULT_TOKEN'])

   # Using TLS
   client = hvac.Client(url='https://localhost:8200')

   # Using TLS with client-side certificate authentication
   client = hvac.Client(url='https://localhost:8200', cert=('path/to/cert.pem', 'path/to/key.pem'))

   # Using Namespace
   client = hvac.Client(url='http://localhost:8200', token=os.environ['VAULT_TOKEN'], namespace=os.environ['VAULT_NAMESPACE'])

Read and write to secret backends
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   client.write('secret/foo', baz='bar', lease='1h')

   print(client.read('secret/foo'))

   client.delete('secret/foo')

Authenticate using token auth backend
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Token
   client.token = 'MY_TOKEN'
   assert client.is_authenticated() # => True
