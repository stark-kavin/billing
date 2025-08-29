from django.contrib import admin
from .models import Party

@admin.register(Party)
class PartyAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'gst_number', 'created_at')
    search_fields = ('name', 'phone', 'gst_number')
