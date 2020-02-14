# Generated by Django 2.2.7 on 2019-12-05 05:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'verbose_name': '文章', 'verbose_name_plural': '文章'},
        ),
        migrations.AlterModelOptions(
            name='article2tag',
            options={'verbose_name': '文章-标签', 'verbose_name_plural': '文章-标签'},
        ),
        migrations.AlterModelOptions(
            name='articledetail',
            options={'verbose_name': '文章详情', 'verbose_name_plural': '文章详情'},
        ),
        migrations.AlterModelOptions(
            name='articleupdown',
            options={'verbose_name': '文章-点赞', 'verbose_name_plural': '文章-点赞'},
        ),
        migrations.AlterModelOptions(
            name='blog',
            options={'verbose_name': 'blog站点', 'verbose_name_plural': 'blog站点'},
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': '文章分类', 'verbose_name_plural': '文章分类'},
        ),
        migrations.AlterModelOptions(
            name='comment',
            options={'verbose_name': '评论', 'verbose_name_plural': '评论'},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'verbose_name': '标签', 'verbose_name_plural': '标签'},
        ),
        migrations.AlterModelOptions(
            name='userinfo',
            options={'verbose_name': '用户', 'verbose_name_plural': '用户'},
        ),
        migrations.AddField(
            model_name='comment',
            name='parent_comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app01.Comment'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='phone',
            field=models.CharField(max_length=11, null=True, unique=True, verbose_name='手机号'),
        ),
        migrations.AlterUniqueTogether(
            name='article2tag',
            unique_together={('article', 'tag')},
        ),
        migrations.AlterUniqueTogether(
            name='articleupdown',
            unique_together={('article', 'user')},
        ),
    ]