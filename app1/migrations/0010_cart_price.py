# Generated by Django 2.2 on 2020-01-07 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0009_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='price',
            field=models.IntegerField(default=0),
        ),
    ]
