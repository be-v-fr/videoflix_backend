from django.db import models
from django.conf import settings
import os

class Video(models.Model):
    """
    Video model containing file, thumbnail and metadata.
    """
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1024)
    created_at = models.DateTimeField(auto_now_add=True)
    video_upload = models.FileField(upload_to='videos', blank=True, null=True)
    thumbnail = models.FileField(upload_to='video_thumbs', blank=True, null=True)

    def get_videos_dir(self):
        return os.path.join(settings.MEDIA_ROOT, 'videos', f'{self.pk}_{self.title}')