Identity
========

.. contents::
   :local:
   :depth: 1

.. versionadded:: Vault 0.9.0

Entity
------

Create Or Update Entity
```````````````````````

.. automethod:: hvac.api.secrets_engines.Identity.create_or_update_entity
   :noindex:

Examples
````````

Creating an entity:

.. testcode:: identity-create-or-update-entity

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    create_response = client.secrets.identity.create_or_update_entity(
        name='hvac-entity',
        metadata=dict(extra_datas='yup'),
    )
    entity_id = create_response['data']['id']
    print('Entity ID for "hvac-entity" is: {id}'.format(id=entity_id))

Example output:

.. testoutput:: identity-create-or-update-entity

    Entity ID for "hvac-entity" is: ...


Updating an entity:

.. testcode:: identity-create-or-update-entity

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    update_response = client.secrets.identity.create_or_update_entity(
        name='hvac-entity-new-name',
        entity_id=entity_id,
    )
    entity_name = update_response['data']['name']
    print('Name for entity ID {id} updated to: {name}'.format(id=entity_id, name=entity_name))

Example output:

.. testoutput:: identity-create-or-update-entity

    Name for entity ID ... updated to: hvac-entity-new-name

.. testcleanup:: identity-create-or-update-entity

    client.secrets.identity.delete_entity(
        entity_id=entity_id,
    )

Create Or Update Entity By Name
```````````````````````````````

.. automethod:: hvac.api.secrets_engines.Identity.create_or_update_entity_by_name
   :noindex:

Examples
````````

.. testcode:: identity-create-or-update-entity-by-name

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    create_response = client.secrets.identity.create_or_update_entity_by_name(
        name='hvac-entity',
        metadata=dict(new_datas='uhuh'),
    )
    entity_id = create_response['data']['id']
    print('Entity ID for "hvac-entity" is: {id}'.format(id=entity_id))

Example output:

.. testoutput:: identity-create-or-update-entity-by-name

    Entity ID for "hvac-entity" is: ...

.. testcleanup:: identity-create-or-update-entity-by-name

    client.secrets.identity.delete_entity(
        entity_id=entity_id,
    )

Read Entity
```````````

.. automethod:: hvac.api.secrets_engines.Identity.read_entity
   :noindex:

Examples
````````

.. testsetup:: identity-read-entity

    client.secrets.identity.create_or_update_entity_by_name(
        name='hvac-entity',
        metadata=dict(new_datas='uhuh'),
    )

    read_response = client.secrets.identity.read_entity_by_name(
        name='hvac-entity',
    )
    entity_id = read_response['data']['id']

.. testcode:: identity-read-entity

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    read_response = client.secrets.identity.read_entity(
        entity_id=entity_id,
    )
    name = read_response['data']['name']
    print('Name for entity ID {id} is: {name}'.format(id=entity_id, name=name))

Example output:

.. testoutput:: identity-read-entity

   Name for entity ID ... is: hvac-entity


Read Entity By Name
```````````````````

.. versionadded:: Vault 0.11.2

.. automethod:: hvac.api.secrets_engines.Identity.read_entity_by_name
   :noindex:

Examples
````````

.. testcode:: identity-read-entity

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    read_response = client.secrets.identity.read_entity_by_name(
        name='hvac-entity',
    )
    entity_id = read_response['data']['id']
    print('Entity ID for "hvac-entity" is: {id}'.format(id=entity_id))

Example output:

.. testoutput:: identity-read-entity

    Entity ID for "hvac-entity" is: ...


Update Entity
`````````````

.. automethod:: hvac.api.secrets_engines.Identity.update_entity
   :noindex:

Examples
````````

.. testsetup:: identity-update-entity

    create_response = client.secrets.identity.create_or_update_entity(
        name='hvac-entity',
        metadata=dict(extra_datas='yup'),
    )
    entity_id = create_response['data']['id']

.. testcode:: identity-update-entity

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    client.secrets.identity.update_entity(
        entity_id=entity_id,
        metadata=dict(new_metadata='yup'),
    )

Delete Entity
`````````````

