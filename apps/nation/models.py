from datetime import date

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class NationMeeting(models.Model):
    fiscal_year = models.IntegerField(verbose_name="ปีงบประมาณ", default=2568)
    number = models.IntegerField(verbose_name="ครั้งที่", default= 1)
    name = models.CharField(verbose_name="ชื่อการประชุม", max_length=200)
    meeting_date = models.DateField(verbose_name="วันที่", blank=True, null=True)    
    picture = models.ImageField(verbose_name="รูปภาพ", upload_to='meeting_pictures/', blank=True, null=True)
    file = models.FileField(verbose_name="ไฟล์", upload_to='meeting_files/', blank=True, null=True)
    
    class Meta:
        verbose_name  = verbose_name_plural = '1. การประชุม.'
        ordering = ['-meeting_date', ]
    
    def __str__(self):
        return self.name
    

class Command(models.Model):    
    name = models.CharField(verbose_name="ชื่อคำสั่ง", max_length=200, blank=False, null=True)
    number = models.IntegerField(verbose_name="เลขที่คำสั่ง")
    fiscal_year = models.IntegerField(verbose_name="ปี", 
                                    validators=[MinValueValidator(2550, message="ปีต้องไม่ต่ำกว่า 2550"),
                                                MaxValueValidator(2580, message="ปีต้องไม่เกิน 2580"),], 
                                    default=(date.today().year+543))    
    date = models.DateField(verbose_name="ลงวันที่", blank=True, null=True)
    file = models.FileField(verbose_name="ไฟล์", upload_to='command_files/', blank=True, null=True)

    class Meta:
        verbose_name = verbose_name_plural = '2. คำสั่ง'
        ordering = ['-date']

    def __str__(self):
        return f"{self.number}/{self.fiscal_year%100} ลงวันที่ {self.date.day}-{self.date.month}-{self.date.year+543}"
    
    def year_number(self):
        return f"{self.number}/{self.fiscal_year%100}"
    year_number.short_description = 'เลขที่คำสั่ง'
    
