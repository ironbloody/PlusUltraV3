# Generated by Django 3.2.8 on 2022-07-03 03:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libreria', '0009_remove_articulo_digital'),
    ]

    operations = [
        migrations.AddField(
            model_name='articulo',
            name='presencial',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]