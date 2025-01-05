from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
import django_rq
from videoflix import settings
from .models import Video
from .utils import delete_source_video
from .tasks import set_video_duration, convert_video_to_hls
import os
import shutil

@receiver(post_save, sender=Video) 
def create_video(sender, instance, created, **kwargs):
    """
    Enqueues routine tasks upon video creation regarding the video duration and conversion to HLS format.
    """
    if created and not settings.TESTING:
        queue = django_rq.get_queue('default', autocommit=True)
        try:
            duration_task = queue.enqueue(set_video_duration, video_obj=instance)
            queue.enqueue(convert_video_to_hls, video_obj=instance, depends_on=duration_task)
        except Exception as e:
            print("Error while executing tasks on video creation:", e)

@receiver(post_delete, sender=Video) 
def delete_video(sender, instance, *args, **kwargs):
    """
    Deletes associated video content files upon deletion of a video model instance.
    """
    delete_source_video(instance)
    video_files_abs_dir = instance.video_files_abs_dir
    if os.path.isdir(video_files_abs_dir):
        shutil.rmtree(video_files_abs_dir)
    if instance.thumbnail:
        if os.path.isfile(instance.thumbnail.path):
            os.remove(instance.thumbnail.path)