from .models import Profile
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from your_app.management.commands.create_rds import Command

@receiver(post_save, sender=User)
def create_profile(sender,instance, created, **kwargs):
    if created:
        Profile.objects.create(staff=instance)

@receiver(post_save, sender=User)
def save_profile(sender,instance, **kwargs):
    instance.profile.save()

@receiver(post_migrate)
def create_rds_after_migration(sender, **kwargs):
    Command().handle()