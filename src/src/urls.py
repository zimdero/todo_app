from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('sign.urls', namespace='sign')),
    path('auth/', include('django.contrib.auth.urls')),
    path('', include('todos.urls', namespace='todos')),
]
