# Generated by Django 4.2.19 on 2025-02-12 09:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_remove_meeting_form_2_remove_meeting_report_sended_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='fiscalobjective',
            options={'ordering': ['fiscal_year'], 'verbose_name': '3. แผน/สรุปผลการประชุม', 'verbose_name_plural': '3. แผน/สรุปผลการประชุม'},
        ),
        migrations.AlterModelOptions(
            name='meeting',
            options={'ordering': ['meeting_date'], 'verbose_name': '4. รายละเอียดการประชุม', 'verbose_name_plural': '4. รายละเอียดการประชุม'},
        ),
        migrations.AddField(
            model_name='section',
            name='type',
            field=models.CharField(choices=[('M', 'หลัก'), ('S', 'สาขา')], default='M', max_length=1, verbose_name='ประเภท'),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meetings', to='core.department', verbose_name='จังหวัด'),
        ),
    ]
