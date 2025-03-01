from django.views.generic import ListView
from django.utils.timezone import localtime
from .models import NationMeeting, Command

class MeetingListView(ListView):
    model = NationMeeting
    template_name = 'nation/meeting_list.html'
    context_object_name = 'meetings'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['commands'] = Command.objects.all()
        return context
