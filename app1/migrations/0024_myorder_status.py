# Generated by Django 2.2 on 2020-02-11 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0023_auto_20200211_1431'),
    ]

    operations = [
        migrations.AddField(
            model_name='myorder',
            name='status',
            field=models.CharField(default='Pending', max_length=30),
        ),
    ]
