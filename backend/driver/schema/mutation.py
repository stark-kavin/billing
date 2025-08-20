import graphene
from graphene_django_cud.mutations import (
    DjangoCreateMutation,
    DjangoDeleteMutation,
    DjangoUpdateMutation,
)
from driver.models import Driver

class CreateDriverMutation(DjangoCreateMutation):
    class Meta:
        model = Driver
        fields = ('name', 'phone')
        field_types = {
            'name': graphene.String(required=True),
            'phone': graphene.String(),
        }
        
        permissions = ["driver.add_driver"]

class UpdateDriverMutation(DjangoUpdateMutation):
    class Meta:
        model = Driver
        fields = ('name', 'phone')
        field_types = {
            'name': graphene.String(),
            'phone': graphene.String(),
        }
        permissions = ["driver.change_driver"]

class DeleteDriverMutation(DjangoDeleteMutation):
    class Meta:
        model = Driver
        permissions = ["driver.delete_driver"]