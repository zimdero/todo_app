from django.urls import path

from . import views

app_name = 'sign'
urlpatterns = [
    path('signup', views.signup, name='signup'),
]
