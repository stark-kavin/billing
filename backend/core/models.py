from django.db import models
from django.core.validators import MinLengthValidator, RegexValidator
from utils.models import SingletonModel
import uuid

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
            MinLengthValidator(10, message="Phone number must be exactly 10 digits long."),
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
            MinLengthValidator(10, message="Phone number must be exactly 10 digits long."),
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

    def _get_site_logo_path(instance, filename: str) -> str:
        """
        Generate a unique file path for the site logo image.
        """
        ext = filename.split('.')[-1]
        filename = f"{uuid.uuid4()}.{ext}"
        return f'site_logo/{filename}'
    
    site_logo = models.ImageField(
        upload_to=_get_site_logo_path,
        blank=True,
        null=True,
        help_text="Site logo image (recommended size: 200x60px)"
    )
    
    class Meta:
        verbose_name = "Site Configuration"
        verbose_name_plural = "Site Configuration"
    
    def __str__(self):
        return self.site_name
    
    def save(self, *args, **kwargs):
        """
        Override the save method to delete the old image when a new one is uploaded.
        """
        if self.pk:
            try:
                old_instance = SiteConfiguration.objects.get(pk=self.pk)
                if old_instance.site_logo and self.site_logo != old_instance.site_logo:
                    old_image = old_instance.site_logo
                else:
                    old_image = None
            except SiteConfiguration.DoesNotExist:
                old_image = None
        else:
            old_image = None
        
        super().save(*args, **kwargs)
        
        if old_image:
            old_image.delete(save=False)