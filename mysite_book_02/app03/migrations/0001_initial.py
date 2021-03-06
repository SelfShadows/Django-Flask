# Generated by Django 2.2.5 on 2019-10-15 08:14

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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('price', models.DecimalField(decimal_places=2, default=99.99, max_digits=5)),
            ],
        ),
        migrations.CreateModel(
            name='AuthorBook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app03.Author')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app03.Book')),
            ],
            options={
                'unique_together': {('author', 'book')},
            },
        ),
        migrations.AddField(
            model_name='author',
            name='books',
            field=models.ManyToManyField(through='app03.AuthorBook', to='app03.Book'),
        ),
    ]