.. automethod:: hvac.api.secrets_engines.Identity.delete_entity
   :noindex:

Examples
````````

.. testcode:: identity

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    client.secrets.identity.delete_entity(
        entity_id='some-entity-id',
    )


Delete Entity By Name
`````````````````````

.. versionadded:: Vault 0.11.2

.. automethod:: hvac.api.secrets_engines.Identity.delete_entity_by_name
   :noindex:

Examples
````````

.. testcode:: identity

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    client.secrets.identity.delete_entity_by_name(
        name='hvac-entity',
    )

List Entities
`````````````

.. automethod:: hvac.api.secrets_engines.Identity.list_entities
   :noindex:

Examples
````````

.. testsetup:: identity-read-entity

    client.secrets.identity.create_or_update_entity_by_name(
        name='hvac-entity',
        metadata=dict(new_datas='uhuh'),
    )

.. testcode:: identity-read-entity

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    list_response = client.secrets.identity.list_entities()
    entity_keys = list_response['data']['keys']
    print('The following entity IDs are currently configured: {keys}'.format(keys=entity_keys))

Example output:

.. testoutput:: identity-read-entity

    The following entity IDs are currently configured: ...


List Entities By Name
`````````````````````

.. versionadded:: Vault 0.11.2

.. automethod:: hvac.api.secrets_engines.Identity.list_entities_by_name
   :noindex:

Examples
````````

.. testcode:: identity-read-entity

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    list_response = client.secrets.identity.list_entities_by_name()
    entity_keys = list_response['data']['keys']
    print('The following entity names are currently configured: {keys}'.format(keys=', '.join(entity_keys)))

Example output:

.. testoutput:: identity-read-entity

    The following entity names are currently configured: hvac-entity

Merge Entities
``````````````

.. automethod:: hvac.api.secrets_engines.Identity.merge_entities
   :noindex:

Examples
````````

.. testsetup:: identity-merge-entities

    client.secrets.identity.create_or_update_entity_by_name(
        name='hvac-entity-old',
        metadata=dict(new_datas='uhuh'),
    )

    read_response = client.secrets.identity.read_entity_by_name(
        name='hvac-entity-old',
    )
    from_entity_ids = [read_response['data']['id']]

    client.secrets.identity.create_or_update_entity_by_name(
        name='hvac-entity',
        metadata=dict(new_datas='uhuh'),
    )

    read_response = client.secrets.identity.read_entity_by_name(
        name='hvac-entity',
    )
    to_entity_id = read_response['data']['id']

.. testcode:: identity-merge-entities

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    list_response = client.secrets.identity.list_entities_by_name()
    print('Pre-merge entities: {keys}'.format(keys=', '.join(sorted(list_response['data']['keys']))))

    client.secrets.identity.merge_entities(
        from_entity_ids=from_entity_ids,
        to_entity_id=to_entity_id,
    )

    list_response = client.secrets.identity.list_entities_by_name()
    entity_keys = list_response['data']['keys']
    print('Post-merge entities: {keys}'.format(keys=', '.join(sorted(list_response['data']['keys']))))

Example output:

.. testoutput:: identity-merge-entities

    Pre-merge entities: hvac-entity, hvac-entity-old
    Post-merge entities: hvac-entity

Entity Alias
------------

Create Or Update Entity Alias
`````````````````````````````

.. automethod:: hvac.api.secrets_engines.Identity.create_or_update_entity_alias
   :noindex:

Examples
````````

.. testsetup:: identity-create-or-update-entity-alias

    create_response = client.secrets.identity.create_or_update_entity(
        name='hvac-entity',
        metadata=dict(extra_datas='yup'),
    )
    entity_id = create_response['data']['id']

    test_approle_path = 'identity-test-approle'
    client.sys.enable_auth_method(
        method_type='approle',
        path=test_approle_path,
    )
    list_auth_response = client.sys.list_auth_methods()
    hvac_approle_accessor = list_auth_response['data']['%s/' % test_approle_path]['accessor']

