# Generated by Django 2.1.4 on 2018-12-22 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scan_app', '0004_applicantcollege_applicantdegree'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicantdegree',
            name='degree_rank',
            field=models.CharField(default=0, max_length=3),
            preserve_default=False,
        ),
    ]
