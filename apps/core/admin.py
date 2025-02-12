from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.templatetags.static import static
from django.db.models import Q

from .models import Section, Department, FiscalObjective, Meeting


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
    
    
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'section', 'province', 'responsible', 'contact_name', 'phone')
    list_display_links = ('__str__', 'section')
    search_fields = ('section__name', 'province', 'responsible', 'contact_name', 'phone')
    list_filter = (MainSubSectionFilter, 'section__number',)


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