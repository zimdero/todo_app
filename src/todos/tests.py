from django.test import TestCase, Client
from django.urls import reverse
from django.utils.html import escape
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.forms.models import model_to_dict

from . import models

class TestTodo(TestCase):
    title = 'new todo'
    description = 'new description'
    due_time = datetime.now().date()
    priority = 1
    c = Client()
    index_url = reverse('todos:index')
    edit_url = reverse('todos:edit')

    def setUp(self):
        self.user = User.objects.create_user(
            username='username',
            password='secretlogitech'
        )

    def test_create_todo_without_user(self):
        todo = {
            'title': self.title,
            'description': self.description,
            'due_time': self.due_time,
            'priority': self.priority
        }

        resp = self.c.post(self.index_url, todo)
        self.assertIn('user', resp.context['form'].errors.keys())

    def test_create_todo_without_title(self):
        todo = {
            'user': self.user.id,
            'description': self.description,
            'due_time': self.due_time,
            'priority': self.priority
        }

        resp = self.c.post(self.index_url, todo)
        self.assertIn('title', resp.context['form'].errors.keys())

    def test_create_todo_without_description(self):
        todo = {
            'user': self.user.id,
            'title': self.title,
            'due_time': self.due_time,
            'priority': self.priority
        }

        resp = self.c.post(self.index_url, todo)
        self.assertIn('description', resp.context['form'].errors.keys())

    def test_create_todo_without_due_time(self):
        todo = {
            'user': self.user.id,
            'title': self.title,
            'description': self.description,
            'priority': self.priority
        }

        resp = self.c.post(self.index_url, todo)
        self.assertIn('due_time', resp.context['form'].errors.keys())

    def test_create_todo_without_priority(self):
        todo = {
            'user': self.user.id,
            'title': self.title,
            'description': self.description,
            'due_time': self.due_time,
        }

        resp = self.c.post(self.index_url, todo)
        self.assertIn('priority', resp.context['form'].errors.keys())


    def test_create_todo_with_due_time_in_past(self):
        yesterday = datetime.now() - timedelta(days=1)

        todo = {
            'user': self.user.id,
            'title': self.title,
            'description': self.description,
            'due_time': yesterday.date(),
            'priority': self.priority
        }

        resp = self.c.post(self.index_url, todo)
        self.assertIn('due_time', resp.context['form'].errors.keys())
        self.assertEqual(resp.context['form'].errors['due_time'][0],
                         'The due_time cannot be in the past!')


    def test_create_todo_with_wrong_priority(self):
        todo = {
            'user': self.user.id,
            'title': self.title,
            'description': self.description,
            'due_time': self.due_time,
            'priority': 4
        }

        resp = self.c.post(self.index_url, todo)
        self.assertFalse(resp.context['form'].is_valid())
        self.assertIn('priority', resp.context['form'].errors.keys())


    def test_edit_todo(self):
        todo = {
            'user': self.user,
            'title': self.title,
            'description': self.description,
            'due_time': self.due_time,
            'priority': self.priority
        }

        todo = models.Todo.objects.create(**todo)
        self.assertIs(todo.__class__, models.Todo)

        new_todo = model_to_dict(todo)
        new_todo['title'] = 'Edit title'

        login = self.c.login(
            username=self.user.username,
            password='secretlogitech')
        self.assertTrue(login)

        resp = self.c.post('{}/{}'.format(self.edit_url, todo.id), new_todo)

        updated_todo = models.Todo.objects.get(pk=todo.id)
        self.assertEqual(updated_todo.title, new_todo['title'])


    def test_delete_todo(self):
        todo = {
            'user': self.user,
            'title': self.title,
            'description': self.description,
            'due_time': self.due_time,
            'priority': self.priority
        }

        todo = models.Todo.objects.create(**todo)
        self.assertIs(todo.__class__, models.Todo)

        login = self.c.login(
            username=self.user.username,
            password='secretlogitech')
        self.assertTrue(login)

        resp = self.c.post(reverse('todos:delete', args=[todo.id]))

        self.assertEqual(0, len(models.Todo.objects.all()))

