# Generated by Django 3.0.2 on 2020-03-19 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0037_orders_payment_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='transaction_id',
            field=models.CharField(default='CASH', max_length=100),
        ),
    ]
