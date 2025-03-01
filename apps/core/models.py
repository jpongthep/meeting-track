from datetime import date

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from apps.configs.models import Config


class Section(models.Model):
    name = models.CharField(verbose_name="สำนัก", max_length=100)
    number = models.IntegerField(verbose_name="ลำดับที่",)
    type = models.CharField(verbose_name="ประเภท", max_length=1, choices=[('M', 'หลัก'), ('S', 'สาขา')], default='M')
    # province = models.CharField(verbose_name="จังหวัด", max_length=100)
    description = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name  = verbose_name_plural = '1. สำนัก'
        ordering = ['type', 'number', ]
    
    def __str__(self):
        return self.name
    
    def sub_departments(self):
        return self.departments.all().count()
    sub_departments.short_description = 'จำนวนหน่วยงาน'
    

class Department(models.Model):
    section = models.ForeignKey(Section, verbose_name="สำนัก",  on_delete=models.CASCADE, related_name='departments')
    
    province = models.CharField(verbose_name="จังหวัด", max_length=100)    
    responsible = models.CharField(verbose_name="เลขา คปจ.", max_length=100, blank=True, null=True)
    contact_name = models.CharField(verbose_name="ผู้ติดต่อ", max_length=100, blank=True, null=True)
    phone = models.CharField(verbose_name="เบอร์โทร", max_length=20, blank=True, null=True)
    comment = models.TextField(verbose_name="หมายเหตุ", blank=True, null=True)

    class Meta:
        verbose_name  = verbose_name_plural = '2. หน่วยงาน'
        ordering = ['section__number', ]
            
    def __str__(self):
        return self.province
    
    def get_current_fiscal_objective(self):
        year = int(Config.objects.get(key = "fiscal-year").value)
        return self.fiscal_objectives.filter(fiscal_year=year).first()
    
    def get_fiscal_meeting(self):
        year = int(Config.objects.get(key = "fiscal-year").value)
        return self.meetings.filter(fiscal_year=year).all()
    

class FiscalObjective(models.Model):
    department = models.ForeignKey(Department, verbose_name = "จังหวัด", on_delete=models.CASCADE, related_name='fiscal_objectives')
    fiscal_year = models.IntegerField(verbose_name="ปีงบประมาณ", default=2568)
    meeting_number = models.PositiveIntegerField(verbose_name="แผนการประชุม (ครั้ง)",default=1)

    class Meta:
        verbose_name  = verbose_name_plural = '3. แผน/สรุปผลการประชุม'
        ordering = ['fiscal_year', ]
            
    def __str__(self):
        return f"{self.department.province} - {self.fiscal_year}"

    

class Meeting(models.Model):
    department = models.ForeignKey(Department, verbose_name = "จังหวัด", on_delete=models.CASCADE, related_name='meetings')
    fiscal_year = models.IntegerField(verbose_name="ปีงบประมาณ", default=2568)
    number = models.IntegerField(verbose_name="ครั้งที่", default= 1)
    meeting_date = models.DateField(blank=True, null=True)        
    
    picture = models.ImageField(verbose_name="รูปภาพ", upload_to='meeting_pictures/', blank=True, null=True)
   
    form2_file = models.FileField(verbose_name="ไฟล์ กม.2", upload_to='meeting_files/', blank=True, null=True)
    report_file = models.FileField(verbose_name="ไฟล์รายงานการประชุม", upload_to='meeting_files/', blank=True, null=True)
    
    summary = models.TextField()
    
    STATUS_CHOICES = [
        ('P', 'ยังไม่ดำเนินการ'),
        ('A', 'ดำเนินการแล้ว'),
    ]
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    
    class Meta:
        verbose_name  = verbose_name_plural = '4. รายละเอียดการประชุม'
        ordering = ['fiscal_year', 'meeting_date', ]
    
    def __str__(self):
        return f"{self.department.province} - {self.fiscal_year%100}-{self.number}"

    def get_plan(self):
        try:
            return FiscalObjective.objects.filter(department=self.department, fiscal_year=self.fiscal_year).first().meeting_number
        except:
            return "-"
    

class Command(models.Model):
    department = models.ForeignKey(Department, verbose_name="จังหวัด", on_delete=models.CASCADE, related_name='commands')
    name = models.CharField(verbose_name="ชื่อคำสั่ง", max_length=200, blank=False, null=True)
    number = models.IntegerField(verbose_name="เลขที่คำสั่ง")
    year = models.IntegerField(verbose_name="ปี", 
                                    validators=[MinValueValidator(2550, message="ปีต้องไม่ต่ำกว่า 2550"),
                                                MaxValueValidator(2580, message="ปีต้องไม่เกิน 2580"),], 
                                    default=(date.today().year+543))
    assignment_date = models.DateField(verbose_name="ลงวันที่", blank=True, null=True)
    expiration_date = models.DateField(verbose_name="วันที่ครบวาระ", blank=True, null=True)
    file = models.FileField(verbose_name="ไฟล์", upload_to='command_files/', blank=True, null=True)

    class Meta:
        verbose_name = verbose_name_plural = '5. คำสั่ง'
        ordering = ['year', 'number']

    def __str__(self):
        return f"{self.number}/{self.year%100} ลงวันที่ {self.assignment_date.day}-{self.assignment_date.month}-{self.assignment_date.year+543}"
    
    def year_number(self):
        return f"{self.number}/{self.year%100}"


class CommitteeMember(models.Model):
    ACTIVE_STATUS_CHOICES = [
        ('A', 'Active'),
        ('E', 'Expired'),
    ]
    command = models.ForeignKey(Command, verbose_name="คำสั่ง", on_delete=models.CASCADE, related_name='committee_members')
    full_name = models.CharField(verbose_name="ชื่อ-สกุล", max_length=120)
    position = models.CharField(verbose_name="ตำแหน่ง", max_length=150)
    status = models.CharField(verbose_name="สถานะ", max_length=10, choices=ACTIVE_STATUS_CHOICES, default='active')
    comment = models.TextField(verbose_name="หมายเหตุ", blank=True, null=True)

    objects = models.Manager()
    
    class Meta:
        verbose_name = verbose_name_plural = '6. กรรมการ'
        ordering = ['command__year', 'command__number', 'full_name']

    def __str__(self):
        return f"{self.full_name} - {self.position}"