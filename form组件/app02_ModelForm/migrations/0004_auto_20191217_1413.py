# Generated by Django 2.2.7 on 2019-12-17 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app02_ModelForm', '0003_auto_20191217_1404'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
