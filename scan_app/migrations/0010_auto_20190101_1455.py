# Generated by Django 2.1.4 on 2019-01-01 09:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scan_app', '0009_applicantcollege_new_applicantdegree_new'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ApplicantCollege_New',
        ),
        migrations.DeleteModel(
            name='ApplicantDegree_New',
        ),
    ]
