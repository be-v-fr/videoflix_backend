from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.cache import cache
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from .models import Video

# Create your tests here.
class VideosTests(APITestCase):
    def setUp(self):
        cache.clear()
        self.user = User.objects.create_user(username='testuser', email='testemail@email.com', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.mock_video_file = SimpleUploadedFile("mock_video.mp4", b"this is not a video file!")
        self.mock_thumb_file = SimpleUploadedFile("mock_thumb.webp", b"this is not an image file!")
        self.mock_video = Video.objects.create(title='testtitle',
                                          description='testdescription',
                                          file=self.mock_video_file,
                                          thumbnail=self.mock_thumb_file)
        
    def tearDown(self):
        cache.clear()        
   
    def test_get_video_list_ok(self):
        """
        Tests videos list view GET request.
        
        Asserts:
            - 200 OK status.
            - Presence of all model fields in response data.
        """
        url = reverse('video-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for key in ('title', 'description', 'created_at', 'file', 'thumbnail'):
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
            - Presence of all model fields in response data.
        """
        url = reverse('video-detail', kwargs={'pk': self.mock_video.pk})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for key in ('title', 'description', 'created_at', 'file', 'thumbnail'):
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
