# Generated by Django 2.2.7 on 2019-11-19 07:54

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0007_remove_persen_birthday'),
    ]

    operations = [
        migrations.AddField(
            model_name='persen',
            name='birthday',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
