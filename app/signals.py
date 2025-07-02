from django.apps import apps
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    Profile = apps.get_model('app', 'Profile')  # Replace 'app' with your app's name
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # This avoids circular import
    profile = getattr(instance, 'profile', None)
    if profile:
        profile.save()
