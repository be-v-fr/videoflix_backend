from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
import django_rq
from .models import Video
from .utils import delete_source_video
from .tasks import convert_video_to_hls
import os
import shutil

@receiver(post_save, sender=Video) 
def create_video(sender, instance, created, **kwargs):
    if created:
        queue = django_rq.get_queue('default', autocommit=True)
        queue.enqueue(convert_video_to_hls, video_obj=instance)

@receiver(post_delete, sender=Video) 
def delete_video(sender, instance, *args, **kwargs):
    delete_source_video(instance)
    videos_dir = instance.get_videos_dir()
    if os.path.isdir(videos_dir):
        shutil.rmtree(videos_dir)
    if instance.thumbnail:
        if os.path.isfile(instance.thumbnail.path):
            os.remove(instance.thumbnail.path)