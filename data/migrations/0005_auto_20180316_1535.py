# Generated by Django 2.0.3 on 2018-03-16 15:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0004_auto_20180120_0027'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='softjob',
            options={'get_latest_by': '-create_time', 'ordering': ['-create_time']},
        ),
    ]
