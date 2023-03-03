# Generated by Django 4.1.5 on 2023-02-07 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0003_alter_post_categories_alter_post_status'),
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
            field=models.CharField(choices=[('DF', 'Draft'), ('PB', 'Published'), ('TRNG', 'Trending')], max_length=10),
        ),
    ]