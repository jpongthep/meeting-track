from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from apps.core.views import summary, export_meetings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', summary, name='summary'),
    path('export-meetings/', export_meetings, name='export-meetings'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

