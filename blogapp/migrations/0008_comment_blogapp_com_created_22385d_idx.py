# Generated by Django 4.1.5 on 2023-02-24 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0007_alter_post_video'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='comment',
            index=models.Index(fields=['created'], name='blogapp_com_created_22385d_idx'),
        ),
    ]