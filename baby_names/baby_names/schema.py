import graphene
import names.schema

# make the schema availiable project wide.
class Query(names.schema.Query, graphene.ObjectType):
    pass


class Mutation(names.schema.Mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query = Query,mutation = Mutation)