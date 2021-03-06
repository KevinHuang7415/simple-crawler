# Generated by Django 2.0.3 on 2018-03-16 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SoftJob',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=5)),
                ('author', models.CharField(max_length=35)),
                ('title', models.CharField(max_length=100)),
                ('url', models.URLField(max_length=65, unique=True)),
                ('content', models.TextField()),
                ('create_time', models.DateTimeField()),
                ('edit_time', models.DateTimeField()),
            ],
            options={
                'db_table': 'SoftJob',
                'ordering': ['-create_time'],
                'get_latest_by': '-create_time',
            },
        ),
    ]
