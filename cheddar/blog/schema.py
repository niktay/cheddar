import graphene
from blog.models import Post
from graphene import InputObjectType
from graphene_django.types import DjangoObjectType


class PostType(DjangoObjectType):
    class Meta:
        model = Post


class PostInput(InputObjectType):
    title = graphene.String(required=True)
    content = graphene.String(required=True)


class CreatePost(graphene.Mutation):
    class Arguments:
        post_data = PostInput(required=True)

    post = graphene.Field(PostType)

    @staticmethod
    def mutate(root, info, post_data=None):
        post = Post(title=post_data.title, content=post_data.content)
        post.save()
        return CreatePost(post=post)


class Query(object):
    all_posts = graphene.List(PostType)

    def resolve_all_posts(self, info, **kwargs):
        return Post.objects.all()


class Mutation(object):
    create_post = CreatePost.Field()
