# Generated by Django 3.2.5 on 2021-12-03 22:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_blog', '0006_remove_userprofile_subscribe'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='profile_name',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]