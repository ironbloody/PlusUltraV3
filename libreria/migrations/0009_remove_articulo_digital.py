# Generated by Django 3.2.8 on 2022-07-02 21:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('libreria', '0008_auto_20220702_2116'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='articulo',
            name='digital',
        ),
    ]
