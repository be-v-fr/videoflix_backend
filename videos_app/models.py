from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import os

class Video(models.Model):
    """
    Video model containing file, thumbnail and metadata.
    """
    DOCUMENTARY = 'Documentary'
    DRAMA = 'Drama'
    ROMANCE = 'Romance'
    GENRES = [
        (DOCUMENTARY.lower(), DOCUMENTARY),
        (DRAMA.lower(), DRAMA),
        (ROMANCE.lower(), ROMANCE)
    ]
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1024)
    genre = models.CharField(max_length=32, choices=GENRES, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    video_upload = models.FileField(upload_to='videos', blank=True, null=True)
    thumbnail = models.FileField(upload_to='video_thumbs', blank=True, null=True)
    duration_in_seconds = models.FloatField(default=None, blank=True, null=True)

    @property
    def video_files_rel_dir(self):
        clean_title = self.title.strip()
        formatted_title = clean_title.replace(' ', '_')
        return os.path.join('videos', f'{self.pk}_{formatted_title}')

    @property
    def video_files_abs_dir(self):
        return os.path.join(settings.MEDIA_ROOT, self.video_files_rel_dir)
    
    @property
    def playlist_rel_url(self):
        filename = f'{self.pk}_master.m3u8'
        if os.path.isfile(os.path.join(self.video_files_abs_dir, filename)):
            return os.path.join(settings.MEDIA_URL, self.video_files_rel_dir, filename)
        raise FileNotFoundError(f"Playlist file '{filename}' does not exist in directory for video ID {self.pk}.")

class VideoCompletion(models.Model):
    """
    Video completion model representing the playback state of a video for a user.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    current_time = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'video'], name='unique_user_video')
        ]