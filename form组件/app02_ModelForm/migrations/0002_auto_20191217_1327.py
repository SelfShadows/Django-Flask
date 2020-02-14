# Generated by Django 2.2.7 on 2019-12-17 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app02_ModelForm', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='book',
        ),
        migrations.AddField(
            model_name='book',
            name='author',
            field=models.ManyToManyField(to='app02_ModelForm.Author'),
        ),
    ]
