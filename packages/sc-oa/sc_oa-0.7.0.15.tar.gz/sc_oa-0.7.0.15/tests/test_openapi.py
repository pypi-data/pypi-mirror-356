"""
    tests.test_openapi
    ------------------

    Tests some stuff of ``sphinxcontrib.openapi`` module.

    :copyright: (c) 2016, Ihor Kalnytskyi.
    :license: BSD, see LICENSE for details.
"""

import os
import textwrap
import collections

import py
import pytest

import yaml

from sphinxcontrib.openapi import renderers
from sphinxcontrib.openapi import openapi20
from sphinxcontrib.openapi import utils


class TestOpenApi2HttpDomain(object):

    def test_basic(self):
        renderer = renderers.HttpdomainOldRenderer(None, {})
        text = '\n'.join(renderer.render_restructuredtext_markup({
            'paths': {
                '/resources/{kind}': {
                    'get': {
                        'summary': 'List Resources',
                        'description': '~ some useful description ~',
                        'parameters': [
                            {
                                'name': 'kind',
                                'in': 'path',
                                'type': 'string',
                                'description': 'Kind of resource to list.',
                            },
                            {
                                'name': 'limit',
                                'in': 'query',
                                'type': 'integer',
                                'description': 'Show up to `limit` entries.',
                            },
                            {
                                'name': 'If-None-Match',
                                'in': 'header',
                                'type': 'string',
                                'description': 'Last known resource ETag.'
                            },
                        ],
                        'responses': {
                            '200': {
                                'description': 'An array of resources.',
                                'headers': {
                                    'ETag': {
                                        'description': 'Resource ETag.',
                                        'type': 'string'
                                    },
                                },
                            },
                        },
                    },
                },
            },
        }))

        assert text == textwrap.dedent('''
            .. http:get:: /resources/{kind}
               :synopsis: List Resources

               **List Resources**

               ~ some useful description ~

               :param string kind:
                  Kind of resource to list.
               :query integer limit:
                  Show up to `limit` entries.
               :status 200:
                  An array of resources.
               :reqheader If-None-Match:
                  Last known resource ETag.
               :resheader ETag:
                  Resource ETag.
        ''').lstrip()

    def test_groups(self):
        renderer = renderers.HttpdomainOldRenderer(None, {'group': True})
        text = '\n'.join(renderer.render_restructuredtext_markup({
            'tags': [
                {'name': 'tags'},
                {'name': 'pets'},
            ],
            'paths': collections.OrderedDict([
                ('/', {
                    'get': {
                        'summary': 'Index',
                        'description': '~ some useful description ~',
                        'responses': {
                            '200': {
                                'description': 'Index',
                                'content': {
                                    'application/json': {
                                        'pets': 'https://example.com/api/pets',
                                        'tags': 'https://example.com/api/tags',
                                    }
                                }
                            },
                        },
                    },
                }),
                ('/pets', {
                    'get': {
                        'summary': 'List Pets',
                        'description': '~ some useful description ~',
                        'responses': {
                            '200': {
                                'description': 'Pets',
                                'content': {
                                    'application/json': [
                                        {
                                            'example': '{"foo": "bar"}'
                                        },
                                    ],
                                },
                            },
                        },
                        'tags': [
                            'pets',
                        ],
                    },
                }),
                ('/pets/{name}', {
                    'get': {
                        'summary': 'Show Pet',
                        'description': '~ some useful description ~',
                        'parameters': [
                            {
                                'name': 'name',
                                'in': 'path',
                                'type': 'string',
                                'description': 'Name of pet.',
                            },
                        ],
                        'responses': {
                            '200': {
                                'description': 'A Pet',
                                'content': {
                                    'application/json': {
                                        'example': '{"foo": "bar"}'
                                    }
                                }
                            },
                        },
                        'tags': [
                            'pets',
                        ],
                    },
                }),
                ('/tags', {
                    'get': {
                        'summary': 'List Tags',
                        'description': '~ some useful description ~',
                        'responses': {
                            '200': {
                                'description': 'Tags',
                                'content': {
                                    'application/json': [
                                        {
                                            'example': '{"foo": "bar"}'
                                        },
                                    ],
                                }
                            },
                        },
                        'tags': [
                            'tags',
                            'pets',
                        ],
                    },
                }),
            ]),
        }))
        assert text == textwrap.dedent('''
            tags
            ====

            .. http:get:: /tags
               :synopsis: List Tags

               **List Tags**

               ~ some useful description ~

               :status 200:
                  Tags

            pets
            ====

            .. http:get:: /pets
               :synopsis: List Pets

               **List Pets**

               ~ some useful description ~

               :status 200:
                  Pets

            .. http:get:: /pets/{name}
               :synopsis: Show Pet

               **Show Pet**

               ~ some useful description ~

               :param string name:
                  Name of pet.
               :status 200:
                  A Pet

            default
            =======

            .. http:get:: /
               :synopsis: Index

               **Index**

               ~ some useful description ~

               :status 200:
                  Index
        ''').lstrip()

    def test_two_resources(self):
        spec = collections.defaultdict(collections.OrderedDict)
        spec['paths']['/resource_a'] = {
            'get': {
                'description': 'resource a',
                'responses': {
                    '200': {'description': 'ok'},
                }
            }
        }
        spec['paths']['/resource_b'] = {
            'post': {
                'description': 'resource b',
                'responses': {
                    '404': {'description': 'error'},
                }
            }
        }

        renderer = renderers.HttpdomainOldRenderer(None, {})
        text = '\n'.join(renderer.render_restructuredtext_markup(spec))
        assert text == textwrap.dedent('''
            .. http:get:: /resource_a
               :synopsis: null

               resource a

               :status 200:
                  ok

            .. http:post:: /resource_b
               :synopsis: null

               resource b

               :status 404:
                  error
        ''').lstrip()

    def test_path_option(self):
        spec = collections.defaultdict(collections.OrderedDict)
        spec['paths']['/resource_a'] = {
            'get': {
                'description': 'resource a',
                'responses': {
                    '200': {'description': 'ok'},
                }
            }
        }
        spec['paths']['/resource_b'] = {
            'post': {
                'description': 'resource b',
                'responses': {
                    '404': {'description': 'error'},
                }
            }
        }

        renderer = renderers.HttpdomainOldRenderer(None, {'paths': [
            '/resource_a',
        ]})
        text = '\n'.join(renderer.render_restructuredtext_markup(spec))
        assert text == textwrap.dedent('''
            .. http:get:: /resource_a
               :synopsis: null

               resource a

               :status 200:
                  ok
        ''').lstrip()

    def test_include_option(self):
        spec = collections.defaultdict(collections.OrderedDict)
        spec['openapi'] = '3.0.0'
        spec['paths']['/Aresource_a'] = {
            'get': {
                'description': 'resource a',
                'responses': {
                    '200': {'description': 'ok'},
                }
            }
        }
        spec['paths']['/Bresource_b'] = {
            'post': {
                'description': 'resource b',
                'responses': {
                    '404': {'description': 'error'},
                }
            }
        }

        renderer = renderers.HttpdomainOldRenderer(None, {'include': [
            '/resource',
            '/A.*',
            '/Bresource.*'
        ]})
        text = '\n'.join(renderer.render_restructuredtext_markup(spec))
        assert text == textwrap.dedent('''
            .. http:get:: /Aresource_a
               :synopsis: null

               resource a

               :status 200:
                  ok.

            .. http:post:: /Bresource_b
               :synopsis: null

               resource b

               :status 404:
                  error.
        ''').lstrip()

    def test_exclude_option(self):
        spec = collections.defaultdict(collections.OrderedDict)
        spec['openapi'] = '3.0.0'
        spec['paths']['/Aresource_a'] = {
            'get': {
                'description': 'resource a',
                'responses': {
                    '200': {'description': 'ok'},
                }
            }
        }
        spec['paths']['/Bresource_b'] = {
            'post': {
                'description': 'resource b',
                'responses': {
                    '404': {'description': 'error'},
                }
            }
        }

        renderer = renderers.HttpdomainOldRenderer(None, {'exclude': [
            '/.*_a',
            '/A.*',
        ]})
        text = '\n'.join(renderer.render_restructuredtext_markup(spec))
        assert text == textwrap.dedent('''
            .. http:post:: /Bresource_b
               :synopsis: null

               resource b

               :status 404:
                  error.
        ''').lstrip()

    def test_method_option(self):
        spec = collections.defaultdict(collections.OrderedDict)
        spec['openapi'] = '3.0'
        spec['paths']['/resource_a'] = {
            'get': {
                'description': 'resource a',
                'responses': {
                    '200': {'description': 'ok'},
                }
            },
            'post': {
                'description': 'resource a',
                'responses': {
                    '201': {'description': 'ok'},
                }
            },
            'put': {
                'description': 'resource a',
                'responses': {
                    '404': {'description': 'error'},
                }
            }
        }

        renderer = renderers.HttpdomainOldRenderer(
            None,
            {
                'methods': ['post'],
                'paths': ['/resource_a'],
            },
        )
        text = '\n'.join(renderer.render_restructuredtext_markup(spec))

        assert text == textwrap.dedent('''
            .. http:post:: /resource_a
               :synopsis: null

               resource a

               :status 201:
                  ok.
        ''').lstrip()

    def test_root_parameters(self):
        spec = {'paths': {}}
        spec['paths']['/resources/{name}'] = collections.OrderedDict()

        spec['paths']['/resources/{name}']['parameters'] = [
            {
                'name': 'name',
                'in': 'path',
                'type': 'string',
                'description': 'The name of the resource.',
            }
        ]
        spec['paths']['/resources/{name}']['get'] = {
            'summary': 'Fetch a Resource',
            'description': '~ some useful description ~',
            'responses': {
                '200': {
                    'description': 'The fetched resource.',
                },
            },
        }
        spec['paths']['/resources/{name}']['put'] = {
            'summary': 'Modify a Resource',
            'description': '~ some useful description ~',
            'responses': {
                '200': {
                    'description': 'The modified resource.',
                },
            },
        }

        renderer = renderers.HttpdomainOldRenderer(None, {})
        text = '\n'.join(renderer.render_restructuredtext_markup(spec))

        assert text == textwrap.dedent('''
            .. http:get:: /resources/{name}
               :synopsis: Fetch a Resource

               **Fetch a Resource**

               ~ some useful description ~

               :param string name:
                  The name of the resource.
               :status 200:
                  The fetched resource.

            .. http:put:: /resources/{name}
               :synopsis: Modify a Resource

               **Modify a Resource**

               ~ some useful description ~

               :param string name:
                  The name of the resource.
               :status 200:
                  The modified resource.
        ''').lstrip()

    def test_path_invalid(self):
        spec = collections.defaultdict(collections.OrderedDict)
        spec['paths']['/resource_a'] = {
            'get': {
                'description': 'resource a',
                'responses': {
                    '200': {'description': 'ok'},
                }
            }
        }
        spec['paths']['/resource_b'] = {
            'post': {
                'description': 'resource b',
                'responses': {
                    '404': {'description': 'error'},
                }
            }
        }

        renderer = renderers.HttpdomainOldRenderer(None, {'paths': [
            '/resource_a',
            '/resource_invalid_name',
        ]})

        with pytest.raises(ValueError) as exc:
            '\n'.join(renderer.render_restructuredtext_markup(spec))

        assert str(exc.value) == (
            'One or more paths are not defined in the spec: '
            '/resource_invalid_name.'
        )

    def test_unicode_is_allowed(self):
        spec = {
            'paths': {
                '/resource_a': {
                    'get': {
                        'description': '\u041f',
                        'responses': {
                            '200': {'description': 'ok'}
                        }
                    }
                }
            }
        }

        renderer = renderers.HttpdomainOldRenderer(None, {})
        text = '\n'.join(renderer.render_restructuredtext_markup(spec))

        assert text == textwrap.dedent('''
            .. http:get:: /resource_a
               :synopsis: null

               \u041f

               :status 200:
                  ok
        ''').lstrip()

    def test_json_in_out(self):
        renderer = renderers.HttpdomainOldRenderer(None, {})
        text = '\n'.join(renderer.render_restructuredtext_markup({
            'definitions': {
                'CreateResourceSchema': {
                    'additionalProperties': False,
                    'properties': {
                        'string_field': {
                            'type': 'string',
                            'description': 'some input string'
                        },
                        'int_field': {
                            'default': 1,
                            'type': 'integer',
                        },
                    },
                    'required': [
                        'string_field'
                    ],
                    'title': 'CreateResourceSchema',
                    'type': 'object'
                },
                'ResourceSchema': {
                    'properties': {
                        'string_field': {
                            'type': 'string',
                            'description': 'some output string'
                        },
                        'int_field': {
                            'type': 'integer',
                        },
                    },
                    'required': [
                        'string_field'
                    ],
                    'title': 'ResourceSchema',
                    'type': 'object'
                },
                'Error': {
                    'properties': {
                        'errors': {
                            'type': 'object'
                        },
                        'message': {
                            'type': 'string'
                        }
                    },
                    'required': [
                        'message'
                    ],
                    'title': 'Error',
                    'type': 'object'
                },
            },
            'paths': {
                '/resources': {
                    'post': {
                        'description': '~ some useful description ~',
                        'parameters': [
                            {
                                'in': 'body',
                                'name': 'CreateResourceSchema',
                                'required': True,
                                'schema': {
                                    '$ref':
                                        '#/definitions/CreateResourceSchema'
                                }
                            },
                        ],
                        'responses': {
                            '201': {
                                'description': '~ some useful description ~',
                                'schema': {
                                    '$ref': '#/definitions/ResourceSchema'
                                }
                            },
                            'default': {
                                'description': '~ some useful description ~',
                                'schema': {
                                    '$ref': '#/definitions/Error'
                                }
                            }
                        },
                    },
                },
            },
        }))

        text2 = textwrap.dedent('''
            .. http:post:: /resources
               :synopsis: null

               ~ some useful description ~


               :<json integer int_field:
               :<json string string_field: some input string (required)

               :status 201:
                  ~ some useful description ~
               :status default:
                  ~ some useful description ~

               :>json integer int_field:
               :>json string string_field: some output string (required)

        ''').lstrip()
        assert text == text2


