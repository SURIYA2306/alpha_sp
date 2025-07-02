from django.apps import AppConfig

class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'  # Replace with your app's actual name

    def ready(self):
        from django.apps import apps
        profile =apps.get_model('app', 'profile')

