# Generated by Django 2.2 on 2020-03-04 09:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0033_menu_no_of_rating'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredients',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ingredient_name', models.CharField(max_length=20)),
                ('ingredient_quantity', models.FloatField()),
                ('food', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.Menu')),
            ],
        ),
    ]
