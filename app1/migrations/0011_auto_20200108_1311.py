# Generated by Django 2.2 on 2020-01-08 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0010_cart_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='price',
            field=models.IntegerField(default=1),
        ),
    ]
