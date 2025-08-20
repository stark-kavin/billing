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

from vehicle.schema.query import VehicleQuery
from vehicle.schema.mutation import (
    CreateVehicleBrandMutation,
    UpdateVehicleBrandMutation,
    DeleteVehicleBrandMutation,
    CreateVehicleMutation,
    UpdateVehicleMutation,
    DeleteVehicleMutation,
    CreateExpenseCategoryMutation,
    UpdateExpenseCategoryMutation,
    DeleteExpenseCategoryMutation,
    CreateVehicleExpenseMutation,
    UpdateVehicleExpenseMutation,
    DeleteVehicleExpenseMutation
)

class Query(graphene.ObjectType):
    core = graphene.Field(CoreQuery)
    driver = graphene.Field(DriverQuery)
    vehicle = graphene.Field(VehicleQuery)

    def resolve_core(self, info):
        return CoreQuery()

    def resolve_driver(self, info):
        return DriverQuery()

    def resolve_vehicle(self, info):
        return VehicleQuery()


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

    # Vehicle mutations
    create_vehicle_brand = CreateVehicleBrandMutation.Field()
    update_vehicle_brand = UpdateVehicleBrandMutation.Field()
    delete_vehicle_brand = DeleteVehicleBrandMutation.Field()
    create_vehicle = CreateVehicleMutation.Field()
    update_vehicle = UpdateVehicleMutation.Field()
    delete_vehicle = DeleteVehicleMutation.Field()
    
    # Expense Category mutations
    create_expense_category = CreateExpenseCategoryMutation.Field()
    update_expense_category = UpdateExpenseCategoryMutation.Field()
    delete_expense_category = DeleteExpenseCategoryMutation.Field()
    
    # Vehicle Expense mutations
    create_vehicle_expense = CreateVehicleExpenseMutation.Field()
    update_vehicle_expense = UpdateVehicleExpenseMutation.Field()
    delete_vehicle_expense = DeleteVehicleExpenseMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
