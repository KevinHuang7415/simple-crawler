# Generated by Django 2.0.1 on 2018-01-20 00:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0003_auto_20180119_0101'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='softjob',
            name='length',
        ),
    ]
