# Generated by Django 2.2.5 on 2019-10-15 07:04

import app01.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0012_auto_20191015_1501'),
    ]

    operations = [
        migrations.CreateModel(
            name='PersonDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('addr', models.CharField(max_length=128)),
                ('phone', models.CharField(default='19983491093', max_length=11)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('hobby', app01.models.FixedCharField(default='羽毛球', max_length=64)),
                ('birthday', models.DateField(auto_now_add=True)),
                ('detail', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app01.PersonDetail')),
            ],
        ),
    ]
