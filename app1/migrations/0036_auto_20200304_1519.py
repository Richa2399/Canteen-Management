# Generated by Django 2.2 on 2020-03-04 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0035_ingredients_brand'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredients',
            name='ingredient_quantity',
            field=models.CharField(max_length=20),
        ),
    ]
