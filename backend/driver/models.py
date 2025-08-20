from django.db import models
from django.core.validators import MinLengthValidator, RegexValidator

class Driver(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        validators=[
            RegexValidator(
                regex=r'^\d+$',
                message="Phone number must be numeric."
            ),
            MinLengthValidator(10, message="Phone number must be exactly 10 digits long.")
        ]
    )

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self.phone and not self.phone.isdigit():
            raise ValueError("Phone number must be numeric")
        return super().save(*args, **kwargs)