import graphene
from graphene_django_cud.mutations import (
    DjangoCreateMutation,
    DjangoDeleteMutation,
    DjangoUpdateMutation,
)
from django.core.exceptions import ValidationError
from graphql import GraphQLError
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
    
    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        try:
            # Validate business logic
            if 'phone' in input and input['phone']:
                phone = input['phone'].strip()
                if not phone.isdigit():
                    raise GraphQLError("Phone number must contain only digits.")
                if len(phone) != 10:
                    raise GraphQLError("Phone number must be exactly 10 digits long.")
                input['phone'] = phone
            
            return super().mutate_and_get_payload(root, info, **input)
        except ValidationError as e:
            raise GraphQLError(f"Validation error: {e.message}")
        except Exception as e:
            raise GraphQLError(f"Error creating driver: {str(e)}")

class UpdateDriverMutation(DjangoUpdateMutation):
    class Meta:
        model = Driver
        fields = ('name', 'phone')
        field_types = {
            'name': graphene.String(),
            'phone': graphene.String(),
        }
        permissions = ["driver.change_driver"]
    
    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        try:
            # Validate business logic
            if 'phone' in input and input['phone']:
                phone = input['phone'].strip()
                if not phone.isdigit():
                    raise GraphQLError("Phone number must contain only digits.")
                if len(phone) != 10:
                    raise GraphQLError("Phone number must be exactly 10 digits long.")
                input['phone'] = phone
            
            return super().mutate_and_get_payload(root, info, **input)
        except ValidationError as e:
            raise GraphQLError(f"Validation error: {e.message}")
        except Driver.DoesNotExist:
            raise GraphQLError("Driver not found.")
        except Exception as e:
            raise GraphQLError(f"Error updating driver: {str(e)}")

class DeleteDriverMutation(DjangoDeleteMutation):
    class Meta:
        model = Driver
        permissions = ["driver.delete_driver"]
    
    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        try:
            return super().mutate_and_get_payload(root, info, **input)
        except Driver.DoesNotExist:
            raise GraphQLError("Driver not found.")
        except Exception as e:
            raise GraphQLError(f"Error deleting driver: {str(e)}")