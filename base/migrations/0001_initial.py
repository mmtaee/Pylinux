# Generated by Django 3.0.8 on 2020-08-14 12:45

import ckeditor.fields
import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='name')),
                ('image', models.ImageField(upload_to='category/')),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', ckeditor.fields.RichTextField()),
                ('create', models.DateTimeField(auto_now_add=True, verbose_name='create time')),
            ],
            options={
                'verbose_name': 'comment',
                'verbose_name_plural': 'comments',
            },
        ),
        migrations.CreateModel(
            name='ContactUs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('subject', models.CharField(max_length=300)),
                ('message', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Messaging',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create', models.DateTimeField(auto_now_add=True, verbose_name='create time')),
                ('subject', models.CharField(max_length=500, verbose_name='subject')),
                ('message', ckeditor.fields.RichTextField()),
                ('seen', models.BooleanField(default=False, verbose_name='seen')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300, verbose_name='title')),
                ('summary', models.TextField()),
                ('text', ckeditor_uploader.fields.RichTextUploadingField()),
                ('image', models.ImageField(upload_to='post/')),
                ('image_source', models.URLField(blank=True, null=True)),
                ('study', models.PositiveIntegerField(default=5)),
                ('create', models.DateTimeField(auto_now_add=True, verbose_name='create time')),
                ('last_update', models.DateTimeField(auto_now=True, verbose_name='last update')),
                ('view', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('commenting', models.BooleanField(default=True, verbose_name='commenting')),
                ('publish', models.BooleanField(default=False, verbose_name='publish')),
            ],
            options={
                'verbose_name': 'post',
                'verbose_name_plural': 'posts',
            },
        ),
        migrations.CreateModel(
            name='ReplyMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', ckeditor.fields.RichTextField()),
                ('create', models.DateTimeField(auto_now_add=True, verbose_name='create time')),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create', models.DateTimeField(auto_now_add=True)),
                ('reason', models.CharField(choices=[('prof', 'profanity'), ('adve', 'advertising'), ('spam', 'spam')], max_length=4)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Comment')),
            ],
        ),
    ]
