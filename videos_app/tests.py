from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.cache import cache
from django.test import override_settings
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from .models import Video, VideoCompletion
import os
import tempfile

class VideosTests(APITestCase):
    """
    Videos test class testing video metadata requests.
    """
    def create_temp_dir(self):
        """
        Creates temporary directory to temporarily save test files in.
        """
        self.temp_dir = tempfile.TemporaryDirectory()
        self.override_settings = override_settings(MEDIA_ROOT=self.temp_dir.name)
        self.override_settings.enable()

    def setUp(self):
        """
        Setup method creating an authenticated user and a video object using mock files.
        """
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
            genre=Video.GENRES[0],
            video_upload=self.mock_video_file,
            thumbnail=self.mock_thumb_file,
            duration_in_seconds=7.65)
        self.create_mock_playlist()

    def create_mock_playlist(self):
        """
        Creates mock playlist in temporary directory.
        """
        video_dir = os.path.join(self.temp_dir.name, 'videos', f"{self.mock_video.pk}_testtitle")
        os.makedirs(video_dir, exist_ok=True)
        playlist_path = os.path.join(video_dir, f"{self.mock_video.pk}_master.m3u8")
        with open(playlist_path, 'w') as f:
            f.write("this is not a playlist file!")
        
    def tearDown(self):
        """
        Resets the system to the state before testing.
        """
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
        for key in ('id', 'title', 'description', 'genre', 'created_at', 'playlist_url', 'duration_in_seconds', 'thumbnail'):
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
        for key in ('id', 'title', 'description', 'genre', 'created_at', 'playlist_url', 'duration_in_seconds', 'thumbnail'):
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

