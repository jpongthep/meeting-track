from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from apps.core.views import meeting_list, export_meetings, command_list

home = TemplateView.as_view(template_name='_base.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('nation/', include('apps.nation.urls')),
    path('', include('apps.core.urls')),
] 


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

