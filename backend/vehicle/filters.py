import django_filters
from .models import VehicleExpense

class VehicleExpenseFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(field_name="date", lookup_expr="gte")
    end_date = django_filters.DateFilter(field_name="date", lookup_expr="lte")

    class Meta:
        model = VehicleExpense
        fields = ["vehicle_id", "category_id"]
