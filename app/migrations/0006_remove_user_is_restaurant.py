# Generated by Django 2.2 on 2019-12-21 08:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20191218_1510'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_restaurant',
        ),
    ]
