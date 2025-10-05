from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class AuthTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('blog:register')
        self.login_url = reverse('blog:login')
        self.profile_url = reverse('blog:profile')
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'ComplexPass123',
            'password2': 'ComplexPass123'
        }

    def test_register_creates_user_and_redirects(self):
        resp = self.client.post(self.register_url, data=self.user_data)
        self.assertEqual(resp.status_code, 302)  # redirect to profile
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_profile_requires_login(self):
        resp = self.client.get(self.profile_url)
        self.assertEqual(resp.status_code, 302)  # redirect to login
        # login then access
        User.objects.create_user(username='u', email='u@test.com', password='p')
        self.client.login(username='u', password='p')
        resp2 = self.client.get(self.profile_url)
        self.assertEqual(resp2.status_code, 200)
