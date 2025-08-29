from django.db import models

class Party(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    gst_number = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
