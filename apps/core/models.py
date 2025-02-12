from django.db import models

from apps.configs.models import Config


class Section(models.Model):
    """
    Represents a section to which a Department belongs.
    """
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
    """
    Department model with additional contact and comment fields, plus a ForeignKey to Section.
    """
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
    """
    Fiscal Objective model with a ForeignKey to Department.
    """
    department = models.ForeignKey(Department, verbose_name = "จังหวัด", on_delete=models.CASCADE, related_name='fiscal_objectives')
    fiscal_year = models.IntegerField(verbose_name="ปีงบประมาณ", default=2568)
    meeting_number = models.PositiveIntegerField(verbose_name="แผนการประชุม (ครั้ง)",default=1)

    class Meta:
        verbose_name  = verbose_name_plural = '3. แผน/สรุปผลการประชุม'
        ordering = ['fiscal_year', ]
            
    def __str__(self):
        return f"{self.department.province} - {self.fiscal_year}"



class Meeting(models.Model):
    """
    Meeting model with updated meeting date fields and a status field.
    """
    department = models.ForeignKey(Department, verbose_name = "จังหวัด", on_delete=models.CASCADE, related_name='meetings')
    fiscal_year = models.IntegerField(verbose_name="ปีงบประมาณ", default=2568)
    number = models.IntegerField(verbose_name="ครั้งที่", default= 1)
    meeting_date = models.DateField(blank=True, null=True)        
    
    picture = models.ImageField(verbose_name="รูปภาพ", upload_to='meeting_pictures/', blank=True, null=True)
   
    form2_file = models.FileField(verbose_name="ไฟล์ กม.2", upload_to='meeting_files/', blank=True, null=True)
    report_file = models.FileField(verbose_name="ไฟล์รายงานการประชุม", upload_to='meeting_files/', blank=True, null=True)
    
    summary = models.TextField()
    
    STATUS_CHOICES = [
        ('P', 'แผน'),
        ('D', 'ดำเนินการแล้ว'),
        ('A', 'ตรวจสอบแล้ว'),
    ]
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    
    class Meta:
        verbose_name  = verbose_name_plural = '4. รายละเอียดการประชุม'
        ordering = ['meeting_date', ]
    
    def __str__(self):
        return f"{self.department.province} - {self.fiscal_year%100}-{self.number}"
    

    
