# Generated by Django 2.2.7 on 2019-11-19 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0003_persen_birthday'),
    ]

    operations = [
        migrations.AlterField(
            model_name='persen',
            name='birthday',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
