# Generated by Django 3.2.5 on 2021-12-03 13:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('test_blog', '0005_alter_userprofile_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='subscribe',
        ),
    ]
