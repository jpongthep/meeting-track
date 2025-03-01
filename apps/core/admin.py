from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.templatetags.static import static
from django.db.models import Q

from .models import Section, Department, FiscalObjective, Meeting, Command, CommitteeMember


admin.site.site_header = "Organization Meeting Tracker Admin"
admin.site.site_title = "Meeting Tracker"
admin.site.index_title = "Manage Meetings and Departments"


class DepartmentInline(admin.TabularInline):
    model = Department
    fields = ('province', 'responsible', 'contact_name', 'phone')
    extra = 0

class MainSubFilter(admin.SimpleListFilter):
    title = 'หลัก/สาขา'
    parameter_name = 'name_contains_sakha'

    def lookups(self, request, model_admin):
        return (
            ('main', 'หลัก'),
            ('sub', 'สาขา'),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'sub':
            return queryset.filter(name__contains='สาขา')
        if value == 'main':
            return queryset.exclude(name__contains='สาขา')
        return queryset


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('name','type', 'sub_departments', )
    list_display_links = ('name',)
    list_editable = ('type',)
    search_fields = ('name', )    
    inlines = [DepartmentInline,]
    list_filter = (MainSubFilter,)
    ordering = ['number',]


class MainSubSectionFilter(admin.SimpleListFilter):
    title = 'หลัก/สาขา'
    parameter_name = 'name_contains_sakha'

    def lookups(self, request, model_admin):
        return (
            ('main', 'หลัก'),
            ('sub', 'สาขา'),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'sub':
            return queryset.filter(section__name__contains='สาขา')
        if value == 'main':
            return queryset.exclude(section__name__contains='สาขา')
        return queryset


class CommandInline(admin.TabularInline):
    model = Command
    fields = ('name', 'number', 'year', 'assignment_date', 'expiration_date', 'num_committee_members')
    readonly_fields = ('num_committee_members',)
    extra = 0
    
    def num_committee_members(self, obj):
        url = reverse("admin:core_command_change", args=[obj.id])
        param = "?q={}".format(obj.department.province)
        return format_html('<a href="{}" title="Edit" target="_blank" class="button">👥 กรรมการ {}</a>', url + param, obj.committee_members.count())

    num_committee_members.short_description = 'จำนวนกรรมการ'
    
    
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'section', 'province', 'responsible', 'num_commands',)
    list_display_links = ('__str__', 'section')
    search_fields = ('section__name', 'province', 'responsible',)
    list_filter = (MainSubSectionFilter, 'section__number',)
    inlines = [CommandInline]
    raw_id_fields = ('section',)
    
    def num_commands(self, obj):
        return obj.commands.count()
    num_commands.short_description = 'จำนวนคำสั่ง'


@admin.register(FiscalObjective)
class FiscalObjectiveAdmin(admin.ModelAdmin):
    list_display = ('fiscal_year', 'department_section_number',  'department', 'meeting_number', 'num_planing', 'num_done', 'num_approved', 'detail',)
    list_display_links = ('fiscal_year', 'department',)
    list_editable = ('meeting_number',)
    raw_id_fields = ('department',)
    search_fields = ('department__province',)
    list_filter = ('fiscal_year', 'department__section__type')
    actions = ['create_meetings_action']
    save_as = True
    
    def department_section_number(self, obj):
        return obj.department.section.number
    department_section_number.short_description = 'หลัก/สาขา'
    department_section_number.admin_order_field = 'department__section__number'

    def detail(self, obj):        
        url = reverse("admin:core_meeting_changelist")        
        param = "?fiscal_year={}&q={}".format(obj.fiscal_year, obj.department.province)
        
        svg_icon = format_html("""
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" style="width:16px;height:16px;">
                <path d="M8.00008 6V9H5.00008V6H8.00008ZM3.00008 4V11H10.0001V4H3.00008ZM13.0001 4H21.0001V6H13.0001V4ZM13.0001 11H21.0001V13H13.0001V11ZM13.0001 18H21.0001V20H13.0001V18ZM10.7072 16.2071L9.29297 14.7929L6.00008 18.0858L4.20718 16.2929L2.79297 17.7071L6.00008 20.9142L10.7072 16.2071Z"></path>
            </svg>
        """)        
        return format_html('<a href="{}" title="Edit" target="_blank">{}</a>', url + param, svg_icon)   
     
    detail.short_description = 'แจกแจง'

    def num_planing(self, obj):
        return obj.department.meetings.filter(Q(fiscal_year = obj.fiscal_year) & Q(status='P')).count()
    num_planing.short_description = 'แผน'
    
    def num_done(self, obj):
        return obj.department.meetings.filter(Q(fiscal_year = obj.fiscal_year) & Q(status='D')).count()
    num_done.short_description = 'ดำเนินการ'
    
    def num_approved(self, obj):
        return obj.department.meetings.filter(Q(fiscal_year = obj.fiscal_year) & Q(status='A')).count()    
    num_approved.short_description = 'ตจรวจสอบแล้ว'

    def create_meetings_action(self, request, queryset):
        created_count = 0
        updated_count = 0

        for fiscal_obj in queryset:
            for i in range(1, fiscal_obj.meeting_number + 1):
                meeting, created = Meeting.objects.update_or_create(
                    department=fiscal_obj.department,
                    fiscal_year=fiscal_obj.fiscal_year,
                    number=i,  
                    defaults={
                        "summary": f"Auto generated meeting record {i}/{fiscal_obj.meeting_number}.",
                    },
                )
                if created:
                    created_count += 1
                else:
                    updated_count += 1
        self.message_user(request, f"Created {created_count} meeting record(s), updated {updated_count} record(s).")
    create_meetings_action.short_description = "สร้างการประชุม"    
    
    
@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ('fiscal_year', 'number', 'department',   'meeting_date', 'status', 'is_send_form2', 'is_send_report')
    list_display_links = ('fiscal_year', 'number', 'department')
    list_editable = ('meeting_date', 'status')
    search_fields = ('department__province',)
    list_filter = ('fiscal_year', 'status', )
    raw_id_fields = ('department',)
    date_hierarchy = 'meeting_date'
    save_as = True
    
    fieldsets = (
        ('ข้อมูลการประชุม', {
            'fields': ('department', 'fiscal_year', ('number', 'meeting_date'), 'status', 'summary')
        }),
        ('เอกสารการประชุม', {
            'fields': ('form2_file', 'report_file')
        }),
    )
        
    def is_send_form2(self, obj):
        if obj.form2_file:
            file_name = obj.form2_file.name.split("/")[-1]
            return format_html('<a href="{}" target="_blank" title="{}">📄 เปิดไฟล์</a>', obj.form2_file.url,file_name)
        return "❌ no file"
    is_send_form2.allow_tags = True
    is_send_form2.short_description = 'ส่งไฟล์ กม.2'

    def is_send_report(self, obj):
        if obj.report_file:
            file_name = obj.report_file.name.split("/")[-1]
            return format_html('<a href="{}" target="_blank" title="{}">📄 เปิดไฟล์</a>', obj.report_file.url,file_name)
        return "❌ no file"
    is_send_report.allow_tags = True   
    is_send_report.short_description = 'รายงานการประชุม'
    

from django.contrib import admin
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import Command, CommitteeMember
from datetime import date

class CommiteeInline(admin.TabularInline):
    model = CommitteeMember
    fields = ('full_name', 'position', 'status',)
    extra = 0


@admin.register(Command)
class CommandAdmin(admin.ModelAdmin):
    list_display = ('department','name', 'number', 'year',  'assignment_date', 'expiration_date')
    list_display_links = ('department', 'name')
    list_filter = ('department', 'year')
    search_fields = ('name', 'department__province')
    date_hierarchy = 'assignment_date'
    ordering = ('year', 'number')
    save_as = True
    inlines = [CommiteeInline]
    raw_id_fields = ('department',)
    
    def has_delete_permission(self, request, obj=None):
        return False

    # fieldsets = (
    #     (None, {
    #         'fields': ('department', 'name', 'number', 'year', 'assignment_date', 'expiration_date', 'file')
    #     }),
    # )

    # def get_form(self, request, obj=None, **kwargs):
    #     form = super().get_form(request, obj, **kwargs)
    #     form.base_fields['year'].validators = [
    #         MinValueValidator(2550, message="ปีต้องไม่ต่ำกว่า 2550"),
    #         MaxValueValidator(2580, message="ปีต้องไม่เกิน 2580"),
    #     ]
    #     form.base_fields['year'].initial = date.today().year + 543
    #     return form

@admin.register(CommitteeMember)
class CommitteeMemberAdmin(admin.ModelAdmin):
    list_display = ('command', 'full_name', 'position', 'status')
    list_display_links = ('full_name',)
    list_filter = ('status',)
    search_fields = ('full_name', 'command__department__province',)
    ordering = ('command__year', 'command__number', 'full_name')
    raw_id_fields = ('command',)

    # fieldsets = (
    #     (None, {
    #         'fields': ('command', 'full_name', 'position', 'status', 'comment')
    #     }),
    # )