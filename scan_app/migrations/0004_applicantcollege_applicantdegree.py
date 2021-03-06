# Generated by Django 2.1.4 on 2018-12-22 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scan_app', '0003_auto_20181221_1805'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApplicantCollege',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clg_name', models.CharField(max_length=100)),
                ('clg_rank', models.CharField(max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='ApplicantDegree',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('degree', models.CharField(max_length=100)),
            ],
        ),
    ]
