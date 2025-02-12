from django.db import models


class Config(models.Model):
    key = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name  = verbose_name_plural = 'Config'
        ordering = ['key', ]
    
    def __str__(self):
        return self.key