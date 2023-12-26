# Generated by Django 4.2.7 on 2023-12-21 20:16

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.query


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=150, verbose_name='Название')),
                ('anouncement', models.TextField(max_length=350, verbose_name='Аннотация')),
                ('text', models.TextField(verbose_name='Текст новости')),
                ('date', models.DateTimeField(auto_now=True, verbose_name='Дата публикации')),
                ('enable', models.BooleanField(default=True)),
                ('article_image', models.ImageField(blank=True, default='default_news.jpg', upload_to='article_images')),
                ('author', models.ForeignKey(default=django.contrib.auth.models.User, null=True, on_delete=django.db.models.query.Prefetch, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Новость',
                'verbose_name_plural': 'Новости',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('status', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
                'ordering': ['status', 'title'],
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=50)),
                ('image', models.ImageField(upload_to='article_many_images/')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.article')),
            ],
        ),
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_cat', models.CharField(max_length=20, unique=True, verbose_name='Кор. назв.')),
                ('name_cat', models.CharField(max_length=50, verbose_name='Категория Наим.')),
                ('enable_cat', models.BooleanField(default=True)),
                ('date_cat', models.DateTimeField(auto_now=True, verbose_name='Дата ввода категории')),
                ('user', models.ForeignKey(default=django.contrib.auth.models.User, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='news.categories'),
        ),
        migrations.AddField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(blank=True, to='news.tag'),
        ),
        migrations.CreateModel(
            name='ViewCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.GenericIPAddressField()),
                ('view_date', models.DateTimeField(auto_now_add=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='views', to='news.article')),
            ],
            options={
                'ordering': ('-view_date',),
                'indexes': [models.Index(fields=['-view_date'], name='news_viewco_view_da_c81d57_idx')],
            },
        ),
    ]