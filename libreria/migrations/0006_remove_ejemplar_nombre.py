# Generated by Django 3.2.8 on 2022-06-13 22:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('libreria', '0005_articulo_imagen'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ejemplar',
            name='nombre',
        ),
    ]
