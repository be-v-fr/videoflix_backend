from rest_framework import serializers
from .models import Video

class VideoSerializer(serializers.ModelSerializer):
    video_files_url = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = ['id', 'title', 'description', 'created_at', 'video_files_url', 'thumbnail']

    def get_video_files_url(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.video_files_rel_url)
        return obj.video_files_rel_url