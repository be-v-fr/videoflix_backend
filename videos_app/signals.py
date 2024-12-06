from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
import django_rq
from .models import Video
from .tasks import convert_video_quality
from .utils import add_suffix_to_filename
import os

RESOLUTIONS = (480, 720, 1080)

@receiver(post_save, sender=Video) 
def create_video(sender, instance, created, **kwargs):
    if created:
        for res in RESOLUTIONS:
            queue = django_rq.get_queue('default', autocommit=True)
            queue.enqueue(convert_video_quality, kwargs={'source': instance.file.path, 'resolution_in_p': res})

@receiver(post_delete, sender=Video) 
def delete_video(sender, instance, *args, **kwargs):
    if instance.file:
        for res in RESOLUTIONS:
            res_path = add_suffix_to_filename(instance.file.path, f'_{res}p')
            if os.path.isfile(res_path):
                os.remove(res_path)
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)
    if instance.thumbnail:
        if os.path.isfile(instance.thumbnail.path):
            os.remove(instance.thumbnail.path)