# Generated by Django 2.2.3 on 2020-03-03 13:27

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_auto_20200303_1140'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='comment_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]