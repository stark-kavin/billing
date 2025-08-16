from django.db import models

class SingletonModel(models.Model):
    
    _PK = 1
    
    class Meta:
        abstract = True
        
    def save(self, *args, **kwargs):
        self.pk = self._PK
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=cls._PK)
        return obj
