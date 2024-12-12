from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.cache import cache
from django.test import override_settings
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from .models import Video
import os
import tempfile

class VideosTests(APITestCase):
    def create_temp_dir(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.override_settings = override_settings(MEDIA_ROOT=self.temp_dir.name)
        self.override_settings.enable()  

    def setUp(self):
        cache.clear()
        self.create_temp_dir()
        self.user = User.objects.create_user(username='testuser', email='testemail@email.com', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.mock_video_file = SimpleUploadedFile("mock_video.mp4", b"this is not a video file!")
        self.mock_thumb_file = SimpleUploadedFile("mock_thumb.webp", b"this is not an image file!")
        self.mock_video = Video.objects.create(
            title='testtitle',
            description='testdescription',
            video_upload=self.mock_video_file,
            thumbnail=self.mock_thumb_file)      
        
    def tearDown(self):
        self.override_settings.disable()
        self.temp_dir.cleanup()
        cache.clear()        
   
    def test_get_video_list_ok(self):
        """
        Tests videos list view GET request.
        
        Asserts:
            - 200 OK status.
            - Absence of file field.
            - Presence of all model fields in response data.
        """
        url = reverse('video-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn('file', response.data)
        for key in ('id', 'title', 'description', 'created_at', 'video_files_url', 'thumbnail'):
            self.assertIn(key, response.data[0])
            
    def test_get_video_list_not_authenticated_unauthorized(self):
        """
        Tests failing videos list view GET request without credentials.
        
        Asserts:
            - 401 Unauthorized status.
        """
        self.client.logout()
        url = reverse('video-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
            
    def test_get_video_detail_ok(self):
        """
        Tests videos detail view GET request.
        
        Asserts:
            - 200 OK status.
            - Absence of file field.
            - Presence of all required fields in response data.
        """
        url = reverse('video-detail', kwargs={'pk': self.mock_video.pk})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn('file', response.data)
        for key in ('id', 'title', 'description', 'created_at', 'video_files_url', 'thumbnail'):
            self.assertIn(key, response.data)
        
    def test_get_video_detail_not_authenticated_unauthorized(self):
        """
        Tests failing videos detail view GET request without credentials.
        
        Asserts:
            - 401 Unauthorized status.
        """
        self.client.logout()
        url = reverse('video-detail', kwargs={'pk': self.mock_video.pk})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
