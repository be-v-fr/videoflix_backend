import os
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from .models import EmailConfirmation, PasswordReset
from datetime import timedelta

os.environ.setdefault('FRONTEND_BASE_URL', 'http://localhost:4200/')

class AuthTests(APITestCase):
    """
    Base test setup class for creating test users, profiles, and authentication tokens.
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
            - Username of new user is "User" plus primary key.
            - Absence of username in response data.
            - Presence of required fields in response data.
        """
        data = {
            'email': 'seconduser@mail.com',
            'password': 'testPassword123',
        }
        url = reverse('signup')
        response = self.client.post(url, data, format='json')
        created_user = User.objects.get(email=response.data['email'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(created_user.username, 'User' + str(created_user.pk))
        self.assertNotIn('username', response.data)
        for key in ('token', 'email', 'user_id'):
            self.assertIn(key, response.data)
        
        
    def test_signup_passwords_email_exists_bad_request(self):
        """
        Tests signup with non-matching passwords.
        
        Asserts:
            - 400 Bad request status.
        """
        data = {
            'email': self.user.email,
            'password': 'testPassword123',
        }
        url = reverse('signup')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
class PasswordResetTests(APITestCase):
    def setUp(self):
        AuthTests.setUp(self)
        self.pw_reset_token = PasswordResetTokenGenerator().make_token(self.user)
        self.pw_reset_obj = PasswordReset.objects.create(user=self.user, token=self.pw_reset_token)
        
    def test_request_ok(self):
        """
        Tests successful password reset request, creating a new token and replacing an existing one.
        
        Asserts:
            - 200 OK status.
            - Previous PasswordReset instance (containing the token) was deleted.
        """
        data = {
            'email': self.user.email,
        }
        url = reverse('request-pw-reset')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(PasswordReset.objects.filter(user=self.user)), 1)
        
    def test_request_unregistered_email_ok(self):
        """
        Tests failing password reset request due to an unregistered email address.
        For security reasons, the 200 OK status is sent nonetheless.
        
        Asserts:
            - 200 OK status.
            - Length of PasswordReset queryset is the same as before, i.e. no PasswordReset object was created.
        """
        queryset_count_before = PasswordReset.objects.count()
        data = {
            'email': 'nonexisting_user@mail.com',
        }
        url = reverse('request-pw-reset')
        response = self.client.post(url, data, format='json')
        queryset_count_after = PasswordReset.objects.count()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(queryset_count_before, queryset_count_after)
        
    def test_request_invalid_email_bad_request(self):
        """
        Tests failing password reset request due to an invalid email address.
        
        Asserts:
            - 400 Bad request status.
            - "email" key is in response.
        """
        data = {
            'email': 'invalid@mail',
        }
        url = reverse('request-pw-reset')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_perform_reset_ok(self):
        """
        Tests successful password reset, using an existing token.
        
        Asserts:
            - 200 OK status.
            - PasswordReset instance (containing the token) was deleted.
        """
        data = {
            'token': self.pw_reset_token,
            'new_password': 'asd123asd123',
        }
        url = reverse('perform-pw-reset')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(PasswordReset.objects.filter(user=self.user)), 0)
        
    def test_perform_reset_invalid_token_bad_request(self):
        """
        Tests failing password reset, using an invalid token.
        
        Asserts:
            - 400 Bad request status.
            - "token" key is in response.
        """
        data = {
            'token': '123456789abcdefg',
            'new_password': 'asd123asd123',
        }
        url = reverse('perform-pw-reset')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('token', response.data)
        
    def test_perform_reset_expired_token_bad_request(self):
        """
        Tests failing password reset, using an expired token.
        
        Asserts:
            - 400 Bad request status.
            - "token" key is in response.
            - Token was deleted.
        """
        self.pw_reset_obj.created_at -= timedelta(hours=25)
        self.pw_reset_obj.save()
        data = {
            'token': self.pw_reset_token,
            'new_password': 'asd123asd123',
        }
        url = reverse('perform-pw-reset')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('token', response.data)
        self.assertEqual(len(PasswordReset.objects.filter(user=self.user)), 0)
        
    def test_perform_reset_weak_pw_bad_request(self):
        """
        Tests failing password reset, using an invalid password.
        
        Asserts:
            - 400 Bad request status.
            - "new_password" key is in response.
        """
        data = {
            'token': self.pw_reset_token,
            'new_password': 'asd123',
        }
        url = reverse('perform-pw-reset')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('new_password', response.data)