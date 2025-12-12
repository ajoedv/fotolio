from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from .models import Profile


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Ensure every User has a related Profile.
    Creates one on first save, and keeps it in sync later.
    """
    if created:
        Profile.objects.create(user=instance)
    else:
        # In case a user existed before profiles were introduced
        try:
            instance.profile.save()
        except Profile.DoesNotExist:
            Profile.objects.create(user=instance)
