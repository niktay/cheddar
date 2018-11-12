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
        new_post = CreatePostInput(required=True)

    post = graphene.Field(PostType)

    @staticmethod
    def mutate(root, info, new_post=None):
        post = Post(title=new_post.title, content=new_post.content)
        post.save()

        return CreatePost(post=post)


class DeletePost(graphene.Mutation):
    class Arguments:
        delete_id = graphene.ID(required=True)

    post = graphene.Field(PostType)

    @staticmethod
    def mutate(root, info, delete_id=None):
        unwanted = Post.objects.get(pk=delete_id)
        deleted_data = deepcopy(unwanted)

        unwanted.delete()

        return DeletePost(post=deleted_data)


class UpdatePostInput(InputObjectType):
    id = graphene.ID(required=True)
    title = graphene.String()
    content = graphene.String()


class UpdatePost(graphene.Mutation):
    class Arguments:
        changes = UpdatePostInput(required=True)

    post = graphene.Field(PostType)

    @staticmethod
    def mutate(root, info, changes=None):
        receipient = Post.objects.get(pk=changes.id)
        UpdatePost.save_changes(changes, receipient)

        return UpdatePost(post=receipient)

    @staticmethod
    def save_changes(changes, receipient):
        for key, value in changes.items():
            if key != 'id':
                receipient.__setattr__(key, value)

        receipient.save()


class Query(object):
    all_posts = graphene.List(PostType)

    def resolve_all_posts(self, info, **kwargs):
        return Post.objects.all()


class Mutation(object):
    create_post = CreatePost.Field()
    delete_post = DeletePost.Field()
    update_post = UpdatePost.Field()
