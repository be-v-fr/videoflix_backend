from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VideoViewSet, VideoCompletionViewSet

router = DefaultRouter()
router.register(r'main', VideoViewSet, basename='video')
router.register(r'completion', VideoCompletionViewSet, basename='video-completion')

urlpatterns = [
    path('', include(router.urls)),
]