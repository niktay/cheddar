import blog.schema
import graphene
import users.schema


class Query(users.schema.Query, blog.schema.Query, graphene.ObjectType):
    pass


class Mutation(
    users.schema.Mutation, blog.schema.Mutation,
    graphene.ObjectType,
):
    pass


schema = graphene.Schema(
    query=Query,
    mutation=Mutation,
)
