# Generated by Django 2.2.7 on 2019-12-25 13:47

import app01.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64, verbose_name='姓名')),
                ('sex', models.IntegerField(choices=[(1, '男'), (2, '女')], verbose_name='性别')),
            ],
        ),
        migrations.CreateModel(
            name='PersonDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('addr', models.CharField(max_length=128)),
                ('phone', models.CharField(default='19983491093', max_length=11)),
            ],
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64, unique=True)),
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
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64, unique=True, verbose_name='书名')),
                ('price', models.DecimalField(decimal_places=2, default=99.99, max_digits=5)),
                ('kucun', models.IntegerField(default=1000, verbose_name='库存')),
                ('maichu', models.IntegerField(default=10, verbose_name='卖出')),
                ('author', models.ManyToManyField(to='app01.Author')),
                ('publisher', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='books', to='app01.Publisher')),
            ],
        ),
    ]
