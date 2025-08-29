import graphene
from graphene_django.types import DjangoObjectType
from party.models import Party
from party.schema.query import PartyType
from graphene_django_cud.mutations import (
    DjangoCreateMutation,
    DjangoUpdateMutation,
    DjangoDeleteMutation
)


class CreateParty(DjangoCreateMutation):
    class Meta:
        model = Party
        fields = ("id", "name", "phone", "gst_number", "created_at")

        phone = graphene.String(required=True)
        gst_number = graphene.String()

    party = graphene.Field(PartyType)

    def mutate(self, info, name, phone, gst_number=None):
        party = Party.objects.create(name=name, phone=phone, gst_number=gst_number)
        return CreateParty(party=party)

class UpdateParty(DjangoUpdateMutation):
    class Meta:
        model = Party
        fields = ("id", "name", "phone", "gst_number", "created_at")

class DeleteParty(DjangoDeleteMutation):
    class Meta:
        model = Party

class Mutation(graphene.ObjectType):
    create_party = CreateParty.Field()
    update_party = UpdateParty.Field()
    delete_party = DeleteParty.Field()
