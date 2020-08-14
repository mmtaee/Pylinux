# Generated by Django 3.0.8 on 2020-08-14 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_auto_20200814_1715'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contactus',
            options={'verbose_name': 'contact us', 'verbose_name_plural': 'contact us'},
        ),
        migrations.AlterModelOptions(
            name='messaging',
            options={'verbose_name': 'message', 'verbose_name_plural': 'messages'},
        ),
        migrations.AlterModelOptions(
            name='replymessage',
            options={'verbose_name': 'reply', 'verbose_name_plural': 'replies'},
        ),
        migrations.AlterModelOptions(
            name='report',
            options={'verbose_name': 'report', 'verbose_name_plural': 'reports'},
        ),
        migrations.AlterField(
            model_name='post',
            name='commenting',
            field=models.BooleanField(default=True, help_text='if checked: post commenting is disabled', verbose_name='commenting'),
        ),
    ]
