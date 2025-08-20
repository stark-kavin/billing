import graphene
from graphene_django import DjangoObjectType
from ..models import Driver


class DriverType(DjangoObjectType):
    class Meta:
        model = Driver
        fields = "__all__"


class DriverQuery(graphene.ObjectType):
    all_drivers = graphene.List(DriverType)
    driver = graphene.Field(DriverType, id=graphene.Int(required=True))

    def resolve_all_drivers(self, info):
        return Driver.objects.all()

    def resolve_driver(self, info, id):
        try:
            return Driver.objects.get(pk=id)
        except Driver.DoesNotExist:
            return None