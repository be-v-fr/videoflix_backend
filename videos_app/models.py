from django.db import models

class Video(models.Model):
    """
    Video model containing file, thumbnail and metadata.
    """
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1024)
    created_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='videos', blank=True, null=True)
    thumbnail = models.FileField(upload_to='video_thumbs', blank=True, null=True)