# Generated by Django 3.0 on 2020-01-21 09:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app1', '0016_menu_canteen'),
    ]

    operations = [
        migrations.CreateModel(
            name='Myorder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('canteen_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cant', to=settings.AUTH_USER_MODEL)),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cust', to=settings.AUTH_USER_MODEL)),
                ('menu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.Menu')),
                ('quant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='qty', to='app1.Cart')),
                ('time', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tym', to='app1.Cart')),
            ],
        ),
    ]