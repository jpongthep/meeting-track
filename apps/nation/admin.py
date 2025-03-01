from django.contrib import admin
from .models import NationMeeting, Command

@admin.register(NationMeeting)
class NationMeetingAdmin(admin.ModelAdmin):
    list_display = ('fiscal_year', 'number', 'name', 'meeting_date')
    list_display_links = ('name', )
    list_filter = ('fiscal_year', 'meeting_date')
    search_fields = ('name',)
    ordering = ('-meeting_date',)
    save_as = True

@admin.register(Command)
class CommandAdmin(admin.ModelAdmin):
    list_display = ('year_number', 'name', 'date')
    list_display_links = ('year_number', 'name', )
    list_filter = ('fiscal_year',)
    search_fields = ('name', 'number')
    ordering = ('-fiscal_year', 'number')
