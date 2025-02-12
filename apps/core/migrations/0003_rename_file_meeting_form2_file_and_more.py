# Generated by Django 4.2.19 on 2025-02-12 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_department_options_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='meeting',
            old_name='file',
            new_name='form2_file',
        ),
        migrations.RemoveField(
            model_name='meeting',
            name='report_send',
        ),
        migrations.AddField(
            model_name='meeting',
            name='form_2',
            field=models.BooleanField(default=False, verbose_name='แบบฟอร์ม กม.2'),
        ),
        migrations.AddField(
            model_name='meeting',
            name='report_file',
            field=models.FileField(blank=True, null=True, upload_to='meeting_files/'),
        ),
        migrations.AddField(
            model_name='meeting',
            name='report_sended',
            field=models.BooleanField(default=False, verbose_name='รายงานการประชุม'),
        ),
        migrations.AlterField(
            model_name='department',
            name='responsible',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='เลขา คปจ.'),
        ),
        migrations.AlterField(
            model_name='fiscalobjective',
            name='meeting_number',
            field=models.PositiveIntegerField(default=1, verbose_name='แผนการประชุม (ครั้ง)'),
        ),
    ]
