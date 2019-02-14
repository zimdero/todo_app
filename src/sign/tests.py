from django.test import TestCase, Client
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from django.utils.html import escape

from django.contrib.auth.models import User

from . import models

class TestUserCreationForm(TestCase):
    username = 'username'
    password1 = 'secretlogitech'
    password2 = 'secretlogitech'
    c = Client()
    register_url = reverse('sign:signup')
    login_url = reverse('login')

    def test_register_without_username(self):
        user = {
            'password1': self.password1,
            'password2': self.password2
        }
        resp = self.c.post(self.register_url, user)
        self.assertFalse(resp.context['form'].is_valid())
        self.assertEqual(1, len(resp.context['form'].errors))
        self.assertIn('username', resp.context['form'].errors.keys())

    def test_register_wrong_password(self):
        user = {
            'username': self.username,
            'password1': self.password1,
            'password2': 'logitechsecret'
        }

        resp = self.c.post(self.register_url, user)
        self.assertFalse(resp.context['form'].is_valid())
        self.assertIn('password2', resp.context['form'].errors.keys())
        self.assertEqual(1, len(resp.context['form'].errors.keys()))


    def test_register_with_escape(self):
        user = {
            'username': '<script>Alert(\'hello\')</script>',
            'password1': self.password1,
            'password2': self.password2
        }

        form_data = {k:escape(v) for (k,v) in user.items()}
        form = UserCreationForm(form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.data['username'], '&lt;script&gt;Alert(&#39;hello&#39;)&lt;/script&gt;')


    def test_register_and_login(self):
        user = {
            'username': self.username,
            'password1': self.password1,
            'password2': self.password2
        }

        form = UserCreationForm(user)
        self.assertTrue(form.is_valid())
        user_obj = form.save()
        self.assertEqual('username', user_obj.username)

        login = self.c.login(
                username=user['username'],
                password=user['password1'])
        self.assertTrue(login)
