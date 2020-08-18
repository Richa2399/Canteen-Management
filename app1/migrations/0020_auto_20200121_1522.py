# Generated by Django 3.0 on 2020-01-21 09:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app1', '0019_auto_20200121_1517'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='canteen',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cantee', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='cart',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='custom', to=settings.AUTH_USER_MODEL),
        ),
    ]
