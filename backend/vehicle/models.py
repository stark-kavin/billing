import uuid
from django.db import models
from django.utils import timezone


def get_brand_logo_upload_path(instance, filename: str) -> str:
    extension = filename.split('.')[-1]
    return f"vehicle_brands/logos/{uuid.uuid4()}.{extension}"


class VehicleBrand(models.Model):
    """
    Represents a vehicle brand (e.g., Toyota, Ford, BMW).
    """
    name = models.CharField(max_length=100, unique=True, db_index=True)
    logo = models.ImageField(upload_to=get_brand_logo_upload_path, blank=True, null=True)

    class Meta:
        verbose_name = "Brand"
        verbose_name_plural = "Brands"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Vehicle(models.Model):
    """
    Represents a vehicle belonging to a specific brand.
    """
    brand = models.ForeignKey(
        VehicleBrand, 
        on_delete=models.PROTECT,
        related_name="vehicles"
    )
    name = models.CharField(max_length=100, db_index=True)
    year = models.PositiveIntegerField()
    registration_number = models.CharField(max_length=20, unique=True, db_index=True, help_text="Unique registration number (e.g., TN 01 AT 1234)")

    class Meta:
        verbose_name = "Vehicle"
        verbose_name_plural = "Vehicles"
        ordering = ["brand__name", "name"]

    def __str__(self) -> str:
        return f"{self.brand.name} {self.name} ({self.year})"
    

class ExpenseCategory(models.Model):
    """
    Categories of expenses (Fuel, Insurance, Maintenance, Tax, etc.)
    """
    name = models.CharField(max_length=100, unique=True, db_index=True)
    emoji = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name = "Expense Category"
        verbose_name_plural = "Expense Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class VehicleExpense(models.Model):
    """
    Tracks expenses associated with a specific vehicle.
    """
    vehicle = models.ForeignKey(
        "Vehicle", 
        on_delete=models.CASCADE,
        related_name="expenses"
    )
    category = models.ForeignKey(
        ExpenseCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="expenses"
    )
    description = models.TextField(blank=True, help_text="Optional description of the expense")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Vehicle Expense"
        verbose_name_plural = "Vehicle Expenses"
        ordering = ["-date", "-created_at"]
        indexes = [
            models.Index(fields=['date']),
            models.Index(fields=['vehicle', 'date']),
            models.Index(fields=['category', 'date']),
        ]

    def __str__(self):
        return f"{self.vehicle} - {self.category or 'Uncategorized'} - ${self.amount} ({self.date})"