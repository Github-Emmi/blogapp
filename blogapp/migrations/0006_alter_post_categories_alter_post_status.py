# Generated by Django 4.1.5 on 2023-02-07 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0005_alter_post_categories'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='categories',
            field=models.CharField(choices=[('HTML', 'Html'), ('CSS', 'Css'), ('JS', 'JavaScripts'), ('PYTHON', 'Python'), ('DJANGO', 'django')], max_length=10),
        ),
        migrations.AlterField(
            model_name='post',
            name='status',
            field=models.CharField(choices=[('DRAFT', 'Draft'), ('PUBLISHED', 'Published'), ('TRENDING', 'Trending')], max_length=10),
        ),
    ]
