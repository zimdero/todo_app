from django.urls import path, re_path

from . import views

app_name = 'todos'
urlpatterns = [
    path('', views.index, name='index'),
    path('clean', views.clean, name='clean'),
    re_path('edit(?:/(?P<todo_id>\d+)/)?', views.edit, name='edit'),
    path('delete/<int:todo_id>', views.delete, name='delete'),
]
