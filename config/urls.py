from django.contrib import admin
from django.urls import path

from apps.core.views import summary

urlpatterns = [
    path('admin/', admin.site.urls),
    path('summary/<year>/', summary, name='summary'),
]