.. testcode:: identity-create-or-update-entity-alias

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    create_response = client.secrets.identity.create_or_update_entity_alias(
        name='hvac-entity-alias',
        canonical_id=entity_id,
        mount_accessor=hvac_approle_accessor,
    )
    alias_id = create_response['data']['id']
    print('Alias ID for "hvac-entity-alias" is: {id}'.format(id=alias_id))

Example output:

.. testoutput:: identity-create-or-update-entity-alias

    Alias ID for "hvac-entity-alias" is: ...

.. testcleanup:: identity-create-or-update-entity-alias

    client.secrets.identity.delete_entity_alias(
        alias_id=alias_id,
    )
    client.sys.disable_auth_method(
        path=test_approle_path,
    )

Update Entity Alias
```````````````````

.. automethod:: hvac.api.secrets_engines.Identity.update_entity_alias
   :noindex:

Examples
````````

.. testsetup:: identity-update-entity-alias

    create_response = client.secrets.identity.create_or_update_entity(
        name='hvac-entity',
        metadata=dict(extra_datas='yup'),
    )
    entity_id = create_response['data']['id']

    test_approle_path = 'identity-test-approle'
    client.sys.enable_auth_method(
        method_type='approle',
        path=test_approle_path,
    )
    list_auth_response = client.sys.list_auth_methods()
    hvac_approle_accessor = list_auth_response['data']['%s/' % test_approle_path]['accessor']

    create_response = client.secrets.identity.create_or_update_entity_alias(
        name='hvac-entity-alias',
        canonical_id=entity_id,
        mount_accessor=hvac_approle_accessor,
    )
    alias_id = create_response['data']['id']

.. testcode:: identity-update-entity-alias

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    client.secrets.identity.update_entity_alias(
        alias_id=alias_id,
        name='new-alias-name',
        canonical_id=entity_id,
        mount_accessor=hvac_approle_accessor,
    )

Read Entity Alias
`````````````````

.. automethod:: hvac.api.secrets_engines.Identity.read_entity_alias
   :noindex:

Examples
````````

.. testsetup:: identity-read-entity-alias

    create_response = client.secrets.identity.create_or_update_entity(
        name='hvac-entity',
        metadata=dict(extra_datas='yup'),
    )
    entity_id = create_response['data']['id']

    test_approle_path = 'identity-test-approle'
    client.sys.enable_auth_method(
        method_type='approle',
        path=test_approle_path,
    )
    list_auth_response = client.sys.list_auth_methods()
    hvac_approle_accessor = list_auth_response['data']['%s/' % test_approle_path]['accessor']

    create_response = client.secrets.identity.create_or_update_entity_alias(
        name='hvac-entity-alias',
        canonical_id=entity_id,
        mount_accessor=hvac_approle_accessor,
    )
    alias_id = create_response['data']['id']

.. testcode:: identity-read-entity-alias

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    read_response = client.secrets.identity.read_entity_alias(
        alias_id=alias_id,
    )
    name = read_response['data']['name']
    print('Name for entity alias {id} is: {name}'.format(id=alias_id, name=name))

Example output:

.. testoutput:: identity-read-entity-alias

    Name for entity alias ... is: hvac-entity-alias

List Entity Aliases
```````````````````

.. automethod:: hvac.api.secrets_engines.Identity.list_entity_aliases
   :noindex:

Examples
````````

.. testcode:: identity-read-entity-alias

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    list_response = client.secrets.identity.list_entity_aliases()
    alias_keys = list_response['data']['keys']
    print('The following entity alias IDs are currently configured: {keys}'.format(keys=', '.join(alias_keys)))

Example output:

.. testoutput:: identity-read-entity-alias

    The following entity alias IDs are currently configured: ...

Delete Entity Alias
```````````````````

.. automethod:: hvac.api.secrets_engines.Identity.delete_entity_alias
   :noindex:

Examples
````````

.. testcode:: identity

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    client.secrets.identity.delete_entity_alias(
        alias_id='some-alias-id',
    )

Group
-----

.. testsetup:: identity-groups

    create_response = client.secrets.identity.create_or_update_group(
        name='hvac-group',
        metadata=dict(extra_datas='we gots em'),
    )
    group_id = create_response['data']['id']

