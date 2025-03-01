from django.urls import path
from .views import MeetingListView

app_name = 'nation'
urlpatterns = [
    path('meetings/', MeetingListView.as_view(), name='meeting-list'),
]

