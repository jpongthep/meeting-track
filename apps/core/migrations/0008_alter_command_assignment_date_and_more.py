# Generated by Django 4.2.19 on 2025-03-01 02:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_command_assignment_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='command',
            name='assignment_date',
            field=models.DateField(blank=True, null=True, verbose_name='ลงวันที่'),
        ),
        migrations.AlterField(
            model_name='command',
            name='expiration_date',
            field=models.DateField(blank=True, null=True, verbose_name='วันที่ครบวาระ'),
        ),
    ]
