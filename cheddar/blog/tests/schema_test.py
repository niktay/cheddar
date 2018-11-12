from collections import OrderedDict

import pytest
from blog.models import Post
from django.test import TestCase
from freezegun import freeze_time
from graphene.test import Client
from mixer.backend.django import mixer

from cheddar.schema import schema


@pytest.mark.django_db
class SchemaTest(TestCase):
    @classmethod
    @freeze_time('2012-12-12')
    def setUpClass(cls):
        super(SchemaTest, cls).setUpClass()
        cls.client = Client(schema)
        mixer.blend(Post, title='Title01', content='Content01')
        mixer.blend(Post, title='Title02', content='Content02')
        mixer.blend(Post, title='Title03', content='Content03')

    @classmethod
    def test_all_posts_returns_posts(cls):
        query = '''
            query {
                allPosts {
                    id
                    title
                    content
                    createdAt
                }
            }
        '''
        expected_result = {
            'data':
            OrderedDict([(
                'allPosts', [
                    OrderedDict([
                        ('id', '1'), ('title', 'Title01'),
                        ('content', 'Content01'),
                        ('createdAt', '2012-12-12T00:00:00+00:00'),
                    ]),
                    OrderedDict([
                        ('id', '2'), ('title', 'Title02'),
                        ('content', 'Content02'),
                        ('createdAt', '2012-12-12T00:00:00+00:00'),
                    ]),
                    OrderedDict([
                        ('id', '3'), ('title', 'Title03'),
                        ('content', 'Content03'),
                        ('createdAt', '2012-12-12T00:00:00+00:00'),
                    ]),
                ],
            )]),
        }

        executed = cls.client.execute(query)
        assert executed == expected_result