Create Or Update Group
``````````````````````

.. automethod:: hvac.api.secrets_engines.Identity.create_or_update_group
   :noindex:

Examples
````````

.. testcode:: identity-create-or-update-group

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    create_response = client.secrets.identity.create_or_update_group(
        name='hvac-group',
        metadata=dict(extra_datas='we gots em'),
    )
    group_id = create_response['data']['id']
    print('Group ID for "hvac-group" is: {id}'.format(id=group_id))

Example output:

.. testoutput:: identity-create-or-update-group

    Group ID for "hvac-group" is: ...

Update Group
````````````

.. automethod:: hvac.api.secrets_engines.Identity.update_group
   :noindex:

Examples
````````

.. testcode:: identity-create-or-update-group

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    client.secrets.identity.update_group(
        name='hvac-group',
        group_id=group_id,
        metadata=dict(new_metadata='yup'),
    )


Create Or Update Group By Name
``````````````````````````````

.. versionadded:: Vault 0.11.2

.. automethod:: hvac.api.secrets_engines.Identity.create_or_update_group_by_name
   :noindex:

Examples
````````

.. testcode:: identity-create-or-update-group

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    client.secrets.identity.create_or_update_group_by_name(
        name='hvac-group',
        metadata=dict(new_datas='uhuh'),
    )


Read Group
``````````

.. automethod:: hvac.api.secrets_engines.Identity.read_group
   :noindex:

Examples
````````

.. testcode:: identity-groups

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    read_response = client.secrets.identity.read_group(
        group_id=group_id,
    )
    name = read_response['data']['name']
    print('Name for group ID {id} is: {name}'.format(id=group_id, name=name))

.. testoutput:: identity-groups

    Name for group ID ... is: hvac-group


Read Group By Name
``````````````````

.. versionadded:: Vault 0.11.2

.. automethod:: hvac.api.secrets_engines.Identity.read_group_by_name
   :noindex:

Examples
````````

.. testcode:: identity-groups

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    read_response = client.secrets.identity.read_group_by_name(
        name='hvac-group',
    )
    group_id = read_response['data']['id']
    print('Group ID for "hvac-group" is: {id}'.format(id=group_id))

Example output:

.. testoutput:: identity-groups

    Group ID for "hvac-group" is: ...

List Groups
```````````

.. automethod:: hvac.api.secrets_engines.Identity.list_groups
   :noindex:

Examples
````````

.. testcode:: identity-groups

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    list_response = client.secrets.identity.list_groups()
    group_keys = list_response['data']['keys']
    print('The following group IDs are currently configured: {keys}'.format(keys=', '.join(group_keys)))

Example output:

.. testoutput:: identity-groups

    The following group IDs are currently configured: ...


List Groups By Name
```````````````````

.. versionadded:: Vault 0.11.2

.. automethod:: hvac.api.secrets_engines.Identity.list_entities_by_name
   :noindex:

Examples
````````

.. testcode:: identity-groups

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    list_response = client.secrets.identity.list_groups_by_name()
    group_keys = list_response['data']['keys']
    print('The following group names are currently configured: {keys}'.format(keys=', '.join(group_keys)))

Example output:

.. testoutput:: identity-groups

    The following group names are currently configured: hvac-group


Delete Group
````````````

.. automethod:: hvac.api.secrets_engines.Identity.delete_group
   :noindex:

Examples
````````

.. testcode:: identity

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    client.secrets.identity.delete_group(
        group_id='some-group-id',
    )


Delete Group By Name
````````````````````

.. versionadded:: Vault 0.11.2

.. automethod:: hvac.api.secrets_engines.Identity.delete_group_by_name
   :noindex:

Examples
````````

.. testcode:: identity

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    client.secrets.identity.delete_group_by_name(
        name='hvac-group',
    )

Group Alias
-----------

