# Generated by Django 2.2.7 on 2019-11-19 08:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0008_persen_birthday'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='persen',
            name='birthday',
        ),
    ]