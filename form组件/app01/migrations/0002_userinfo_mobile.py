# Generated by Django 2.2.7 on 2019-11-23 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='mobile',
            field=models.CharField(max_length=11, null=True),
        ),
    ]
