# Generated by Django 2.1.4 on 2018-12-21 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scan_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicantcv',
            name='Applicant_cv',
            field=models.FileField(upload_to=''),
        ),
    ]
