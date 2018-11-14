from collections import OrderedDict

import pytest
from django.contrib.auth import get_user_model
from django.test import TestCase
from freezegun import freeze_time
from graphene.test import Client
from mixer.backend.django import mixer

from cheddar.schema import schema


@pytest.mark.django_db
class UserSchemaTest(TestCase):
    @classmethod
    @freeze_time('2012-12-12')
    def setUpClass(cls):
        super(UserSchemaTest, cls).setUpClass()
        cls.client = Client(schema)
        user_one = mixer.blend(
            get_user_model(),
            username='user01',
            first_name='User',
            last_name='One',
            email='user01@gmail.com',
        )
        user_one.set_password('user01password')

        user_two = mixer.blend(
            get_user_model(),
            username='user02',
            first_name='User',
            last_name='Two',
            email='user02@gmail.com',
        )
        user_two.set_password('user02password')

        user_three = mixer.blend(
            get_user_model(),
            username='user03',
            first_name='User',
            last_name='Three',
            email='user03@gmail.com',
        )
        user_three.set_password('user03password')

    @classmethod
    def test_all_users_returns_users(cls):
        query = '''
            query {
                allUsers {
                    id
                    username
                    firstName
                    lastName
                    email
                }
            }
        '''
        expected_result = {
            'data':
            OrderedDict([(
                'allUsers',
                [
                    OrderedDict([
                        ('id', '1'),
                        ('username', 'user01'),
                        (
                            'firstName',
                            'User',
                        ),
                        ('lastName', 'One'),
                        ('email', 'user01@gmail.com'),
                    ]),
                    OrderedDict([
                        ('id', '2'),
                        ('username', 'user02'),
                        (
                            'firstName',
                            'User',
                        ),
                        ('lastName', 'Two'),
                        ('email', 'user02@gmail.com'),
                    ]),
                    OrderedDict([
                        ('id', '3'),
                        ('username', 'user03'),
                        (
                            'firstName',
                            'User',
                        ),
                        ('lastName', 'Three'),
                        ('email', 'user03@gmail.com'),
                    ]),
                ],
            )]),
        }

        executed = cls.client.execute(query)
        assert executed == expected_result

    @classmethod
    def test_create_user_returns_user(cls):
        mutation = '''
            mutation createUser($input: CreateUserInput!) {
                createUser(newUser: $input) {
                    user {
                        id
                        username
                        firstName
                        lastName
                        email
                    }
                }
            }
        '''
        new_user = {
            'input': {
                'username': 'user04',
                'firstName': 'User',
                'lastName': 'Four',
                'email': 'user04@gmail.com',
                'password': 'user04password',
            },
        }

        expected_result = {
            'data':
            OrderedDict([(
                'createUser',
                OrderedDict([(
                    'user',
                    OrderedDict([
                        ('id', '4'),
                        ('username', 'user04'),
                        ('firstName', 'User'),
                        ('lastName', 'Four'),
                        ('email', 'user04@gmail.com'),
                    ]),
                )]),
            )]),
        }

        executed = cls.client.execute(mutation, variables=new_user)
        assert executed == expected_result
