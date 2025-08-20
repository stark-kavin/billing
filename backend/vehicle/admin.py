from django.contrib import admin
from .models import VehicleBrand, Vehicle, ExpenseCategory, VehicleExpense
from django.utils.html import format_html

@admin.register(VehicleBrand)
class VehicleBrandAdmin(admin.ModelAdmin):
    list_display = ('name','logo_preview')
    search_fields = ('name',)

    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="height:50px;"/>', obj.logo.url)
        return format_html('<svg xmlns="http://www.w3.org/2000/svg" height="50px" viewBox="0 -960 960 960" width="50px" fill="#e3e3e3"><path d="M200-120q-33 0-56.5-23.5T120-200v-560q0-33 23.5-56.5T200-840h560q33 0 56.5 23.5T840-760v560q0 33-23.5 56.5T760-120H200Zm40-337 160-160 160 160 160-160 40 40v-183H200v263l40 40Zm-40 257h560v-264l-40-40-160 160-160-160-160 160-40-40v184Zm0 0v-264 80-376 560Z"/></svg>')
    logo_preview.short_description = "Logo"

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('brand', 'name', 'year', 'registration_number')
    list_filter = ('brand', 'year')
    search_fields = ('name', 'brand__name', 'registration_number')


@admin.register(ExpenseCategory)
class ExpenseCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'expense_count')
    search_fields = ('name',)

    def expense_count(self, obj):
        return obj.expenses.count()
    expense_count.short_description = "Number of Expenses"


@admin.register(VehicleExpense)
class VehicleExpenseAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'category', 'amount', 'date', 'created_at')
    list_filter = ('category', 'date', 'vehicle__brand', 'created_at')
    search_fields = ('vehicle__name', 'vehicle__registration_number', 'category__name', 'description')
    date_hierarchy = 'date'
    
    fieldsets = (
        (None, {
            'fields': ('vehicle', 'category', 'amount', 'date')
        }),
        ('Details', {
            'fields': ('description',),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('vehicle', 'category', 'vehicle__brand')
