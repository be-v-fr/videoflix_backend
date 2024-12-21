from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from .models import Video, VideoCompletion
from .serializers import VideoSerializer, VideoCompletionSerializer
from .permissions import IsOwnerOrStaff

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

class VideoViewSet(ReadOnlyModelViewSet):
    """
    API endpoint for videos view.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

    @method_decorator(cache_page(CACHE_TTL))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(CACHE_TTL))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
class VideoCompletionViewSet(ModelViewSet):
    """
    API endpoint for video completions view.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwnerOrStaff]
    serializer_class = VideoCompletionSerializer

    def get_queryset(self):
        """
        Filter queryset to return objects featuring the current user only.
        """
        current_user = self.request.user
        if current_user.is_staff:
            return VideoCompletion.objects.all()
        return VideoCompletion.objects.filter(user=current_user)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance, created = VideoCompletion.objects.update_or_create(
            user=request.user,
            video=serializer.validated_data['video'],
            defaults={'current_time': serializer.validated_data['current_time']}
        )
        response_serializer = self.get_serializer(instance)
        headers = self.get_success_headers(response_serializer.data)
        if created:
            return Response(response_serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(response_serializer.data, status=status.HTTP_200_OK, headers=headers)