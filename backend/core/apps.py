from django.apps import AppConfig
from django.conf import settings


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        from django.contrib.auth import get_user_model
        from django.db.utils import OperationalError, ProgrammingError

        if settings.DEBUG:
            User = get_user_model()
            try:
                if not User.objects.filter(username="dev").exists():
                    User.objects.create_superuser(
                        username="dev",
                        email="dev@example.com",
                        password="admin123"
                    )
                    print("✅ Dev superuser created: dev / admin123")
            except (OperationalError, ProgrammingError):
                # Happens before migrations, safe to ignore
                pass    