class VideoCompletionTests(APITestCase):
    """
    Video completion test class testing playback state requests.
    """
    def generate_create_data(self):
        """
        Returns data to create a video completion object.
        """
        return {
            'video_id': self.mock_video.pk,
            'current_time': 2.34
        }

    def create_temp_dir(self):
        """
        Copies temporary directory creation from videos tests class.
        """
        VideosTests.create_temp_dir(self=self)

    def setUp(self):
        """
        Extends videos tests setup by creating a video completion object and introducing a second user. 
        """
        VideosTests.setUp(self=self)
        self.different_user = User.objects.create_user(username='testuser2', email='testemail2@email.com', password='testpassword')
        self.video_completion = VideoCompletion.objects.create(
            user=self.user,
            **self.generate_create_data()
        )

    def create_mock_playlist(self):
        """
        Copies mock playlist creation from videos tests class.
        """
        VideosTests.create_mock_playlist(self=self)
        
    def tearDown(self):
        """
        Copies teardown method from videos tests class.
        """
        VideosTests.tearDown(self=self)  

    def test_get_video_completion_list_ok(self):
        """
        Tests video completions list view GET request.
        
        Asserts:
            - 200 OK status.
            - Absence of user field in response data.
            - Presence of all serializer fields in response data.
        """
        url = reverse('video-completion-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn('user', response.data[0])
        for key in ('id', 'video_id', 'current_time', 'updated_at'):
            self.assertIn(key, response.data[0])

    def test_get_video_completion_list_different_user_ok(self):
        """
        Tests video completions list view GET request when the video completion
        object is not assigned to the active user.
        
        Asserts:
            - 200 OK status.
            - Empty response.
        """
        self.video_completion.user = self.different_user
        self.video_completion.save()
        url = reverse('video-completion-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_get_video_completion_list_not_authenticated_unauthorized(self):
        """
        Tests video completions list view GET request without credentials.
        
        Asserts:
            - 401 Unauthorized status.
        """
        self.client.logout()
        url = reverse('video-completion-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_video_completion_detail_ok(self):
        """
        Tests video completions detail view GET request.
        
        Asserts:
            - 200 OK status.
            - Absence of user field in response data.
            - Presence of all serializer fields in response data.
        """
        url = reverse('video-completion-detail', kwargs={'pk': self.video_completion.pk})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn('user', response.data)
        for key in ('id', 'video_id', 'current_time', 'updated_at'):
            self.assertIn(key, response.data)

    def test_get_video_completion_detail_different_user_not_found(self):
        """
        Tests video completions detail view GET request when the video completion
        object is not assigned to the active user.
        
        Asserts:
            - 404 Not found status.
        """
        self.video_completion.user = self.different_user
        self.video_completion.save()
        url = reverse('video-completion-detail', kwargs={'pk': self.video_completion.pk})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_video_completion_detail_not_authenticated_unauthorized(self):
        """
        Tests video completions detail view GET request without credentials.
        
        Asserts:
            - 401 Unauthorized status.
        """
        self.client.logout()
        url = reverse('video-completion-detail', kwargs={'pk': self.video_completion.pk})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_video_completion_list_created(self):
        """
        Tests video completions list view POST request.
        
        Asserts:
            - 201 Created status.
            - Object user is request user.
            - Absence of user field in response data.
            - Presence of all serializer fields in response data.
        """
        self.video_completion.delete()
        url = reverse('video-completion-list')
        response = self.client.post(url, data=self.generate_create_data(), format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.video_completion.user, self.user)
        self.assertNotIn('user', response.data)
        for key in ('id', 'video_id', 'current_time', 'updated_at'):
            self.assertIn(key, response.data)

    def test_post_video_completion_list_already_exists_ok(self):
        """
        Tests video completions list view POST request when there is already
        a video completion instance for this combination of user and video.
        (The existing instance will be updated rather than creating a new one.)
        
        Asserts:
            - 200 Ok status.
            - Object user is request user.
            - Object id is existing id.
            - Current time has been updated.
            - Absence of user field in response data.
            - Presence of all serializer fields in response data.
        """
        url = reverse('video-completion-list')
        data=self.generate_create_data()
        data.update({'current_time': data['current_time'] - 0.1})
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.video_completion.user, self.user)
        self.assertEqual(response.data['id'], self.video_completion.pk)
        self.assertEqual(response.data['current_time'], data['current_time'])
        self.assertNotIn('user', response.data)
        for key in ('id', 'video_id', 'current_time', 'updated_at'):
            self.assertIn(key, response.data)

    def test_post_video_completion_list_not_authenticated_unauthorized(self):
        """
        Tests video completions list view POST request.
        
        Asserts:
            - 401 Unauthorized status.
        """
        self.client.logout()
        url = reverse('video-completion-list')
        response = self.client.post(url, data=self.generate_create_data(), format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_put_video_completion_detail_ok(self):
        """
        Tests video completions detail view PUT request.
        
        Asserts:
            - 200 Ok status.
            - Absence of user field in response data.
            - Presence of all serializer fields in response data.
        """
        new_current_time = 3.21
        url = reverse('video-completion-detail', kwargs={'pk': self.video_completion.pk})
        response = self.client.put(url, data={'current_time': new_current_time}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn('user', response.data)
        for key in ('id', 'video_id', 'current_time', 'updated_at'):
            self.assertIn(key, response.data)

    def test_put_video_completion_foreign_not_found(self):
        """
        Tests video completions detail view PUT request for a foreign completion.
        
        Asserts:
            - 404 Not found status.
        """
        new_current_time = 3.21
        self.video_completion.user = self.different_user
        self.video_completion.save()
        url = reverse('video-completion-detail', kwargs={'pk': self.video_completion.pk})
        response = self.client.put(url, data={'current_time': new_current_time}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_video_completion_detail_ok(self):
        """
        Tests video completions detail view PATCH request.
        
        Asserts:
            - 200 Ok status.
            - Absence of user field in response data.
            - Presence of all serializer fields in response data.
        """
        new_current_time = 3.21
        url = reverse('video-completion-detail', kwargs={'pk': self.video_completion.pk})
        response = self.client.patch(url, data={'current_time': new_current_time}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn('user', response.data)
        for key in ('id', 'video_id', 'current_time', 'updated_at'):
            self.assertIn(key, response.data)

    def test_patch_video_completion_foreign_not_found(self):
        """
        Tests video completions detail view PATCH request for a foreign completion.
        
        Asserts:
            - 404 Not found status.
        """
        new_current_time = 3.21
        self.video_completion.user = self.different_user
        self.video_completion.save()
        url = reverse('video-completion-detail', kwargs={'pk': self.video_completion.pk})
        response = self.client.patch(url, data={'current_time': new_current_time}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)