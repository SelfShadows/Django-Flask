# Generated by Django 2.2.7 on 2019-12-17 06:04

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app02_ModelForm', '0002_auto_20191217_1327'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='email',
            field=models.EmailField(default='870670791@qq.com', max_length=254),
        ),
        migrations.AddField(
            model_name='book',
            name='date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
