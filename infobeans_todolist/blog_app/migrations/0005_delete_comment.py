# Generated by Django 4.1 on 2023-07-09 13:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0004_comment'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Comment',
        ),
    ]