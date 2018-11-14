import graphene
from django.contrib.auth import get_user_model
from graphene import InputObjectType
from graphene_django import DjangoObjectType


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()


class CreateUserInput(InputObjectType):
    username = graphene.String(required=True)
    password = graphene.String(required=True)
    first_name = graphene.String(required=True)
    last_name = graphene.String(required=True)
    email = graphene.String(required=True)


class CreateUser(graphene.Mutation):
    class Arguments:
        new_user = CreateUserInput(required=True)

    user = graphene.Field(UserType)

    def mutate(root, info, new_user=None):
        user = get_user_model()(
            username=new_user.username,
            email=new_user.email,
            first_name=new_user.first_name,
            last_name=new_user.last_name,
        )

        user.set_password(new_user.password)
        user.save()

        return CreateUser(user=user)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()


class Query(graphene.ObjectType):
    me = graphene.Field(UserType)
    all_users = graphene.List(UserType)

    def resolve_all_users(self, info):
        return get_user_model().objects.all()

    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not Logged in!')
        return user