class TestOpenApi3HttpDomain(object):

    def test_basic(self):
        renderer = renderers.HttpdomainOldRenderer(
            None,
            {
                'examples': True,
                'group_examples': True
            }
        )
        text = '\n'.join(renderer.render_restructuredtext_markup({
            'openapi': '3.0.0',
            'paths': {
                '/resources/{kind}': {
                    'get': {
                        'summary': 'List Resources',
                        'description': '~ some useful description ~',
                        'parameters': [
                            {
                                'name': 'kind',
                                'in': 'path',
                                'schema': {'type': 'string'},
                                'description': 'Kind of resource to list.',
                            },
                            {
                                'name': 'limit',
                                'in': 'query',
                                'schema': {'type': 'integer'},
                                'description': 'Show up to `limit` entries.',
                                'required': True,
                            },
                            {
                                'name': 'offset',
                                'in': 'query',
                                'schema': {'type': 'integer'},
                                'description': 'Start from offset.',
                            },
                            {
                                'name': 'If-None-Match',
                                'in': 'header',
                                'schema': {'type': 'string'},
                                'description': 'Last known resource ETag.'
                            },
                        ],
                        'requestBody': {
                            'content': {
                                'application/json':  {
                                    'example': '{"foo2": "bar2"}'
                                }
                            }
                        },
                        'responses': {
                            '200': {
                                'description': 'An array of resources.',
                                'content': {
                                    'application/json': {
                                        'example': '{"foo": "bar"}'
                                    }
                                }
                            },
                        },
                    },
                },
            },
        }))
        assert text == textwrap.dedent('''
            .. http:get:: /resources/{kind}
               :synopsis: List Resources

               **List Resources**

               ~ some useful description ~

               :param string kind:
                  Kind of resource to list.
               :query integer limit:
                  Show up to `limit` entries.
                  (Required)
               :query integer offset:
                  Start from offset.
               :reqheader If-None-Match:
                  Last known resource ETag.
               :status 200:
                  An array of resources.

               **Example request:**

               .. sourcecode:: http

                  GET /resources/string?limit=1&offset=1 HTTP/1.1
                  Host: example.com
                  Content-Type: application/json

                  {"foo2": "bar2"}


               **Example request:**

               .. sourcecode:: http

                  GET /resources/string?limit=1&offset=1 HTTP/1.1
                  Host: example.com


               **Example response:**

               .. sourcecode:: http

                  HTTP/1.1 200 OK
                  Content-Type: application/json

                  {"foo": "bar"}

        ''').lstrip()

    def test_rfc7807(self):
        # Fix order to have a reliable test
        pb_example = collections.OrderedDict()
        pb_example["type"] = "string"
        pb_example["title"] = "string"
        pb_example["status"] = 1
        pb_example["detail"] = "string"
        pb_example["instance"] = "string"
        renderer = renderers.HttpdomainOldRenderer(None, {'examples': True})
        text = '\n'.join(renderer.render_restructuredtext_markup({
            'openapi': '3.0.0',
            'paths': {
                '/problem': {
                    'post': {
                        'summary': 'Problem',
                        'description': '~ some useful description ~',
                        'requestBody': {
                            'content': {
                                'application/problem+json':  {
                                    'example': pb_example
                                }
                            }
                        },
                        'responses': {
                            '200': {
                                'description': 'An array of resources.',
                                'content': {
                                    'application/json': {
                                        'example': {"foo": "bar"}
                                    }
                                }
                            },
                        },
                    },
                },
            },
        }))
        assert text == textwrap.dedent('''
            .. http:post:: /problem
               :synopsis: Problem

               **Problem**

               ~ some useful description ~


               **Example request:**

               .. sourcecode:: http

                  POST /problem HTTP/1.1
                  Host: example.com
                  Content-Type: application/problem+json

                  {
                      "type": "string",
                      "title": "string",
                      "status": 1,
                      "detail": "string",
                      "instance": "string"
                  }

               :status 200:
                  An array of resources.

                  **Example response:**

                  .. sourcecode:: http

                     HTTP/1.1 200 OK
                     Content-Type: application/json

                     {
                         "foo": "bar"
                     }

        ''').lstrip()

    def test_group_examples(self):
        renderer = renderers.HttpdomainOldRenderer(None, {
            'examples': True,
            'group_examples': True
            }
        )
        text = '\n'.join(renderer.render_restructuredtext_markup({
            'openapi': '3.0.0',
            'paths': {
                '/problem': {
                    'post': {
                        'summary': 'Problem',
                        'description': '~ some useful description ~',
                        'requestBody': {
                            'content': {
                                'application/json':  {
                                    'example': {"foo": "bar"}
                                }
                            }
                        },
                        'responses': {
                            '200': {
                                'description': 'An array of resources.',
                                'content': {
                                    'application/json': {
                                        'example': {"foo": "bar"}
                                    }
                                }
                            },
                        },
                    },
                },
            },
        }))
        assert text == textwrap.dedent('''
            .. http:post:: /problem
               :synopsis: Problem

               **Problem**

               ~ some useful description ~

               :status 200:
                  An array of resources.

               **Example request:**

               .. sourcecode:: http

                  POST /problem HTTP/1.1
                  Host: example.com
                  Content-Type: application/json

                  {
                      "foo": "bar"
                  }


               **Example response:**

               .. sourcecode:: http

                  HTTP/1.1 200 OK
                  Content-Type: application/json

                  {
                      "foo": "bar"
                  }

        ''').lstrip()

    def test_groups(self):
        renderer = renderers.HttpdomainOldRenderer(None, {'group': True})
        text = '\n'.join(renderer.render_restructuredtext_markup({
            'openapi': '3.0.0',
            'tags': [
                {'name': 'tags'},
                {'name': 'pets'},
            ],
            'paths': collections.OrderedDict([
                ('/', {
                    'get': {
                        'summary': 'Index',
                        'description': '~ some useful description ~',
                        'deprecated': True,
                        'responses': {
                            '200': {
                                'description': 'Index',
                                'content': {
                                    'application/json': {
                                        'pets': 'https://example.com/api/pets',
                                        'tags': 'https://example.com/api/tags',
                                    }
                                }
                            },
                        },
                    },
                }),
                ('/pets', {
                    'get': {
                        'summary': 'List Pets',
                        'description': '~ some useful description ~',
                        'responses': {
                            '200': {
                                'description': 'Pets',
                                'content': {
                                    'application/json': [
                                        {
                                            'example': '{"foo": "bar"}'
                                        },
                                    ],
                                },
                            },
                        },
                        'tags': [
                            'pets',
                        ],
                    },
                }),
                ('/pets/{name}', {
                    'get': {
                        'summary': 'Show Pet',
                        'description': '~ some useful description ~',
                        'parameters': [
                            {
                                'name': 'name',
                                'in': 'path',
                                'schema': {'type': 'string'},
                                'description': 'Name of pet.',
                            },
                        ],
                        'responses': {
                            '200': {
                                'description': 'A Pet',
                                'content': {
                                    'application/json': {
                                        'example': '{"foo": "bar"}'
                                    }
                                }
                            },
                        },
                        'tags': [
                            'pets',
                        ],
                    },
                }),
                ('/tags', {
                    'get': {
                        'summary': 'List Tags',
                        'description': '~ some useful description ~',
                        'responses': {
                            '200': {
                                'description': 'Tags',
                                'content': {
                                    'application/json': [
                                        {
                                            'example': '{"foo": "bar"}'
                                        },
                                    ],
                                }
                            },
                        },
                        'tags': [
                            'tags',
                            'pets',
                        ],
                    },
                }),
            ]),
        }))
        assert text == textwrap.dedent('''
            tags
            ====

            .. http:get:: /tags
               :synopsis: List Tags

               **List Tags**

               ~ some useful description ~

               :status 200:
                  Tags.

            pets
            ====

            .. http:get:: /pets
               :synopsis: List Pets

               **List Pets**

               ~ some useful description ~

               :status 200:
                  Pets.

            .. http:get:: /pets/{name}
               :synopsis: Show Pet

               **Show Pet**

               ~ some useful description ~

               :param string name:
                  Name of pet.
               :status 200:
                  A Pet.

            default
            =======

            .. http:get:: /
               :synopsis: Index

               **Index**

               ~ some useful description ~

               **DEPRECATED**

               :status 200:
                  Index.
        ''').lstrip()

    def test_required_parameters(self):
        renderer = renderers.HttpdomainOldRenderer(None, {})
        text = '\n'.join(renderer.render_restructuredtext_markup({
            'openapi': '3.0.0',
            'paths': {
                '/resources/{kind}': {
                    'get': {
                        'summary': 'List Resources',
                        'description': '~ some useful description ~',
                        'parameters': [
                            {
                                'name': 'kind',
                                'in': 'path',
                                'schema': {'type': 'string'},
                                'description': 'Kind of resource to list.',
                            },
                            {
                                'name': 'limit',
                                'in': 'query',
                                'required': True,
                                'schema': {'type': 'integer'},
                                'description': 'Show up to `limit` entries.',
                            },
                            {
                                'name': 'If-None-Match',
                                'in': 'header',
                                'required': True,
                                'schema': {'type': 'string'},
                                'description': 'Last known resource ETag.'
                            },
                        ],
                        'requestBody': {
                            'content': {
                                'application/json':  {
                                    'example': '{"foo2": "bar2"}'
                                }
                            }
                        },
                        'responses': {
                            '200': {
                                'description': 'An array of resources.',
                                'content': {
                                    'application/json': {
                                        'example': '{"foo": "bar"}'
                                    }
                                }
                            },
                        },
                    },
                },
            },
        }))
        assert text == textwrap.dedent('''
            .. http:get:: /resources/{kind}
               :synopsis: List Resources

               **List Resources**

               ~ some useful description ~

               :param string kind:
                  Kind of resource to list.
               :query integer limit:
                  Show up to `limit` entries.
                  (Required)
               :reqheader If-None-Match:
                  Last known resource ETag.
                  (Required)
               :status 200:
                  An array of resources.
        ''').lstrip()

    def test_example_generation(self):
        renderer = renderers.HttpdomainOldRenderer(None, {'examples': True})
        text = '\n'.join(renderer.render_restructuredtext_markup({
            'openapi': '3.0.0',
            'paths': collections.OrderedDict([
                ('/resources/', collections.OrderedDict([
                    ('get', {
                        'summary': 'List Resources',
                        'description': '~ some useful description ~',
                        'parameters': [
                            {
                                'name': 'limit',
                                'in': 'query',
                                'required': True,
                                'schema': {'type': 'integer'},
                                'description': 'Show up to `limit` entries.',
                            },
                            {
                                'name': 'If-None-Match',
                                'in': 'header',
                                'schema': {'type': 'string'},
                                'description': 'Last known resource ETag.'
                            },
                        ],
                        'responses': {
                            '200': {
                                'description': 'An array of resources.',
                                'content': {
                                    'application/json': {
                                        'schema': {
                                            'type': 'array',
                                            'items': {
                                                '$ref': '#/components/schemas/Resource',  # noqa
                                            },
                                        },
                                    }
                                }
                            },
                        },
                    }),
                    ('post', {
                        'summary': 'Create Resource',
                        'description': '~ some useful description ~',
                        'parameters': [],
                        'requestBody': {
                            'content': {
                                'application/json':  {
                                    'schema': {
                                            'type': 'array',
                                            'items': {
                                                '$ref': '#/components/schemas/Resource',  # noqa
                                            },
                                    },
                                }
                            }
                        },
                        'responses': {
                            '200': {
                                'description': 'The created resource.',
                                'content': {
                                    'application/json': {
                                        'schema': {
                                            '$ref': '#/components/schemas/Resource',  # noqa
                                        },
                                    }
                                }
                            },
                        },
                    }),
                ])),
                ('/resources/{kind}', collections.OrderedDict([
                    ('get', {
                        'summary': 'Show Resource',
                        'description': '~ some useful description ~',
                        'parameters': [
                            {
                                'name': 'kind',
                                'in': 'path',
                                'schema': {'type': 'string'},
                                'description': 'Kind of resource to list.',
                                'example': 'KIND01'
                            },
                        ],
                        'responses': {
                            '200': {
                                'description': 'The created resource.',
                                'content': {
                                    'application/json': {
                                        'schema': {
                                            '$ref': '#/components/schemas/Resource',  # noqa
                                        },
                                    }
                                }
                            },
                        },
                    }),
                    ('patch', {
                        'summary': 'Update Resource (partial)',
                        'description': '~ some useful description ~',
                        'parameters': [
                            {
                                'name': 'kind',
                                'in': 'path',
                                'schema': {'type': 'string'},
                                'description': 'Kind of resource to list.',
                            },
                        ],
                        'requestBody': {
                            'content': {
                                'application/json':  {
                                    'schema': {
                                        '$ref': '#/components/schemas/Resource',  # noqa
                                    },
                                }
                            }
                        },
                        'responses': {
                            '200': {
                                'description': 'The created resource.',
                                'content': {
                                    'application/json': {
                                        'schema': {
                                            '$ref': '#/components/schemas/Resource',  # noqa
                                        },
                                    }
                                }
                            },
                        },
                    }),
                ])),
            ]),
            'components': {
                'schemas': {
                    'Resource': {
                        'type': 'object',
                        'properties': collections.OrderedDict([
                            ('kind', {
                                'title': 'Kind',
                                'type': 'string',
                                'readOnly': True,
                            }),
                            ('description', {
                                'title': 'Description',
                                'type': 'string',
                            }),
                            ('data', {
                                'title': 'Data',
                                'type': 'string',
                                'format': 'byte',
                            }),
                        ]),
                        'example': {
                            'kind': 'KIND01',
                            'description': 'DESC',
                            'data': 'ABCD',
                        }
                    },
                },
            },
        }))

        assert text == textwrap.dedent('''
            .. http:get:: /resources/
               :synopsis: List Resources

               **List Resources**

               ~ some useful description ~

               :query integer limit:
                  Show up to `limit` entries.
                  (Required)
               :reqheader If-None-Match:
                  Last known resource ETag.

               **Example request:**

               .. sourcecode:: http

                  GET /resources/?limit=1 HTTP/1.1
                  Host: example.com

               :status 200:
                  An array of resources.

                  **Example response:**

                  .. sourcecode:: http

                     HTTP/1.1 200 OK
                     Content-Type: application/json

                     [
                         {
                             "kind": "KIND01",
                             "description": "DESC",
                             "data": "ABCD"
                         }
                     ]


            .. http:post:: /resources/
               :synopsis: Create Resource

               **Create Resource**

               ~ some useful description ~


               **Example request:**

               .. sourcecode:: http

                  POST /resources/ HTTP/1.1
                  Host: example.com
                  Content-Type: application/json

                  [
                      {
                          "description": "DESC",
                          "data": "ABCD"
                      }
                  ]

               :status 200:
                  The created resource.

                  **Example response:**

                  .. sourcecode:: http

                     HTTP/1.1 200 OK
                     Content-Type: application/json

                     {
                         "kind": "KIND01",
                         "description": "DESC",
                         "data": "ABCD"
                     }


            .. http:get:: /resources/{kind}
               :synopsis: Show Resource

               **Show Resource**

               ~ some useful description ~

               :param string kind:
                  Kind of resource to list.

               **Example request:**

               .. sourcecode:: http

                  GET /resources/KIND01 HTTP/1.1
                  Host: example.com

               :status 200:
                  The created resource.

                  **Example response:**

                  .. sourcecode:: http

                     HTTP/1.1 200 OK
                     Content-Type: application/json

                     {
                         "kind": "KIND01",
                         "description": "DESC",
                         "data": "ABCD"
                     }


            .. http:patch:: /resources/{kind}
               :synopsis: Update Resource (partial)

               **Update Resource (partial)**

               ~ some useful description ~

               :param string kind:
                  Kind of resource to list.

               **Example request:**

               .. sourcecode:: http

                  PATCH /resources/string HTTP/1.1
                  Host: example.com
                  Content-Type: application/json

                  {
                      "description": "DESC",
                      "data": "ABCD"
                  }

               :status 200:
                  The created resource.

                  **Example response:**

                  .. sourcecode:: http

                     HTTP/1.1 200 OK
                     Content-Type: application/json

                     {
                         "kind": "KIND01",
                         "description": "DESC",
                         "data": "ABCD"
                     }

        ''').lstrip()

    def test_get_example_with_explode(self):
        renderer = renderers.HttpdomainOldRenderer(None, {'examples': True})
        text = '\n'.join(renderer.render_restructuredtext_markup({
            'openapi': '3.0.0',
            'paths': collections.OrderedDict([
                ('/resources/', collections.OrderedDict([
                    ('get', {
                        'summary': 'List Resources',
                        'description': '~ some useful description ~',
                        'parameters': [
                            {
                                'name': 'params',
                                'in': 'query',
                                'required': True,
                                'schema': {
                                    'type': 'array',
                                    'items': {
                                        'type': 'string'
                                    }
                                },
                                'style': 'form',
                                'explode': True,
                                'example': [
                                    'p1',
                                    'p2',
                                ],
                                'description': 'List with explode set to True'
                            },
                            {
                                'name': 'values',
                                'in': 'query',
                                'required': True,
                                'schema': {
                                    'type': 'object',
                                    'additionalProperties': True
                                },
                                'style': 'form',
                                'explode': True,
                                'example': collections.OrderedDict([
                                    ('v1', 'V1'),
                                    ('v2', 'V2'),
                                ]),
                                'description': 'Dict with explode set to True'
                            },
                        ],
                        'responses': {
                            '200': {
                                'description': 'OK'
                            },
                        },
                    }),
                ])),
            ]),
        }))

        assert text == textwrap.dedent('''
            .. http:get:: /resources/
               :synopsis: List Resources

               **List Resources**

               ~ some useful description ~

               :query array params:
                  List with explode set to True.
                  (Required)
               :query object values:
                  Dict with explode set to True.
                  (Required)

               **Example request:**

               .. sourcecode:: http

                  GET /resources/?params=p1&params=p2&v1=V1&v2=V2 HTTP/1.1
                  Host: example.com

               :status 200:
                  OK.
        ''').lstrip()

    def test_callback(self):
        renderer = renderers.HttpdomainOldRenderer(None, {})
        text = '\n'.join(renderer.render_restructuredtext_markup({
            'openapi': '3.0.0',
            'paths': {
                '/resources/{kind}': {
                    'post': {
                        'summary': 'List Resources',
                        'description': '~ some useful description ~',
                        'parameters': [
                            {
                                'name': 'kind',
                                'in': 'path',
                                'schema': {'type': 'string'},
                                'description': 'Kind of resource to list.',
                            },
                            {
                                'name': 'callback',
                                'in': 'query',
                                'description': 'the callback address',
                                'required': False,
                                'schema': {
                                    'type': 'string',
                                    'format': 'uri'
                                },
                                'example': 'http://client.com/callback'
                            }
                        ],
                        'requestBody': {
                            'content': {
                                'application/json':  {
                                    'example': '{"foo2": "bar2"}'
                                }
                            }
                        },
                        'responses': {
                            '202': {
                                'description': 'Something',
                                'content': {
                                    'application/json': {
                                        'example': '{"foo": "bar"}'
                                    }
                                }
                            },
                        },
                        'callbacks': {
                            'callback': {
                                '${request.query.callback}': {
                                    'post': {
                                        'summary': 'Response callback',
                                        'operationId': 'sampleCB',
                                        'requestBody': {
                                            'required': True,
                                            'description': 'Result',
                                            'content': {
                                                'application/json': {
                                                    'schema': {
                                                        'type': 'object',
                                                        'required': ['status'],
                                                        'properties': {
                                                            'status': {
                                                                'type':
                                                                    'string',
                                                                'enum': [
                                                                    'OK',
                                                                    'ERROR'
                                                                ]
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        },
                                        'responses': {
                                            '200': {
                                                'description': 'Success'
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    },
                },
            },
        }))
        assert text == textwrap.dedent('''
            .. http:post:: /resources/{kind}
               :synopsis: List Resources

               **List Resources**

               ~ some useful description ~

               :param string kind:
                  Kind of resource to list.
               :query string callback:
                  the callback address.
               :status 202:
                  Something.

               .. admonition:: Callback: callback

                  .. http:post:: ${request.query.callback}
                     :synopsis: Response callback

                     **Response callback**

                     :jsonparam string status:
                     :status 200:
                        Success.

        ''').lstrip()

    def test_string_example(self):
        renderer = renderers.HttpdomainOldRenderer(None, {'examples': True})
        text = '\n'.join(renderer.render_restructuredtext_markup({
            'openapi': '3.0.0',
            'paths': {
                '/resources': {
                    'get': {
                        'summary': 'Get resources',
                        'responses': {
                            '200': {
                                'description': 'Something',
                                'content': {
                                    'application/json': {
                                        'schema': {
                                            'type': 'string',
                                            'example': '"A sample"',
                                        }
                                    }
                                }
                            },
                        },
                    },
                },
            },
        }))

        assert text == textwrap.dedent('''
            .. http:get:: /resources
               :synopsis: Get resources

               **Get resources**


               **Example request:**

               .. sourcecode:: http

                  GET /resources HTTP/1.1
                  Host: example.com

               :status 200:
                  Something.

                  **Example response:**

                  .. sourcecode:: http

                     HTTP/1.1 200 OK
                     Content-Type: application/json

                     "A sample"

        ''').lstrip()

    def test_ref_example(self):
        renderer = renderers.HttpdomainOldRenderer(None, {'examples': True})
        text = '\n'.join(renderer.render_restructuredtext_markup({
            'openapi': '3.0.0',
            'paths': {
                '/resources': {
                    'get': {
                        'summary': 'Get resources',
                        'responses': {
                            '200': {
                                'description': 'Something',
                                'content': {
                                    'application/json': {
                                        'schema': {
                                            '$ref':
                                                '#/components/schemas/Data',
                                        }
                                    }
                                }
                            },
                        },
                    },
                },
            },
            'components': {
                'schemas': {
                    'Data': {
                        'type': 'object',
                        'additionalProperties': True,
                        'example': {
                            'prop1': "Sample 1",
                        }
                    }
                }
            }
        }))

        assert text == textwrap.dedent('''
            .. http:get:: /resources
               :synopsis: Get resources

               **Get resources**


               **Example request:**

               .. sourcecode:: http

                  GET /resources HTTP/1.1
                  Host: example.com

               :status 200:
                  Something.

                  **Example response:**

                  .. sourcecode:: http

                     HTTP/1.1 200 OK
                     Content-Type: application/json

                     {
                         "prop1": "Sample 1",
                         "...": "..."
                     }

        ''').lstrip()

    def test_method_option(self):
        spec = collections.defaultdict(collections.OrderedDict)
        spec['paths']['/resource_a'] = {
            'get': {
                'description': 'resource a',
                'responses': {
                    '200': {'description': 'ok'},
                }
            },
            'post': {
                'description': 'resource a',
                'responses': {
                    '201': {'description': 'ok'},
                }
            },
            'put': {
                'description': 'resource a',
                'responses': {
                    '404': {'description': 'error'},
                }
            }
        }

        renderer = renderers.HttpdomainOldRenderer(
            None,
            {
                'methods': ['post'],
                'paths': ['/resource_a'],
            },
        )
        text = '\n'.join(renderer.render_restructuredtext_markup(spec))

        assert text == textwrap.dedent('''
            .. http:post:: /resource_a
               :synopsis: null

               resource a

               :status 201:
                  ok
        ''').lstrip()

    def test_simpletype_example(self):
        spec = yaml.safe_load(textwrap.dedent("""
        ---
        openapi: 3.0.0
        paths:
          /resources:
            post:
              summary: Summary
              description: test service
              requestBody:
                description: present
                content:
                  application/json:
                    schema:
                      $ref: '#/components/schemas/MyRequest'
              responses:
                200:
                  description: Success
                  content:
                    application/json:
                      schema:
                        $ref: '#/components/schemas/MyRequest'
        components:
          schemas:
            MyRequest:
              description: absent
              type: object
              properties:
                a:
                  $ref: '#/components/schemas/MySimpleType'
                b:
                  type: string
                  example: B
            MySimpleType:
              type: string
              enum: [A, B, C]
              example: C
        """))

        renderer = renderers.HttpdomainOldRenderer(
            None,
            {
                'examples': True,
                'group_examples': True,
                'entities': True
            }
        )
        text = '\n'.join(renderer.render_restructuredtext_markup(spec))
        assert text == textwrap.dedent('''
            .. http:post:: /resources
               :synopsis: Summary

               **Summary**

               test service

               :form body: present.
                  Object of type :ref:`MyRequest </components/schemas/MyRequest>`.
               :status 200:
                  Success.
                  Object of type :ref:`MyRequest </components/schemas/MyRequest>`.

               **Example request:**

               .. sourcecode:: http

                  POST /resources HTTP/1.1
                  Host: example.com
                  Content-Type: application/json

                  {
                      "a": "C",
                      "b": "B"
                  }


               **Example response:**

               .. sourcecode:: http

                  HTTP/1.1 200 OK
                  Content-Type: application/json

                  {
                      "a": "C",
                      "b": "B"
                  }

        ''').lstrip()

    def test_header_example(self):
        renderer = renderers.HttpdomainOldRenderer(None, {'examples': True, "contextpath": True})
        spec = yaml.safe_load(textwrap.dedent("""
        ---
        openapi: 3.0.0
        paths:
          /resources:
            post:
              summary: Summary
              description: test service
              parameters:
                - name: HeaderRequest
                  in: header
                  description: request header
                  schema:
                    type: string
                    maxLength: 32
                  example: "MD5=thvDyvhfIqlvFe+A9MYgxAfm1q5="
              requestBody:
                content:
                  application/json:
                    schema:
                      type: string
                    example: REQUEST
                    required: true
              responses:
                200:
                  description: Success
                  content:
                    application/json:
                      schema:
                        type: string
                      example: RESPONSE
                  headers:
                    HeaderResponse:
                      description: response header
                      schema:
                        type: string
                      example: "MD5=thvDyvhfIqlvFe+A9MYgxAfm1q5="
                400:
                  description: Error
                  content:
                    application/json:
                      schema:
                        type: string
                      example: ERROR
        """))

        text = '\n'.join(renderer.render_restructuredtext_markup(spec))
        assert text == textwrap.dedent('''
            .. http:post:: /resources
               :synopsis: Summary

               **Summary**

               test service

               :reqheader HeaderRequest:
                  request header.
                  Constraints: maxLength is 32.

               **Example request:**

               .. sourcecode:: http

                  POST /resources HTTP/1.1
                  Host: example.com
                  Content-Type: application/json
                  HeaderRequest: MD5=thvDyvhfIqlvFe+A9MYgxAfm1q5=

                  REQUEST

               :resheader HeaderResponse:
                  response header.
               :status 200:
                  Success.

                  **Example response:**

                  .. sourcecode:: http

                     HTTP/1.1 200 OK
                     Content-Type: application/json
                     HeaderResponse: MD5=thvDyvhfIqlvFe+A9MYgxAfm1q5=

                     RESPONSE

               :status 400:
                  Error.

                  **Example response:**

                  .. sourcecode:: http

                     HTTP/1.1 400 Bad Request
                     Content-Type: application/json

                     ERROR

        ''').lstrip()

        renderer = renderers.HttpdomainOldRenderer(
            None,
            {
                'examples': True,
                'group_examples': True
            }
        )
        text = '\n'.join(renderer.render_restructuredtext_markup(spec))
        assert text == textwrap.dedent('''
            .. http:post:: /resources
               :synopsis: Summary

               **Summary**

               test service

               :reqheader HeaderRequest:
                  request header.
                  Constraints: maxLength is 32.
               :resheader HeaderResponse:
                  response header.
               :status 200:
                  Success.
               :status 400:
                  Error.

               **Example request:**

               .. sourcecode:: http

                  POST /resources HTTP/1.1
                  Host: example.com
                  Content-Type: application/json
                  HeaderRequest: MD5=thvDyvhfIqlvFe+A9MYgxAfm1q5=

                  REQUEST


               **Example response:**

               .. sourcecode:: http

                  HTTP/1.1 200 OK
                  Content-Type: application/json
                  HeaderResponse: MD5=thvDyvhfIqlvFe+A9MYgxAfm1q5=

                  RESPONSE


               **Example response:**

               .. sourcecode:: http

                  HTTP/1.1 400 Bad Request
                  Content-Type: application/json

                  ERROR

        ''').lstrip()

    def test_entities(self):
        renderer = renderers.HttpdomainOldRenderer(None, {'entities': True})
        spec = yaml.safe_load(textwrap.dedent("""
        ---
        openapi: 3.0.0
        servers:
        - url: https://test.org/context
        paths:
          /resources:
            post:
              summary: Summary
              description: test service
              requestBody:
                content:
                  application/json:
                    schema:
                      type: string
                    example: REQUEST
                    required: true
              responses:
                200:
                  description: Success
                  content:
                    application/json:
                      schema:
                        type: string
                      example: RESPONSE
          /resources2:
            post:
              summary: Summary
              description: test service
              requestBody:
                description: Body
                content:
                  application/json:
                    schema:
                      $ref: '#/components/schemas/Test1'
              responses:
                200:
                  description: Success
                  content:
                    application/json:
                      schema:
                        $ref: '#/components/schemas/Test1'
          /resources3:
            post:
              summary: Summary
              description: test service
              requestBody:
                content:
                  application/json:
                    schema:
                      type: array
                      items:
                        $ref: '#/components/schemas/Test1'
              responses:
                200:
                  description: Success
                  content:
                    application/json:
                      schema:
                        type: array
                        items:
                          $ref: '#/components/schemas/Test1'
        components:
          schemas:
            Test1:
              type: object
              properties:
                field1:
                  type: integer
                  format: int32
                  description: Signed 32 bits
        """))

        text = '\n'.join(renderer.render_restructuredtext_markup(spec))
        assert text == textwrap.dedent('''
          .. http:post:: /resources
             :synopsis: Summary

             **Summary**

             test service

             :status 200:
                Success.
                Object of type string.

          .. http:post:: /resources2
             :synopsis: Summary

             **Summary**

             test service

             :form body: Body.
                Object of type :ref:`Test1 </components/schemas/Test1>`.
             :status 200:
                Success.
                Object of type :ref:`Test1 </components/schemas/Test1>`.

          .. http:post:: /resources3
             :synopsis: Summary

             **Summary**

             test service

             :form body: Array of :ref:`Test1 </components/schemas/Test1>`.
             :status 200:
                Success.
                Array of :ref:`Test1 </components/schemas/Test1>`.
        ''').lstrip()

        renderer = renderers.HttpdomainOldRenderer(None, {})
        text = '\n'.join(renderer.render_restructuredtext_markup(spec))
        assert text == textwrap.dedent('''
          .. http:post:: /resources
             :synopsis: Summary

             **Summary**

             test service

             :status 200:
                Success.

          .. http:post:: /resources2
             :synopsis: Summary

             **Summary**

             test service

             :form body: Body.
             :status 200:
                Success.

          .. http:post:: /resources3
             :synopsis: Summary

             **Summary**

             test service

             :status 200:
                Success.
        ''').lstrip()

    def test_entity_no_type(self):
        renderer = renderers.HttpdomainOldRenderer(None, {'examples': True})
        spec = yaml.safe_load(textwrap.dedent("""
        ---
        openapi: 3.0.0
        servers:
        - url: https://test.org/context
        paths:
          /resources:
            post:
              summary: Summary
              description: test service
              requestBody:
                description: Body
                content:
                  application/json:
                    schema:
                      $ref: '#/components/schemas/Test1'
              responses:
                200:
                  description: Success
                  content:
                    application/json:
                      schema:
                        $ref: '#/components/schemas/Test2'
        components:
          schemas:
            Test1:
              description: any type1
              example:
                field1: 12
            Test2:
              description: any type2
        """))

        text = '\n'.join(renderer.render_restructuredtext_markup(spec))
        assert text == textwrap.dedent('''
          .. http:post:: /resources
             :synopsis: Summary

             **Summary**

             test service

             :form body: Body.
                any type1.

             **Example request:**

             .. sourcecode:: http

                POST /resources HTTP/1.1
                Host: example.com
                Content-Type: application/json

                {
                    "field1": 12
                }

             :status 200:
                Success.

                **Example response:**

                .. sourcecode:: http

                   HTTP/1.1 200 OK
                   Content-Type: application/json

                   {
                       "...": "..."
                   }

        ''').lstrip()

    def test_adv_parameters(self):
        renderer = renderers.HttpdomainOldRenderer(None, {'entities': True})
        spec = yaml.safe_load(textwrap.dedent("""
        ---
        openapi: 3.0.0
        paths:
          /resources/{param0}:
            get:
              summary: Summary
              description: test service
              parameters:
                - name: param0
                  in: path
                  description: query param
                  schema:
                    type: string
                    maxLength: 10
                - name: param1
                  in: query
                  description: first param
                  required: true
                  schema:
                    type: string
                    maxLength: 64
                - name: param2
                  in: header
                  description: second param
                  schema:
                    type: string
                    maxLength: 32
                - name: param3
                  in: query
                  description: third param
                  schema:
                    type: array
                    items:
                      type: string
                      maxLength: 64
                    minItems: 1
              responses:
                200:
                  description: Success
                  content:
                    application/json:
                      schema:
                        type: string
                      example: RESPONSE
        """))

        text = '\n'.join(renderer.render_restructuredtext_markup(spec))
        assert text == textwrap.dedent('''
          .. http:get:: /resources/{param0}
             :synopsis: Summary

             **Summary**

             test service

             :param string param0:
                query param.
                Object of type string.
                Constraints: maxLength is 10.
             :query string param1:
                first param.
                Object of type string.
                Constraints: maxLength is 64.
                (Required)
             :query array param3:
                third param.
                Array of string.
                Constraints: maxLength is 64; minItems is 1.
             :reqheader param2:
                second param.
                Object of type string.
                Constraints: maxLength is 32.
             :status 200:
                Success.
                Object of type string.
        ''').lstrip()

    def test_contextpath(self):
        spec = yaml.safe_load(textwrap.dedent("""
        ---
        openapi: 3.0.0
        servers:
        - url: https://test.org/context
        paths:
          /resources:
            get:
              summary: Summary
              responses:
                200:
                  description: Success
                  content:
                    application/json:
                      schema:
                        type: string
                      example: RESPONSE
        """))

        renderer = renderers.HttpdomainOldRenderer(None, {'contextpath': True, 'examples': True})
        text = '\n'.join(renderer.render_restructuredtext_markup(spec))
        assert text == textwrap.dedent('''
          .. http:get:: /context/resources
             :synopsis: Summary

             **Summary**


             **Example request:**

             .. sourcecode:: http

                GET /context/resources HTTP/1.1
                Host: example.com

             :status 200:
                Success.

                **Example response:**

                .. sourcecode:: http

                   HTTP/1.1 200 OK
                   Content-Type: application/json

                   RESPONSE

                 ''').lstrip()

        renderer = renderers.HttpdomainOldRenderer(None, {
                'contextpath': True,
                'examples': True,
                'group': True
            })
        text = '\n'.join(renderer.render_restructuredtext_markup(spec))
        assert text == textwrap.dedent('''
          default
          =======

          .. http:get:: /context/resources
             :synopsis: Summary

             **Summary**


             **Example request:**

             .. sourcecode:: http

                GET /context/resources HTTP/1.1
                Host: example.com

             :status 200:
                Success.

                **Example response:**

                .. sourcecode:: http

                   HTTP/1.1 200 OK
                   Content-Type: application/json

                   RESPONSE

                 ''').lstrip()

    def test_bool_param_in_query(self):
        renderer = renderers.HttpdomainOldRenderer(None, {'examples': True})
        spec = yaml.safe_load(textwrap.dedent("""
        ---
        openapi: 3.0.0
        paths:
          /resources:
            get:
              summary: Summary
              description: test service
              parameters:
                - name: myparam
                  in: query
                  description: test param
                  schema:
                    type: boolean
                    default: false
              responses:
                200:
                  description: Success
        """))

        text = '\n'.join(renderer.render_restructuredtext_markup(spec))
        assert text == textwrap.dedent('''
            .. http:get:: /resources
               :synopsis: Summary

               **Summary**

               test service

               :query boolean myparam:
                  test param.
                  Default: ``false``.

               **Example request:**

               .. sourcecode:: http

                  GET /resources?myparam=false HTTP/1.1
                  Host: example.com

               :status 200:
                  Success.
        ''').lstrip()

    def test_markdown(self):
        renderer = renderers.HttpdomainOldRenderer(None, {'format': 'markdown', 'examples': True})
        spec = yaml.safe_load(textwrap.dedent("""
        ---
        openapi: 3.0.0
        paths:
          /resources/{opt}:
            post:
              summary: Summary
              description: test service in __bold__
              parameters:
                - name: opt
                  in: path
                  description: test param in _italic_
                  schema:
                    type: string
                - name: myparam
                  in: query
                  description: test param in _italic_
                  schema:
                    type: boolean
                    default: false
                - name: myheader
                  in: header
                  description: test param in _italic_
                  schema:
                    type: boolean
                    default: false
              responses:
                200:
                  description: Success
        """))
        text = '\n'.join(renderer.render_restructuredtext_markup(spec))
        assert text == textwrap.dedent('''
            .. http:post:: /resources/{opt}
               :synopsis: Summary

               **Summary**

               test service in **bold**

               :param string opt:
                  test param in *italic*.
               :query boolean myparam:
                  test param in *italic*.
                  Default: ``false``.
               :reqheader myheader:
                  test param in *italic*.
                  Default: ``false``.
               :status 200:
                  Success.
        ''').lstrip()


class TestResolveRefs(object):

    def test_ref_resolving(self):
        data = {
            'foo': {
                'a': 13,
                'b': {
                    'c': True,
                }
            },
            'bar': {
                '$ref': '#/foo/b'
            },
            'baz': [
                {'$ref': '#/foo/a'},
                {'$ref': '#/foo/b'},
                'batman',
            ]
        }

        assert utils._resolve_refs('', data) == {
            'foo': {
                'a': 13,
                'b': {
                    '$entity_ref': '#/foo/b',
                    'c': True,
                }
            },
            'bar': {
                '$entity_ref': '#/foo/b',
                'c': True,
            },
            'baz': [
                13,
                {
                    '$entity_ref': '#/foo/b',
                    'c': True
                },
                'batman',
            ]
        }

    def test_relative_ref_resolving_on_fs(self):
        baseuri = 'file:///%s' % os.path.abspath(__file__).replace('\\', '/')

        data = {
            'bar': {
                '$ref': 'testdata/foo.json#/foo/b',
            },
            # check also JSON to YAML references:
            'baz': {
                '$ref': 'testdata/foo.yaml#/foo',
            }
        }

        # import pdb
        # pdb.set_trace()
        assert utils._resolve_refs(baseuri, data) == {
            'bar': {
                '$entity_ref': 'testdata/foo.json#/foo/b',
                'c': True,
            },
            'baz': {
                '$entity_ref': 'testdata/foo.yaml#/foo',
                'a': 17,
                'b': 13,
            },
        }

    def test_noproperties(self):
        renderer = renderers.HttpdomainOldRenderer(None, {'examples': True})
        text = '\n'.join(renderer.render_restructuredtext_markup({
            'openapi': '3.0.0',
            'paths': {
                '/resources': {
                    'post': {
                        'summary': 'Create Resources',
                        'description': '~ some useful description ~',
                        'requestBody': {
                            'content': {
                                'application/json':  {
                                    'schema': {
                                        '$ref': '#/components/schemas/Resource',  # noqa
                                    }
                                }
                            }
                        },
                        'responses': {
                            '200': {
                                'description': 'Something',
                            },
                        },
                    },
                },
            },
            'components': {
                'schemas': {
                    'Resource': {
                        'type': 'object',
                        'additionalProperties': True,
                    },
                },
            },

        }))
        assert text == textwrap.dedent('''
            .. http:post:: /resources
               :synopsis: Create Resources

               **Create Resources**

               ~ some useful description ~


               **Example request:**

               .. sourcecode:: http

                  POST /resources HTTP/1.1
                  Host: example.com
                  Content-Type: application/json

                  {
                      "...": "..."
                  }

               :status 200:
                  Something.
        ''').lstrip()


def test_openapi2_examples(tmpdir, run_sphinx):
    spec = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        'OpenAPI-Specification',
        'examples',
        'v2.0',
        'json',
        'uber.json')
    py.path.local(spec).copy(tmpdir.join('src', 'test-spec.yml'))

    with pytest.raises(ValueError) as excinfo:
        run_sphinx('test-spec.yml', options={'examples': True})

    assert str(excinfo.value) == (
        'Rendering examples is not supported for OpenAPI v2.x specs.')


@pytest.mark.parametrize('render_examples', [False, True])
def test_openapi3_examples(tmpdir, run_sphinx, render_examples):
    spec = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        'OpenAPI-Specification',
        'examples',
        'v3.0',
        'petstore.yaml')
    py.path.local(spec).copy(tmpdir.join('src', 'test-spec.yml'))
    run_sphinx('test-spec.yml', options={'examples': render_examples})

    rendered_html = tmpdir.join('out', 'index.html').read_text('utf-8')

    assert ('<strong>Example response:</strong>' in rendered_html) \
        == render_examples


class TestConvertJsonSchema(object):
    schema = {
        'type': 'object',
        'required': ['name', 'surprise'],
        'properties': {
            'name': {
                'type': 'string',
                'description': 'The name of user'},
            'alias': {
                'type': 'array',
                'items': {
                    'type': 'string'},
                'description': 'The list of user alias'},
            'id': {
                'type': 'integer',
                'description': 'the id of user',
                'readOnly': True},
            'surprise': {
                'type': 'string'},
            'secret': {
                'type': 'string',
                'readOnly': True}}}

    result = list(openapi20.convert_json_schema(schema))

    def test_required_field_with_description(self):
        assert ':<json string name: The name of user (required)' in self.result

    def test_required_field_without_description(self):
        assert ':<json string surprise: (required)' in self.result

    def test_array_field(self):
        assert ':<json string alias[]:' in self.result

    def test_read_only_field_with_description(self):
        assert ':<json integer id: the id of user (read only)' in self.result

    def test_read_only_field_without_description(self):
        assert ':<json string secret: (read only)' in self.result

    def test_nested_schema(self):
        schema = {
            'type': 'object',
            'required': ['name'],
            'properties': {
                'name': {
                    'type': 'string',
                    'description': 'The name of user'
                },
                'friends': {
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'properties': {
                            'name': {
                                'type': 'string',
                                'readOnly': True
                            },
                            'age': {'type': 'integer'}
                        }
                    },
                    'description': 'The list of user alias'
                },
                'id': {
                    'type': 'integer',
                    'description': 'the id of user',
                    'readOnly': True
                },
                'car': {
                    'type': 'object',
                    'properties': {
                        'provider': {'type': 'string'},
                        'date': {
                            'type': 'string',
                            'description': 'The car of user'
                        }
                    }
                },
                'meta': {
                    'type': 'object',
                    'description': 'free form metadata',
                },
            }
        }

        result = '\n'.join(openapi20.convert_json_schema(schema))

        expected = textwrap.dedent('''
            :<json string car.date: The car of user
            :<json string car.provider:
            :<json integer friends[].age:
            :<json string friends[].name: (read only)
            :<json integer id: the id of user (read only)
            :<json object meta: free form metadata
            :<json string name: The name of user (required)'''.strip('\n'))

        assert result == expected
