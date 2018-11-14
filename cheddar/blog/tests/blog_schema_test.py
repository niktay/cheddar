from collections import OrderedDict

import pytest
from blog.models import Post
from django.test import TestCase
from freezegun import freeze_time
from graphene.test import Client
from mixer.backend.django import mixer

from cheddar.schema import schema


@pytest.mark.django_db
class BlogSchemaTest(TestCase):
    @classmethod
    @freeze_time('2012-12-12')
    def setUpClass(cls):
        super(BlogSchemaTest, cls).setUpClass()
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
                'allPosts',
                [
                    OrderedDict([
                        ('id', '1'),
                        ('title', 'Title01'),
                        ('content', 'Content01'),
                        ('createdAt', '2012-12-12T00:00:00+00:00'),
                    ]),
                    OrderedDict([
                        ('id', '2'),
                        ('title', 'Title02'),
                        ('content', 'Content02'),
                        ('createdAt', '2012-12-12T00:00:00+00:00'),
                    ]),
                    OrderedDict([
                        ('id', '3'),
                        ('title', 'Title03'),
                        ('content', 'Content03'),
                        ('createdAt', '2012-12-12T00:00:00+00:00'),
                    ]),
                ],
            )]),
        }

        executed = cls.client.execute(query)
        assert executed == expected_result

    @classmethod
    @freeze_time('2012-12-12')
    def test_create_post_returns_post(cls):
        mutation = '''
            mutation createPost($input: CreatePostInput!) {
                createPost(newPost: $input) {
                    post {
                        id
                        title
                        content
                        createdAt
                    }
                }
            }
        '''
        new_post = {
            'input': {
                'title': 'Title04',
                'content': 'Content04',
            },
        }
        expected_result = {
            'data':
            OrderedDict([(
                'createPost',
                OrderedDict(
                    [(
                        'post',
                        OrderedDict(
                            [
                                ('id', '4'), ('title', 'Title04'),
                                ('content', 'Content04'),
                                (
                                    'createdAt',
                                    '2012-12-12T00:00:00+00:00',
                                ),
                            ],
                        ),
                    )],
                ),
            )]),
        }

        executed = cls.client.execute(mutation, variables=new_post)
        assert executed == expected_result

    @classmethod
    def test_delete_post_returns_post(cls):
        mutation = '''
            mutation {
                deletePost(deleteId: 1) {
                    post {
                        id
                        title
                        content
                        createdAt
                    }
                }
            }
        '''
        expected_result = {
            'data':
            OrderedDict([(
                'deletePost',
                OrderedDict(
                    [(
                        'post',
                        OrderedDict(
                            [
                                ('id', '1'), ('title', 'Title01'),
                                ('content', 'Content01'),
                                (
                                    'createdAt',
                                    '2012-12-12T00:00:00+00:00',
                                ),
                            ],
                        ),
                    )],
                ),
            )]),
        }

        executed = cls.client.execute(mutation)
        assert executed == expected_result

    @classmethod
    @freeze_time('2012-12-12')
    def test_update_post_returns_post(cls):
        mutation = '''
            mutation updatePost($input: UpdatePostInput!) {
                updatePost(changes: $input) {
                    post {
                        id
                        title
                        content
                        createdAt
                    }
                }
            }
        '''
        changes = {
            'input': {
                'id': 1,
                'title': 'updatedTitle',
            },
        }
        expected_result = {
            'data':
            OrderedDict([(
                'updatePost',
                OrderedDict(
                    [(
                        'post',
                        OrderedDict(
                            [
                                ('id', '1'), ('title', 'updatedTitle'),
                                ('content', 'Content01'),
                                (
                                    'createdAt',
                                    '2012-12-12T00:00:00+00:00',
                                ),
                            ],
                        ),
                    )],
                ),
            )]),
        }

        executed = cls.client.execute(mutation, variables=changes)
        print(executed)
        assert executed == expected_result
