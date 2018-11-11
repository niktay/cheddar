from copy import deepcopy

import graphene
from blog.models import Post
from graphene import InputObjectType
from graphene_django.types import DjangoObjectType


class PostType(DjangoObjectType):
    class Meta:
        model = Post


class CreatePostInput(InputObjectType):
    title = graphene.String(required=True)
    content = graphene.String(required=True)


class CreatePost(graphene.Mutation):
    class Arguments:
        post_data = CreatePostInput(required=True)

    post = graphene.Field(PostType)

    @staticmethod
    def mutate(root, info, post_data=None):
        post = Post(title=post_data.title, content=post_data.content)
        post.save()
        return CreatePost(post=post)


class DeletePostInput(InputObjectType):
    id = graphene.ID(required=True)


class DeletePost(graphene.Mutation):
    class Arguments:
        post_data = DeletePostInput(required=True)

    post = graphene.Field(PostType)

    @staticmethod
    def mutate(root, info, post_data=None):
        post_to_delete = Post.objects.get(pk=post_data.id)
        deleted_post = deepcopy(post_to_delete)

        post_to_delete.delete()

        return DeletePost(post=deleted_post)


class Query(object):
    all_posts = graphene.List(PostType)

    def resolve_all_posts(self, info, **kwargs):
        return Post.objects.all()


class Mutation(object):
    create_post = CreatePost.Field()
    delete_post = DeletePost.Field()
