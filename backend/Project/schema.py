import graphene
import graphql_jwt
from core.schema.query import CoreQuery
from core.schema.mutation import UpdateSiteConfiguration

class Query(graphene.ObjectType):
    core = graphene.Field(CoreQuery)
    def resolve_core(self, info):
        return CoreQuery()


class Mutation(graphene.ObjectType):
    update_site_configuration = UpdateSiteConfiguration.Field()
    
    # JWT authentication mutations
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
