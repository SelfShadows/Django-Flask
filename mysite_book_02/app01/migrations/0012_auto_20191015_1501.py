# Generated by Django 2.2.5 on 2019-10-15 07:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0011_persondetail'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Person',
        ),
        migrations.DeleteModel(
            name='PersonDetail',
        ),
    ]