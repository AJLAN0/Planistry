from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from django.core import mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .models import UserPreferences

User = get_user_model()

class UserAuthenticationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = '/api/users/register/'
        self.login_url = '/api/users/login/'
        self.logout_url = '/api/users/logout/'
        self.test_user_data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'testpass123',
            'password2': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User'
        }
        
        # Create a test user
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )

    def test_user_registration(self):
        test_data = {
            'email': 'newuser@example.com',
            'username': 'newuser',
            'password': 'testpass123',
            'password2': 'testpass123',
            'first_name': 'New',
            'last_name': 'User'
        }
        response = self.client.post(self.register_url, test_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email='newuser@example.com').exists())
        self.assertTrue(UserPreferences.objects.filter(user__email='newuser@example.com').exists())

    def test_user_registration_invalid_data(self):
        invalid_data = self.test_user_data.copy()
        invalid_data['password2'] = 'differentpass'
        response = self.client.post(self.register_url, invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login(self):
        login_data = {
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data['data'])
        self.assertIn('access', response.data['data'])
        self.assertIn('user', response.data['data'])

    def test_user_login_invalid_credentials(self):
        login_data = {
            'email': 'wrong@example.com',
            'password': 'wrongpass'
        }
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_logout(self):
        # First login to get the token
        login_data = {
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        login_response = self.client.post(self.login_url, login_data)
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        token = login_response.data['data']['token']
        access = login_response.data['data']['access']

        # Then logout using both tokens
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')
        response = self.client.post(self.logout_url, {'refresh': token})
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)

class UserProfileTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )
        self.profile_url = '/api/users/profile/'
        self.profile_update_url = '/api/users/profile/update/'
        self.preferences_url = '/api/users/preferences/'
        self.preferences_update_url = '/api/users/preferences/update/'

    def test_get_user_profile(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['email'], 'test@example.com')

    def test_update_user_profile(self):
        self.client.force_authenticate(user=self.user)
        update_data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'bio': 'New bio'
        }
        response = self.client.put(self.profile_update_url, update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')

    def test_get_user_preferences(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.preferences_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('daily_study_goal', response.data['data'])

    def test_update_user_preferences(self):
        self.client.force_authenticate(user=self.user)
        update_data = {
            'daily_study_goal': 180,
            'weekly_study_goal': 900,
            'preferred_study_duration': 60,
            'preferred_break_duration': 20,
            'reminder_frequency': 'daily',
            'study_reminders_enabled': True,
            'deadline_reminders_enabled': True,
            'assessment_reminders_enabled': True
        }
        response = self.client.put(self.preferences_update_url, update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        preferences = UserPreferences.objects.get(user=self.user)
        self.assertEqual(preferences.daily_study_goal, 180)

class PasswordResetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )
        self.password_reset_request_url = '/api/users/password-reset/'
        self.password_reset_confirm_url = '/api/users/password-reset-confirm/{uid}/{token}/'

    def test_password_reset_request(self):
        response = self.client.post(self.password_reset_request_url, {'email': 'test@example.com'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ['test@example.com'])

    def test_password_reset_confirm(self):
        # Generate token and uid
        token = PasswordResetTokenGenerator().make_token(self.user)
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        
        # Confirm password reset
        confirm_data = {
            'password': 'newpass123',
            'password2': 'newpass123'
        }
        url = self.password_reset_confirm_url.format(uid=uid, token=token)
        response = self.client.post(url, confirm_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Refresh user instance from database
        self.user.refresh_from_db()
        
        # Verify new password works
        self.assertTrue(self.user.check_password('newpass123'))

    def test_password_reset_invalid_token(self):
        # Use a valid UID but invalid token
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        url = self.password_reset_confirm_url.format(uid=uid, token='invalid-token')
        response = self.client.post(url, {
            'password': 'newpass123',
            'password2': 'newpass123'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(self.user.check_password('newpass123'))

class TestEmailTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.test_email_url = '/api/users/test-email/'

    def test_send_test_email(self):
        response = self.client.get(self.test_email_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ['aj0ly.hd@gmail.com'])
