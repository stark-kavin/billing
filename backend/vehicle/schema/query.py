import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphene import relay
from ..models import Vehicle, VehicleBrand, ExpenseCategory, VehicleExpense
from ..filters import VehicleExpenseFilter


class VehicleBrandType(DjangoObjectType):
    class Meta:
        model = VehicleBrand
        fields = "__all__"


class VehicleType(DjangoObjectType):
    class Meta:
        model = Vehicle
        fields = "__all__"


class ExpenseCategoryType(DjangoObjectType):
    class Meta:
        model = ExpenseCategory
        fields = "__all__"


class VehicleExpenseType(DjangoObjectType):
    class Meta:
        model = VehicleExpense
        fields = "__all__"
        filter_fields = ['vehicle_id', 'category_id']
        interfaces = (relay.Node, )


class VehicleQuery(graphene.ObjectType):
    all_vehicle_brands = graphene.List(VehicleBrandType)
    vehicle_brand = graphene.Field(VehicleBrandType, id=graphene.Int(required=True))
    
    all_vehicles = graphene.List(VehicleType)
    vehicle = graphene.Field(VehicleType, id=graphene.Int(required=True))
    vehicles_by_brand = graphene.List(VehicleType, brand_id=graphene.Int(required=True))
    
    all_expense_categories = graphene.List(ExpenseCategoryType)
    expense_category = graphene.Field(ExpenseCategoryType, id=graphene.Int(required=True))
    
    all_vehicle_expenses = graphene.List(VehicleExpenseType)
    vehicle_expense = graphene.Field(VehicleExpenseType, id=graphene.Int(required=True))
    expenses = DjangoFilterConnectionField(
        VehicleExpenseType,
        filterset_class=VehicleExpenseFilter
    )

    def resolve_all_vehicle_brands(self, info):
        return VehicleBrand.objects.all()

    def resolve_vehicle_brand(self, info, id):
        try:
            return VehicleBrand.objects.get(pk=id)
        except VehicleBrand.DoesNotExist:
            return None

    def resolve_all_vehicles(self, info):
        return Vehicle.objects.select_related('brand').all()

    def resolve_vehicle(self, info, id):
        try:
            return Vehicle.objects.select_related('brand').get(pk=id)
        except Vehicle.DoesNotExist:
            return None

    def resolve_vehicles_by_brand(self, info, brand_id):
        return Vehicle.objects.filter(brand_id=brand_id).select_related('brand')

    def resolve_all_expense_categories(self, info):
        return ExpenseCategory.objects.all()

    def resolve_expense_category(self, info, id):
        try:
            return ExpenseCategory.objects.get(pk=id)
        except ExpenseCategory.DoesNotExist:
            return None

    def resolve_all_vehicle_expenses(self, info):
        return VehicleExpense.objects.select_related('vehicle', 'category', 'vehicle__brand').all()

    def resolve_vehicle_expense(self, info, id):
        try:
            return VehicleExpense.objects.select_related('vehicle', 'category', 'vehicle__brand').get(pk=id)
        except VehicleExpense.DoesNotExist:
            return None
