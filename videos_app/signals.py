from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from .models import Video
import os
from pathlib import Path

@receiver(post_save, sender=Video) 
def create_video(sender, instance, created, **kwargs):
    if created:
        pass # add rendering logic later

@receiver(post_delete, sender=Video) 
def delete_video(sender, instance, *args, **kwargs):
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)
            # add / replace different video resolution files later
    if instance.thumbnail:
        if os.path.isfile(instance.thumbnail.path):
            os.remove(instance.thumbnail.path)