.. testsetup:: identity-group-alias

    create_response = client.secrets.identity.create_or_update_group(
        name='hvac-group',
        metadata=dict(extra_datas='we gots em'),
        group_type='external',
    )
    group_id = create_response['data']['id']

    test_approle_path = 'identity-test-approle'
    client.sys.enable_auth_method(
        method_type='approle',
        path=test_approle_path,
    )
    list_auth_response = client.sys.list_auth_methods()
    hvac_approle_accessor = list_auth_response['data']['%s/' % test_approle_path]['accessor']

Create Or Update Group Alias
````````````````````````````

.. automethod:: hvac.api.secrets_engines.Identity.create_or_update_group_alias
   :noindex:

Examples
````````

.. testcode:: identity-group-alias

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    create_response = client.secrets.identity.create_or_update_group_alias(
            name='hvac-group-alias',
            canonical_id=group_id,
            mount_accessor=hvac_approle_accessor,
        )
    alias_id = create_response['data']['id']
    print('Group alias ID for "hvac-group_alias" is: {id}'.format(id=alias_id))

Example output:

.. testoutput:: identity-group-alias

    Group alias ID for "hvac-group_alias" is: ...


Update Group Alias
``````````````````

.. automethod:: hvac.api.secrets_engines.Identity.update_group_alias
   :noindex:

Examples
````````

.. testcode:: identity-group-alias

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    client.secrets.identity.update_group_alias(
        alias_id=alias_id,
        name='hvac-group-alias',
        canonical_id=group_id,
        mount_accessor=hvac_approle_accessor,
    )


Read Group Alias
````````````````

.. automethod:: hvac.api.secrets_engines.Identity.read_group_alias
   :noindex:

Examples
````````

.. testcode:: identity-group-alias

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    read_response = client.secrets.identity.read_group_alias(
        alias_id=alias_id,
    )
    name = read_response['data']['name']
    print('Name for group alias {id} is: {name}'.format(id=alias_id, name=name))

Example output:

.. testoutput:: identity-group-alias

    Name for group alias ... is: hvac-group-alias


List Group Aliases
``````````````````

.. automethod:: hvac.api.secrets_engines.Identity.list_group_aliases
   :noindex:

Examples
````````

.. testcode:: identity-group-alias

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    list_response = client.secrets.identity.list_group_aliases()
    alias_keys = list_response['data']['keys']
    print('The following group alias IDs are currently configured: {keys}'.format(keys=', '.join(alias_keys)))

Example output:

.. testoutput:: identity-group-alias

    The following group alias IDs are currently configured: ...


Delete Group Alias
``````````````````

.. automethod:: hvac.api.secrets_engines.Identity.delete_group_alias
   :noindex:

Examples
````````

.. testcode:: identity

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    client.secrets.identity.delete_group_alias(
        alias_id='some-alias-id',
    )

Lookup
------

.. testsetup:: identity-lookup

    client.secrets.identity.create_or_update_entity_by_name(
        name='hvac-entity',
        metadata=dict(new_datas='uhuh'),
    )

    client.secrets.identity.create_or_update_group(
        name='hvac-group',
        metadata=dict(extra_datas='we gots em'),
    )

Lookup Entity
`````````````

.. automethod:: hvac.api.secrets_engines.Identity.lookup_entity
   :noindex:

Examples
````````

.. testcode:: identity-lookup

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    lookup_response = client.secrets.identity.lookup_entity(
        name='hvac-entity',
    )
    entity_id = lookup_response['data']['id']
    print('Entity ID for "hvac-entity" is: {id}'.format(id=entity_id))

Example output:

.. testoutput:: identity-lookup

    Entity ID for "hvac-entity" is: ...


Lookup Group
````````````

.. automethod:: hvac.api.secrets_engines.Identity.lookup_group
   :noindex:

Examples
````````

.. testcode:: identity-lookup

    import hvac
    client = hvac.Client(url='https://127.0.0.1:8200')

    lookup_response = client.secrets.identity.lookup_group(
        name='hvac-group',
    )
    group_id = lookup_response['data']['id']
    print('Group ID for "hvac-entity" is: {id}'.format(id=group_id))

Example output:

.. testoutput:: identity-lookup

    Group ID for "hvac-entity" is: ...
