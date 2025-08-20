import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from ..models import Driver


class DriverType(DjangoObjectType):
    class Meta:
        model = Driver
        fields = "__all__"


class DriverQuery(graphene.ObjectType):
    all_drivers = graphene.List(DriverType)
    driver = graphene.Field(DriverType, id=graphene.Int(required=True))

    def resolve_all_drivers(self, info):
        try:
            return Driver.objects.all()
        except Exception as e:
            raise GraphQLError(f"Error fetching drivers: {str(e)}")

    def resolve_driver(self, info, id):
        try:
            return Driver.objects.get(pk=id)
        except Driver.DoesNotExist:
            raise GraphQLError(f"Driver with id {id} not found.")
        except Exception as e:
            raise GraphQLError(f"Error fetching driver: {str(e)}")