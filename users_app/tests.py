from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token

class AuthTests(APITestCase):
    """
    Base test setup class for creating test users, profiles, and tokens.
    """    
    def setUp(self):
        """
        Creates a customer and business user, with associated profiles and authentication tokens.
        """
        self.user = User.objects.create_user(username='testuser', email='testemail@email.com', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        
    def test_login_ok(self):
        """
        Tests successful login with correct credentials.
        
        Asserts:
            - 200 OK status.
            - Absence of username in response data.
            - Presence of required fields in response data.
        """
        data = {
            'email': self.user.email,
            'password': 'testpassword',
        }
        url = reverse('login')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn('username', response.data)
        for key in ('token', 'email', 'user_id'):
            self.assertIn(key, response.data)
        
    def test_login_false_password_bad_request(self):
        """
        Tests login with incorrect password.
        
        Asserts:
            400 Bad Request status.
        """
        data = {
            'email': self.user.email,
            'password': 'wrongpassword',
        }
        url = reverse('login')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_login_not_registered_bad_request(self):
        """
        Tests login with incorrect password.
        
        Asserts:
            400 Bad Request status.
        """
        data = {
            'email': 'doesnotexist@mail.com',
            'password': 'randompassword',
        }
        url = reverse('login')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_signup_ok(self):
        """
        Tests successful signup with valid credentials.
        
        Asserts:
            - 201 Created status.
            - Absence of username in response data.
            - Presence of required fields in response data.
        """
        data = {
            'email': 'seconduser@mail.com',
            'password': 'testPassword123',
            'repeated_password': 'testPassword123',
        }
        url = reverse('signup')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotIn('username', response.data)
        for key in ('token', 'email', 'user_id'):
            self.assertIn(key, response.data)
            
    def test_signup_passwords_do_not_match_bad_request(self):
        """
        Tests signup with non-matching passwords.
        
        Asserts:
            - 400 Bad request status.
        """
        data = {
            'email': 'seconduser@mail.com',
            'password': 'testPassword123',
            'repeated_password': 'testPassword124',
        }
        url = reverse('signup')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_signup_passwords_email_exists_bad_request(self):
        """
        Tests signup with non-matching passwords.
        
        Asserts:
            - 400 Bad request status.
        """
        data = {
            'email': self.user.email,
            'password': 'testPassword123',
            'repeated_password': 'testPassword123',
        }
        url = reverse('signup')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)