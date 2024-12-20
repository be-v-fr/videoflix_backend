from rest_framework import serializers
from .models import Video, VideoCompletion

class VideoSerializer(serializers.ModelSerializer):
    playlist_url = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = ['id', 'title', 'description', 'created_at', 'playlist_url', 'duration_in_seconds', 'thumbnail']

    def get_playlist_url(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.playlist_rel_url)
        return obj.playlist_url
    
class VideoCompletionSerializer(serializers.ModelSerializer):
    video_id = serializers.PrimaryKeyRelatedField(queryset=Video.objects.all(), source='video')
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = VideoCompletion
        fields = ['id', 'video_id', 'current_time', 'updated_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request_method = self.context['request'].method
        if request_method in ['PUT', 'PATCH']:
            self.fields['video_id'].read_only = True

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'video' in validated_data:
            raise serializers.ValidationError('You cannot change the video of an existing completion.')
        validated_data['user'] = self.context['request'].user
        return super().update(instance, validated_data)