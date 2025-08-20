import graphene
import graphql_jwt

from core.schema.query import CoreQuery
from core.schema.mutation import UpdateSiteConfiguration

from driver.schema.query import DriverQuery
from driver.schema.mutation import (
    CreateDriverMutation,
    UpdateDriverMutation,
    DeleteDriverMutation
)

class Query(graphene.ObjectType):
    core = graphene.Field(CoreQuery)
    driver = graphene.Field(DriverQuery)

    def resolve_core(self, info):
        return CoreQuery()


class Mutation(graphene.ObjectType):

    # Core mutations
    update_site_configuration = UpdateSiteConfiguration.Field()
    
    # JWT authentication mutations
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

    # Driver mutations
    create_driver = CreateDriverMutation.Field()
    update_driver = UpdateDriverMutation.Field()
    delete_driver = DeleteDriverMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
