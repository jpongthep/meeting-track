from django.urls import path
from django.views.generic import TemplateView

from . import views 

home = TemplateView.as_view(template_name='_base.html')

app_name = 'core'
urlpatterns = [
    path('', home, name='home'),
    
    path('meeting-list/', views.meeting_list, name='meeting-list'),
    path('command-list/', views.command_list, name='command-list'),
    
    path('export-meetings/', views.export_meetings, name='export-meetings'),
    
    path('committee-members-list/<command_id>/', views.committee_members_list, name='committee-members-list'),
] 

