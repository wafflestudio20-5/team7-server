# Generated by Django 4.1 on 2023-02-04 05:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('velogapp', '0004_alter_postimage_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='thumbnail',
            field=models.ImageField(default='media/default.png', null=True, upload_to=''),
        ),
    ]
