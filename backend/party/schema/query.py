import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from party.models import Party
from graphene.relay import Node
from graphene_django.filter import DjangoFilterConnectionField

class PartyType(DjangoObjectType):
    class Meta:
        model = Party
        fields = ("id", "name", "phone", "gst_number", "created_at")
        filter_fields = {
            "name": ["exact", "icontains", "istartswith"],
            "phone": ["exact", "icontains", "istartswith"],
            "gst_number": ["exact", "icontains", "istartswith"],
            "created_at": ["exact", "range"],
        }
        interfaces = (Node,)

class PartyQuery(graphene.ObjectType):

    parties = DjangoFilterConnectionField(PartyType)
    def resolve_parties(self, info, **kwargs):
        return Party.objects.all()

    party = graphene.Field(PartyType, id=graphene.ID(required=True))
    def resolve_party(self, info, id):
        try:
            return Party.objects.get(pk=id)
        except Party.DoesNotExist:
            raise GraphQLError("Party not found")