# Generated by Django 2.2.7 on 2019-12-17 04:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('price', models.DecimalField(decimal_places=2, default=99.99, max_digits=5)),
                ('title', models.CharField(max_length=64, unique=True)),
                ('publisher', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='books', to='app02_ModelForm.Publisher')),
            ],
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64)),
                ('book', models.ManyToManyField(to='app02_ModelForm.Book')),
            ],
        ),
    ]
