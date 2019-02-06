GitHub
======

.. contents::
   :local:
   :depth: 1

Configure Connection Parameters
-------------------------------

.. automethod:: hvac.api.auth_methods.Github.configure
   :noindex:

Examples
````````

.. testsetup:: github

    client = hvac.Client(url='https://127.0.0.1:8200')
    client.sys.enable_auth_method(
        method_type='github'
    )

.. testcode:: github

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    client.auth.github.configure(
        organization='our-lovely-company',
        max_ttl='48h',  # i.e., A given token can only be renewed for up to 48 hours
    )

Reading Configuration
---------------------

.. automethod:: hvac.api.auth_methods.Github.read_configuration
   :noindex:

Examples
````````

.. testcode:: github

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    github_config = client.auth.github.read_configuration()
    print('The Github auth method is configured with a max_ttl of: {max_ttl}'.format(
        max_ttl=github_config['data']['max_ttl']
    ))

Example output:

.. testoutput:: github

    The Github auth method is configured with a max_ttl of: 172800


Mapping Teams to Policies
-------------------------

.. automethod:: hvac.api.auth_methods.Github.map_team
   :noindex:

Examples
````````

.. testcode:: github

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    teams = [
        dict(name='some-dev-team', policies=['dev-team']),
        dict(name='admin-team', policies=['administrator']),
    ]
    for team in teams:
        client.auth.github.map_team(
            team_name=team['name'],
            policies=team['policies'],
        )

Reading Team Mappings
---------------------

.. automethod:: hvac.api.auth_methods.Github.read_team_mapping
   :noindex:

Examples
````````

.. testcode:: github

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    team_name = 'admin-team'
    read_team_response = client.auth.github.read_team_mapping(
        team_name=team_name,
    )
    print('The Github team {team} is mapped to the following policies: {policies}'.format(
        team=team_name,
        policies=read_team_response['data']['value'],
    ))

Example output:

.. testoutput:: github

    The Github team admin-team is mapped to the following policies: administrator


Mapping Users to Policies
-------------------------

.. automethod:: hvac.api.auth_methods.Github.map_user
   :noindex:

Examples
````````

.. testcode:: github

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    users = [
        dict(name='some-dev-user', policies=['dev-team']),
        dict(name='some-admin-user', policies=['administrator']),
    ]
    for user in users:
        client.auth.github.map_user(
            user_name=user['name'],
            policies=user['policies'],
        )

Reading User Mappings
---------------------

.. automethod:: hvac.api.auth_methods.Github.read_user_mapping
   :noindex:

Examples
````````

.. testcode:: github

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    user_name = 'some-dev-user'
    read_user_response = client.auth.github.read_user_mapping(
        user_name=user_name,
    )
    print('The Github user "{user}" is mapped to the following policies: {policies}'.format(
        user=user_name,
        policies=read_user_response['data']['value'],
    ))

Example output:

.. testoutput:: github

    The Github user "some-dev-user" is mapped to the following policies: dev-team

Authentication / Login
----------------------

.. automethod:: hvac.api.auth_methods.Github.login
   :noindex:

Examples
````````

Log in and automatically update the underlying "token" attribute on the :py:meth:`hvac.adapters.Adapter` instance:

.. testcode:: github

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')
    login_response = client.auth.github.login(token='some personal github token')



