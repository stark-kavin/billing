import graphene
from graphene_django_cud.mutations import (
    DjangoCreateMutation,
    DjangoDeleteMutation,
    DjangoUpdateMutation,
)
from graphene_file_upload.scalars import Upload
from vehicle.models import Vehicle, VehicleBrand, ExpenseCategory, VehicleExpense


class CreateVehicleBrandMutation(DjangoCreateMutation):
    class Meta:
        model = VehicleBrand
        fields = ('name', 'logo')
        field_types = {
            'name': graphene.String(required=True),
            'logo': Upload(),
        }
        
        permissions = ["vehicle.add_vehiclebrand"]


class UpdateVehicleBrandMutation(DjangoUpdateMutation):
    class Meta:
        model = VehicleBrand
        fields = ('name', 'logo')
        field_types = {
            'name': graphene.String(),
            'logo': Upload(),
        }
        permissions = ["vehicle.change_vehiclebrand"]


class DeleteVehicleBrandMutation(DjangoDeleteMutation):
    class Meta:
        model = VehicleBrand
        permissions = ["vehicle.delete_vehiclebrand"]


class CreateVehicleMutation(DjangoCreateMutation):
    class Meta:
        model = Vehicle
        fields = ('brand', 'name', 'year', 'registration_number')
        field_types = {
            'brand': graphene.ID(required=True),
            'name': graphene.String(required=True),
            'year': graphene.Int(required=True),
            'registration_number': graphene.String(required=True),
        }
        
        permissions = ["vehicle.add_vehicle"]


class UpdateVehicleMutation(DjangoUpdateMutation):
    class Meta:
        model = Vehicle
        fields = ('brand', 'name', 'year', 'registration_number')
        field_types = {
            'brand': graphene.ID(),
            'name': graphene.String(),
            'year': graphene.Int(),
            'registration_number': graphene.String(),
        }
        permissions = ["vehicle.change_vehicle"]


class DeleteVehicleMutation(DjangoDeleteMutation):
    class Meta:
        model = Vehicle
        permissions = ["vehicle.delete_vehicle"]


class CreateExpenseCategoryMutation(DjangoCreateMutation):
    class Meta:
        model = ExpenseCategory
        fields = ('name',)
        field_types = {
            'name': graphene.String(required=True),
        }
        permissions = ["vehicle.add_expensecategory"]


class UpdateExpenseCategoryMutation(DjangoUpdateMutation):
    class Meta:
        model = ExpenseCategory
        fields = ('name',)
        field_types = {
            'name': graphene.String(),
        }
        permissions = ["vehicle.change_expensecategory"]


class DeleteExpenseCategoryMutation(DjangoDeleteMutation):
    class Meta:
        model = ExpenseCategory
        permissions = ["vehicle.delete_expensecategory"]


class CreateVehicleExpenseMutation(DjangoCreateMutation):
    class Meta:
        model = VehicleExpense
        fields = ('vehicle', 'category', 'description', 'amount', 'date')
        field_types = {
            'vehicle': graphene.ID(required=True),
            'category': graphene.ID(),
            'description': graphene.String(),
            'amount': graphene.Decimal(required=True),
            'date': graphene.Date(),
        }
        permissions = ["vehicle.add_vehicleexpense"]


class UpdateVehicleExpenseMutation(DjangoUpdateMutation):
    class Meta:
        model = VehicleExpense
        fields = ('vehicle', 'category', 'description', 'amount', 'date')
        field_types = {
            'vehicle': graphene.ID(),
            'category': graphene.ID(),
            'description': graphene.String(),
            'amount': graphene.Decimal(),
            'date': graphene.Date(),
        }
        permissions = ["vehicle.change_vehicleexpense"]


class DeleteVehicleExpenseMutation(DjangoDeleteMutation):
    class Meta:
        model = VehicleExpense
        permissions = ["vehicle.delete_vehicleexpense"]
