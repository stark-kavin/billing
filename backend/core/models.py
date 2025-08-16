from django.db import models
from django.core.validators import MinLengthValidator, RegexValidator
from utils.models import SingletonModel

class SiteConfiguration(SingletonModel):
    """
    Singleton model to store global site configuration settings.
    Only one instance of this model can exist at a time.
    """
    site_name = models.CharField(
        max_length=100,
        default="Site Name",
        help_text="The name of the website displayed to users"
    )
    
    address = models.TextField(
        blank=True,
        help_text="Address of the organization"
    )
    
    phone1 = models.CharField(
        max_length=10,
        validators=[
            MinLengthValidator(5),
            RegexValidator(
                regex=r'^\d+$',
                message='Phone number must contain only digits',
                code='invalid_phone'
            ),
        ],
        default="0000000000",
        help_text="Primary contact number"
    )
    
    phone2 = models.CharField(
        max_length=10,
        validators=[
            MinLengthValidator(5),
            RegexValidator(
                regex=r'^\d+$',
                message='Phone number must contain only digits',
                code='invalid_phone'
            ),
        ],
        default="0000000000",
        help_text="Secondary contact number",
        blank=True
    )
    
    site_logo = models.ImageField(
        upload_to='site_logo/',
        blank=True,
        null=True,
        help_text="Site logo image (recommended size: 200x60px)"
    )
    
    class Meta:
        verbose_name = "Site Configuration"
        verbose_name_plural = "Site Configuration"
    
    def __str__(self):
        return self.site_name
    
