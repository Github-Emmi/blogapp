# Generated by Django 4.1.5 on 2023-02-21 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0006_alter_post_categories_alter_post_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='video',
            field=models.FileField(default=None, upload_to='blog_vid/'),
        ),
    ]
