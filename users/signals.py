from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import Profile
from django.shortcuts import get_object_or_404

# When a User is created, automatically create a Profile for that user
@receiver(post_save, sender=User)
def create_or_update_profile(sender, instance, created, **kwargs):
    if created:  # If the user is newly created
        # Create a Profile for the user with their email and username
        Profile.objects.create(
            user=instance,
            email=instance.email,
            display_name=instance.username,
        )
    else:  # If the user already exists
        # Update the email in the profile
        profile = get_object_or_404(Profile, user=instance)
        profile.email = instance.email
        profile.save()

# When a Profile is updated, sync the user's email with the profile email
@receiver(post_save, sender=Profile)
def sync_user_email_with_profile(sender, instance, created, **kwargs):
    if not created:  # If the profile is updated, not newly created
        user = instance.user
        # If the email in the profile is different from the user's email
        if user.email != instance.email:
            user.email = instance.email  # Update the user's email to match the profile
            user.save()
