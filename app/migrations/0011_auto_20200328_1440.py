# Generated by Django 3.0.4 on 2020-03-28 09:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_auto_20200311_1536'),
    ]

    operations = [
        migrations.CreateModel(
            name='CanteenProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('canteen_rating', models.CharField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default='Not Assigned', max_length=20)),
                ('status', models.CharField(choices=[('Block', 'Block'), ('Active', 'Active')], default='Active', max_length=20)),
                ('canteen', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Canteen',
        ),
    ]
