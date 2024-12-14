from rest_framework import serializers
from .models import Video

class VideoSerializer(serializers.ModelSerializer):
    playlist_url = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = ['id', 'title', 'description', 'created_at', 'playlist_url', 'thumbnail']

    def get_playlist_url(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.playlist_rel_url)
        return obj.playlist_url