# Generated by Django 2.2.5 on 2019-10-12 07:25

import app01.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0006_person'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='hobby',
            field=app01.models.FixedCharField(default='羽毛球', max_length=64),
        ),
    ]
